from pathlib import Path
import tkinter as tk

from src.core.process_watcher import CommandLogWatcher
from src.ui.window import MonitorWindow


def main() -> None:
    log_path = Path("/tmp/g2t_test.log")
    watcher = CommandLogWatcher(log_path=log_path, target_cmds={"mkdir", "cd"})

    app = MonitorWindow()

    def poll_commands() -> None:
        for tag, cmd_text, info_text, _wiki_url in watcher.poll_new_rows():
            row_idx = len(app.tree.get_children())
            row_tag = "even" if row_idx % 2 == 0 else "odd"
            app.tree.insert("", tk.END, values=(tag, cmd_text, info_text), tags=(row_tag,))

        app.root.after(400, poll_commands)

    app.root.after(400, poll_commands)
    app.run()


if __name__ == "__main__":
    main()