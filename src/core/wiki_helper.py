COMMAND_INFO = {
    "mkdir": ("FS", "man mkdir", "https://wiki.ubuntuusers.de/Shell/mkdir/"),
    "cd": ("FS", "man cd", "https://wiki.archlinux.org/title/Bash"),
    "ls": ("FS", "man ls", "https://wiki.ubuntuusers.de/Shell/ls/"),
    "rm": ("FS", "man rm", "https://wiki.ubuntuusers.de/Shell/rm/"),
    "cp": ("FS", "man cp", "https://wiki.ubuntuusers.de/Shell/cp/"),
    "mv": ("FS", "man mv", "https://wiki.ubuntuusers.de/Shell/mv/"),
}


def resolve_command_info(cmd_name: str) -> tuple[str, str, str]:
    """Liefert (tag, man_cmd, wiki_url) für einen Befehl."""
    if cmd_name in COMMAND_INFO:
        return COMMAND_INFO[cmd_name]
    return ("CMD", f"man {cmd_name}", "https://wiki.ubuntuusers.de/Startseite/")