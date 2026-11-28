from pathlib import Path
import psutil

from src.core.wiki_helper import resolve_command_info


class ProcessWatcher:
    """Beobachtet neu gestartete Prozesse und gleicht sie mit bekannten PATH-Binaries ab."""

    def __init__(self, known_binaries: set[str]) -> None:
        self.known_binaries = known_binaries
        self._seen_pids: set[int] = set()
        self._initialized = False

    def poll_new_processes(self) -> list[tuple[str, str, str, str]]:
        """Gibt neu gestartete Prozesse als (tag, display_cmd, info_text, wiki_url) zurück."""
        current_pids: set[int] = set()
        new_rows: list[tuple[str, str, str, str]] = []

        for proc in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
            pid = proc.info.get("pid")
            if pid is None:
                continue
            current_pids.add(pid)

            if pid in self._seen_pids:
                continue

            if not self._initialized:
                continue

            name = (proc.info.get("name") or "").strip()
            cmdline = proc.info.get("cmdline") or []
            base_cmd = Path(cmdline[0]).name if cmdline else name

            if base_cmd not in self.known_binaries:
                continue

            cmd_display = " ".join(cmdline) if cmdline else base_cmd
            tag, man_cmd, wiki_url = resolve_command_info(base_cmd)
            info_text = f"{man_cmd}  |  {wiki_url.replace('https://', '')}"
            new_rows.append((tag, f">> {cmd_display}", info_text, wiki_url))

        self._seen_pids = current_pids
        self._initialized = True
        return new_rows