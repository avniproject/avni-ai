import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Callable
from dataclasses import dataclass
from contextvars import ContextVar, copy_context
from .enums import TaskStatus
from .config_processor import ConfigProcessor

logger = logging.getLogger(__name__)


@dataclass
class ConfigTask:
    task_id: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    config_data: Dict[str, Any]
    auth_token: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    progress: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "progress": self.progress,
            "result": self.result,
            "error": self.error,
        }


_current_task_id: ContextVar[Optional[str]] = ContextVar(
    "current_task_id", default=None
)


def get_current_task_id() -> Optional[str]:
    return _current_task_id.get()


def set_current_task_id(task_id: str) -> None:
    _current_task_id.set(task_id)


class TaskManager:
    def __init__(self, task_expiry_hours: int = 24):
        self._tasks: Dict[str, ConfigTask] = {}
        self._background_tasks: set = set()
        self.task_expiry_hours = task_expiry_hours
        self._cleanup_task = None

    def _ensure_cleanup_started(self) -> None:
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._periodic_cleanup())

    async def _periodic_cleanup(self) -> None:
        while True:
            try:
                await asyncio.sleep(3600 * 12)
                cleaned = self.cleanup_old_tasks()
                if cleaned > 0:
                    logger.info(f"Periodic cleanup removed {cleaned} old tasks")
            except Exception as e:
                logger.error(f"Error in periodic cleanup: {e}")

    def create_task(
        self,
        config_data: Dict[str, Any],
        auth_token: str,
    ) -> ConfigTask:
        # Start cleanup task lazily when the first task is created
        self._ensure_cleanup_started()

        task_id = str(uuid.uuid4())
        now = datetime.utcnow()

        task = ConfigTask(
            task_id=task_id,
            status=TaskStatus.PENDING,
            created_at=now,
            updated_at=now,
            config_data=config_data,
            auth_token=auth_token,
        )

        self._tasks[task_id] = task

        logger.info(f"Created task {task_id}")
        return task

    def get_task(self, task_id: str) -> Optional[ConfigTask]:
        return self._tasks.get(task_id)

    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        progress: Optional[str] = None,
    ) -> None:
        task = self._tasks.get(task_id)
        if task:
            task.status = status
            task.updated_at = datetime.utcnow()
            if result is not None:
                task.result = result
            if error is not None:
                task.error = error
            if progress is not None:
                task.progress = progress
            logger.info(f"Updated task {task_id} status to {status.value}")

    def start_background_task(self, task_id: str) -> None:
        ctx = copy_context()

        background_task = ctx.run(
            asyncio.create_task,
            self._process_config_background(task_id),
            name=f"config_task_{task_id}",
        )

        self._background_tasks.add(background_task)
        background_task.add_done_callback(self._background_tasks.discard)

        logger.info(f"Started background processing for task {task_id}")

    def _create_progress_updater(self, task_id: str) -> Callable[[str], None]:
        """Create a progress updater callback for the given task."""

        def updater(message: str):
            self.update_task_status(task_id, TaskStatus.PROCESSING, progress=message)

        return updater

    async def _process_config_background(self, task_id: str) -> None:
        try:
            set_current_task_id(task_id)

            task = self.get_task(task_id)

            self.update_task_status(
                task_id,
                TaskStatus.PROCESSING,
                progress="Starting configuration processing...",
            )

            progress_updater = self._create_progress_updater(task_id)

            result = await ConfigProcessor.process_config(
                config=task.config_data,
                auth_token=task.auth_token,
                task_id=task_id,
                progress_callback=progress_updater,
            )

            self.update_task_status(
                task_id,
                TaskStatus.COMPLETED,
                result=result.to_dict(),
                progress="Configuration processing completed successfully",
            )

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Background task {task_id} failed: {error_msg}")
            import traceback

            logger.error(f"Full traceback: {traceback.format_exc()}")

            self.update_task_status(
                task_id,
                TaskStatus.FAILED,
                error=error_msg,
                progress="Configuration processing failed",
            )

    def cleanup_old_tasks(self) -> int:
        cutoff = datetime.utcnow() - timedelta(hours=self.task_expiry_hours)
        to_remove = []

        for task_id, task in self._tasks.items():
            if (
                task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]
                and task.updated_at < cutoff
            ):
                to_remove.append(task_id)

        for task_id in to_remove:
            del self._tasks[task_id]

        if to_remove:
            logger.info(f"Cleaned up {len(to_remove)} old completed/failed tasks")

        return len(to_remove)

    def get_task_count(self) -> Dict[str, int]:
        counts = {status.value: 0 for status in TaskStatus}
        for task in self._tasks.values():
            counts[task.status.value] += 1
        return counts


# This is a singleton
task_manager = TaskManager()
