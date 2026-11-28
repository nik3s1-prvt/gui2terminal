import os
from pathlib import Path


def scan_path_binaries() -> dict[str, str]:
    """Findet alle ausführbaren Dateien in PATH und liefert {befehlsname: pfad}."""
    binaries: dict[str, str] = {}
    path_env = os.environ.get("PATH", "")

    for raw_dir in path_env.split(os.pathsep):
        if not raw_dir:
            continue
        directory = Path(raw_dir)
        if not directory.is_dir():
            continue

        try:
            for entry in directory.iterdir():
                if entry.name in binaries:
                    continue
                if entry.is_file() and os.access(entry, os.X_OK):
                    binaries[entry.name] = str(entry)
        except PermissionError:
            continue

    return binaries