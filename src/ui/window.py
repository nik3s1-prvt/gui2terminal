import tkinter as tk
from tkinter import ttk
import webbrowser


class MonitorWindow:
    """Clean dark UI window for gui2terminal (g2t)."""

    def __init__(self, donate_url: str = "https://example.com/donate") -> None:
        self.donate_url = donate_url

        self.root = tk.Tk()
        self.root.title("gui2terminal (g2t)")
        self.root.geometry("920x520")
        self.root.minsize(700, 360)

        self.bg_app = "#14161a"
        self.bg_surface = "#1c1f26"
        self.bg_row_alt = "#21252e"
        self.bg_selected = "#2b3a52"
        self.fg_primary = "#e6edf3"
        self.fg_muted = "#9aa4b2"
        self.accent = "#58a6ff"
        self.border = "#2d333b"

        self.root.configure(bg=self.bg_app)
        self._configure_styles()

        self._build_header()
        self._build_columns()
        self._build_footer()
        self._insert_placeholder_rows()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("App.TFrame", background=self.bg_app)
        style.configure("Surface.TFrame", background=self.bg_surface)

        style.configure(
            "Title.TLabel",
            background=self.bg_app,
            foreground=self.fg_primary,
            font=("Segoe UI", 12, "bold"),
        )
        style.configure(
            "Footer.TLabel",
            background=self.bg_app,
            foreground=self.fg_muted,
            font=("Segoe UI", 9),
        )
        style.configure(
            "Donate.TButton",
            background="#232832",
            foreground=self.fg_primary,
            bordercolor=self.border,
            lightcolor="#2b313d",
            darkcolor="#1a1e26",
            padding=(12, 5),
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Donate.TButton",
            background=[("active", "#2f3644")],
            bordercolor=[("active", self.accent)],
        )

        style.configure(
            "G2T.Treeview",
            background=self.bg_surface,
            fieldbackground=self.bg_surface,
            foreground=self.fg_primary,
            bordercolor=self.border,
            lightcolor=self.border,
            darkcolor=self.border,
            rowheight=32,
            font=("Consolas", 10),
        )
        style.configure(
            "G2T.Treeview.Heading",
            background="#181b20",
            foreground=self.fg_muted,
            bordercolor=self.border,
            relief="flat",
            padding=(8, 6),
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "G2T.Treeview.Heading",
            background=[("active", "#22262e")],
        )
        style.map(
            "G2T.Treeview",
            background=[("selected", self.bg_selected)],
            foreground=[("selected", "#ffffff")],
        )

        style.configure(
            "G2T.Vertical.TScrollbar",
            background="#252a34",
            troughcolor=self.bg_surface,
            bordercolor=self.bg_surface,
            arrowcolor=self.fg_muted,
        )

    def _build_header(self) -> None:
        header = ttk.Frame(self.root, style="App.TFrame", padding=(14, 10))
        header.pack(fill=tk.X)

        title = ttk.Label(header, text="gui2terminal (g2t)", style="Title.TLabel")
        title.pack(side=tk.LEFT)

        if self.donate_url:
            donate_btn = ttk.Button(
                header,
                text="Donate",
                style="Donate.TButton",
                command=self._open_donate,
            )
            donate_btn.pack(side=tk.RIGHT)

        tk.Frame(self.root, bg=self.border, height=1).pack(fill=tk.X)

    def _build_columns(self) -> None:
        table_wrap = ttk.Frame(self.root, style="Surface.TFrame", padding=(10, 8, 10, 8))
        table_wrap.pack(fill=tk.BOTH, expand=True)

        columns = ("tag", "command", "info")
        self.tree = ttk.Treeview(
            table_wrap,
            columns=columns,
            show="headings",
            selectmode="browse",
            style="G2T.Treeview",
        )

        # Linke schmale Spalte, mittlere breite Befehls-Spalte, rechte Spalte für Wiki/Man
        self.tree.heading("tag", text="Type", anchor=tk.W)
        self.tree.heading("command", text="Command", anchor=tk.W)
        self.tree.heading("info", text="Wiki / Man", anchor=tk.W)

        self.tree.column("tag", width=110, minwidth=85, stretch=False, anchor=tk.W)
        self.tree.column("command", width=430, minwidth=240, stretch=True, anchor=tk.W)
        self.tree.column("info", width=310, minwidth=180, stretch=True, anchor=tk.W)

        self.tree.tag_configure("even", background=self.bg_surface)
        self.tree.tag_configure("odd", background=self.bg_row_alt)

        scrollbar = ttk.Scrollbar(
            table_wrap,
            orient=tk.VERTICAL,
            command=self.tree.yview,
            style="G2T.Vertical.TScrollbar",
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", self._on_double_click)

    def _build_footer(self) -> None:
        tk.Frame(self.root, bg=self.border, height=1).pack(fill=tk.X)

        footer = ttk.Frame(self.root, style="App.TFrame", padding=(14, 8))
        footer.pack(fill=tk.X)

        label = ttk.Label(
            footer,
            text="Fun project • Double-click row for wiki • Made with <3 in Germany",
            style="Footer.TLabel",
        )
        label.pack(side=tk.LEFT)

    def _insert_placeholder_rows(self) -> None:
        sample_rows = [
            ("FS", ">> mkdir test", "man mkdir  |  ubuntuusers.de/Shell"),
            ("FS", ">> cd test", "man cd  |  wiki.archlinux.org/title/Bash"),
            ("NET", ">> nmcli dev status", "man nmcli  |  wiki.archlinux.org/title/NetworkManager"),
            ("SYNC", ">> rsync -av src/ dst/", "man rsync  |  wiki.ubuntuusers.de/rsync/"),
        ]
        for idx, row in enumerate(sample_rows):
            row_tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert("", tk.END, values=row, tags=(row_tag,))

    def _open_donate(self) -> None:
        if self.donate_url:
            webbrowser.open(self.donate_url)

    def _on_double_click(self, _event: tk.Event) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        if len(values) >= 3 and "http" in values[2]:
            for part in values[2].split():
                if part.startswith(("http://", "https://")):
                    webbrowser.open(part)
                    break

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    MonitorWindow().run()