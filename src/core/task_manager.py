"""Thread-safe task management system for async configuration processing."""

import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from dataclasses import dataclass
from contextvars import ContextVar, copy_context

from .enums import TaskStatus

logger = logging.getLogger(__name__)


@dataclass
class ConfigTask:
    """Configuration processing task."""

    task_id: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    config_data: Dict[str, Any]
    auth_token: str
    base_url: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    progress: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response."""
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "progress": self.progress,
            "result": self.result,
            "error": self.error,
        }


# Context variable to store the current task ID (thread-safe)
_current_task_id: ContextVar[Optional[str]] = ContextVar(
    "current_task_id", default=None
)


def get_current_task_id() -> Optional[str]:
    """Get the current task ID from context."""
    return _current_task_id.get()


def set_current_task_id(task_id: str) -> None:
    """Set the current task ID in context."""
    _current_task_id.set(task_id)


class TaskManager:
    """Concurrent task manager using context isolation for configuration processing."""

    def __init__(self, task_expiry_hours: int = 24):
        self._tasks: Dict[str, ConfigTask] = {}
        self._background_tasks: set = set()
        self.task_expiry_hours = task_expiry_hours

    def create_task(
        self,
        config_data: Dict[str, Any],
        auth_token: str,
        base_url: Optional[str] = None,
    ) -> str:
        """Create a new configuration processing task."""
        task_id = str(uuid.uuid4())
        now = datetime.utcnow()

        task = ConfigTask(
            task_id=task_id,
            status=TaskStatus.PENDING,
            created_at=now,
            updated_at=now,
            config_data=config_data,
            auth_token=auth_token,
            base_url=base_url,
        )

        self._tasks[task_id] = task

        logger.info(f"Created task {task_id}")
        return task_id

    def get_task(self, task_id: str) -> Optional[ConfigTask]:
        """Get task by ID."""
        task = self._tasks.get(task_id)
        if task:
            # Check if task has expired
            if self._is_task_expired(task):
                self._mark_task_expired(task)
        return task

    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        progress: Optional[str] = None,
    ) -> None:
        """Update task status and metadata."""
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

    def start_background_task(self, task_id: str, processor) -> None:
        """Start background processing for a task with proper context isolation."""
        # Copy the current context to isolate this background task
        ctx = copy_context()

        # Create the background task within the copied context
        background_task = ctx.run(
            asyncio.create_task,
            self._process_config_background(task_id, processor),
            name=f"config_task_{task_id}",
        )

        # Track background tasks
        self._background_tasks.add(background_task)
        background_task.add_done_callback(self._background_tasks.discard)

        logger.info(f"Started background processing for task {task_id}")

    async def _process_config_background(self, task_id: str, processor) -> None:
        """Process configuration in background with proper context."""
        try:
            # Set the current task ID in context for this background task
            set_current_task_id(task_id)

            # Get the task data
            task = self.get_task(task_id)
            if not task:
                logger.error(f"Task {task_id} not found")
                return

            self.update_task_status(
                task_id,
                TaskStatus.PROCESSING,
                progress="Starting configuration processing...",
            )

            # Process the configuration using the existing processor
            result = await processor.process_config(
                config=task.config_data,
                auth_token=task.auth_token,
                base_url=task.base_url,
            )

            # Mark as completed
            self.update_task_status(
                task_id,
                TaskStatus.COMPLETED,
                result=result,
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

    def _is_task_expired(self, task: ConfigTask) -> bool:
        """Check if a task has expired."""
        expiry_time = task.created_at + timedelta(hours=self.task_expiry_hours)
        return datetime.utcnow() > expiry_time

    def _mark_task_expired(self, task: ConfigTask) -> None:
        """Mark task as expired."""
        if task.status in [TaskStatus.PENDING, TaskStatus.PROCESSING]:
            task.status = TaskStatus.EXPIRED
            task.updated_at = datetime.datetime.utcnow()
            task.error = "Task expired"
            logger.info(f"Marked task {task.task_id} as expired")

    def cleanup_expired_tasks(self) -> int:
        """Clean up expired tasks and return count removed."""
        expired_tasks = []
        for task_id, task in self._tasks.items():
            if self._is_task_expired(task):
                expired_tasks.append(task_id)

        for task_id in expired_tasks:
            del self._tasks[task_id]

        if expired_tasks:
            logger.info(f"Cleaned up {len(expired_tasks)} expired tasks")

        return len(expired_tasks)

    def get_task_count(self) -> Dict[str, int]:
        """Get count of tasks by status."""
        counts = {status.value: 0 for status in TaskStatus}
        for task in self._tasks.values():
            if self._is_task_expired(task):
                self._mark_task_expired(task)
            counts[task.status.value] += 1
        return counts


# Global task manager instance
task_manager = TaskManager()
