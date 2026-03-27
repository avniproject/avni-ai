"""Lightweight Python playground executor using host subprocesses with conversation silos."""

import base64
import logging
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class PlaygroundExecutor:
    """Runs LLM-generated Python scripts in conversation-scoped temp directories.

    Each conversation gets its own "silo" directory under ``base_dir``.  Files
    persist across calls within the same conversation so the LLM can iterate
    (e.g. generate a bundle, then fix it).  Stale silos are cleaned up
    periodically based on ``silo_ttl_hours``.
    """

    def __init__(
        self,
        base_dir: str = "/tmp/avni-playground",
        default_timeout: int = 30,
        max_timeout: int = 120,
        silo_ttl_hours: int = 24,
    ):
        self.base_dir = Path(base_dir)
        self.default_timeout = default_timeout
        self.max_timeout = max_timeout
        self.silo_ttl_hours = silo_ttl_hours
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_or_create_silo(self, conversation_id: str) -> Path:
        """Return the silo directory for *conversation_id*, creating it if needed."""
        safe_id = conversation_id.replace("/", "_").replace("..", "_")
        silo = self.base_dir / safe_id
        silo.mkdir(parents=True, exist_ok=True)
        return silo

    def execute(
        self,
        conversation_id: str,
        code: str,
        input_files: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        auth_token: Optional[str] = None,
        avni_base_url: Optional[str] = None,
    ) -> Dict:
        """Write *code* into the silo, run it as a subprocess, and collect output.

        Args:
            conversation_id: Identifies the silo directory.
            code: Python source to execute.
            input_files: Mapping of filename → content (string or base64 for
                binary) to write into the silo before execution.
            timeout: Seconds before the subprocess is killed.
            auth_token: Injected as ``AVNI_AUTH_TOKEN`` env var.
            avni_base_url: Injected as ``AVNI_BASE_URL`` env var.

        Returns:
            Dict with keys: success, exit_code, stdout, stderr, output_files,
            silo_files.
        """
        timeout = min(timeout or self.default_timeout, self.max_timeout)
        silo = self.get_or_create_silo(conversation_id)

        # Track files that exist before execution so we can detect new ones.
        files_before = set(self._list_files(silo))

        # Write input files into silo.
        if input_files:
            for filename, content in input_files.items():
                safe_name = Path(filename).name  # prevent path traversal
                filepath = silo / safe_name
                try:
                    raw = base64.b64decode(content)
                    filepath.write_bytes(raw)
                except Exception:
                    filepath.write_text(content, encoding="utf-8")

        # Write the script.
        script_path = silo / "script.py"
        script_path.write_text(code, encoding="utf-8")

        # Build a minimal env — only pass what's needed.
        env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": str(silo),
            "PYTHONUNBUFFERED": "1",
        }
        if auth_token:
            env["AVNI_AUTH_TOKEN"] = auth_token
        if avni_base_url:
            env["AVNI_BASE_URL"] = avni_base_url

        try:
            proc = subprocess.run(
                ["python", str(script_path)],
                cwd=str(silo),
                env=env,
                capture_output=True,
                timeout=timeout,
                text=True,
            )
            exit_code = proc.returncode
            stdout = proc.stdout
            stderr = proc.stderr
            success = exit_code == 0
        except subprocess.TimeoutExpired:
            exit_code = -1
            stdout = ""
            stderr = f"Script timed out after {timeout}s"
            success = False
        except Exception as e:
            exit_code = -1
            stdout = ""
            stderr = str(e)
            success = False

        # Collect output files (new or modified since execution started).
        files_after = set(self._list_files(silo))
        new_files = files_after - files_before - {"script.py"}

        output_files: Dict[str, str] = {}
        for fname in sorted(new_files):
            fpath = silo / fname
            try:
                output_files[fname] = fpath.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                output_files[fname] = base64.b64encode(fpath.read_bytes()).decode()

        return {
            "success": success,
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
            "output_files": output_files,
            "silo_files": sorted(self._list_files(silo)),
        }

    def list_silo_files(self, conversation_id: str) -> List[str]:
        """List files in a conversation's silo."""
        silo = self.get_or_create_silo(conversation_id)
        return sorted(self._list_files(silo))

    def cleanup_stale_silos(self) -> int:
        """Delete silos older than ``silo_ttl_hours``.  Returns count removed."""
        cutoff = time.time() - (self.silo_ttl_hours * 3600)
        removed = 0
        if not self.base_dir.exists():
            return 0
        for child in self.base_dir.iterdir():
            if child.is_dir() and child.stat().st_mtime < cutoff:
                try:
                    shutil.rmtree(child)
                    removed += 1
                    logger.info(f"Cleaned up stale silo: {child.name}")
                except Exception as e:
                    logger.error(f"Failed to clean silo {child.name}: {e}")
        return removed

    @staticmethod
    def _list_files(directory: Path) -> List[str]:
        """Return relative file names (non-recursive) in *directory*."""
        return [f.name for f in directory.iterdir() if f.is_file()]
