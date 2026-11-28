import tkinter as tk

from src.core.bin_scanner import scan_path_binaries
from src.core.process_watcher import ProcessWatcher
from src.ui.window import MonitorWindow


def main() -> None:
    binaries = scan_path_binaries()
    watcher = ProcessWatcher(known_binaries=set(binaries.keys()))
    watcher.poll_new_processes()  # Vorhandene Prozesse beim Start als Basis merken

    app = MonitorWindow()

    def poll_loop() -> None:
        for tag, cmd_text, info_text, _wiki_url in watcher.poll_new_processes():
            row_idx = len(app.tree.get_children())
            row_tag = "even" if row_idx % 2 == 0 else "odd"
            app.tree.insert("", tk.END, values=(tag, cmd_text, info_text), tags=(row_tag,))

        app.root.after(500, poll_loop)

    app.root.after(500, poll_loop)
    app.run()


if __name__ == "__main__":
    main()