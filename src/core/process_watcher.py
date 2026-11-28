from pathlib import Path
from typing import Callable

from src.core.wiki_helper import resolve_command_info


class CommandLogWatcher:
    """Liest neue Befehle (z. B. mkdir, cd) aus einer Test-Logdatei."""

    def __init__(self, log_path: Path, target_cmds: set[str] | None = None) -> None:
        self.log_path = log_path
        self.target_cmds = target_cmds or {"mkdir", "cd"}
        self._seen_count = 0

    def poll_new_rows(self) -> list[tuple[str, str, str, str]]:
        """Gibt neue Einträge als (tag, display_cmd, info_text, wiki_url) zurück."""
        if not self.log_path.exists():
            return []

        lines = self.log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        if len(lines) <= self._seen_count:
            return []

        new_lines = lines[self._seen_count :]
        self._seen_count = len(lines)

        rows: list[tuple[str, str, str, str]] = []
        for raw in new_lines:
            cmd_line = raw.strip()
            if not cmd_line or cmd_line.startswith("#"):
                continue

            cmd_name = cmd_line.split()[0]
            if cmd_name not in self.target_cmds:
                continue

            tag, man_cmd, wiki_url = resolve_command_info(cmd_name)
            info_text = f"{man_cmd}  |  {wiki_url.replace('https://', '')}"
            rows.append((tag, f">> {cmd_line}", info_text, wiki_url))

        return rows