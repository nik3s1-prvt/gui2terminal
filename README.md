# g2t (`gui2terminal`)

> **Read-only. Local-only. Just a fun project — keep expectations low!**

A lightweight, read-only Linux monitor that watches what happens on your system, matches launched binaries against installed `PATH` commands, shows brief local help text, and links to relevant distribution wiki pages.

## Update
The Programm can read now a few things but only if u open something

---

## System
First it will be able to use on Linux based systems, cause who tf use Windows
Anyways in the Future its sure possible it will be able to use on Windows



## What It Is

**g2t** is a small educational/curiosity monitor for Linux. Whenever programs start or system events occur, it tries to show the corresponding command-line equivalent alongside quick context and a wiki link — purely as a non-interactive, read-only observer.

It is **not** a magic GUI-to-CLI recorder for every single mouse click or canvas action inside complex apps. Think of it as a friendly side-eye at what commands get invoked on your machine.

---

## Set Your Expectations (Fun Project Disclaimer)

This is a **fun / scratch-your-own-itch project**, not enterprise software or a polished commercial product.

* **Don't expect anything crazy:** Edge cases happen, some GUI/wrapper/flatpak/snap launches won't map cleanly to a neat CLI command, and things may be rough around the edges.
* **Strictly read-only:** It **only reads** system info and **never executes** detected commands on your behalf.
* **100% local & zero telemetry:** No background tracking, no cloud database, no phone-home behavior.
* **Contains AI content:** Parts of the code, structure, and documentation were written with AI assistance.

---

## How It Works

1. **Scan `PATH` (no database):** On startup, it scans executable files in your `PATH` directories (such as `/usr/bin`, `/bin`, `/usr/local/bin`) into memory.
2. **Watch new processes:** Using `psutil` and `/proc`, it spots newly started processes and checks whether their executable name matches a known `PATH` command.
3. **Add quick context & wiki links:** It checks `/etc/os-release` to guess your distro family (e.g., Ubuntu/Kubuntu, Arch) for wiki URLs and pulls short local descriptions via `whatis` when available.
4. **Display in a read-only view:** It prints/displays detected commands, short descriptions, and wiki links without touching or running those commands.

---

## System Components Accessed & Why

| Component | Purpose | Why It's Needed |
| :--- | :--- | :--- |
| **`PATH` directories** (`/usr/bin`, `/bin`, etc.) | Lists installed executable names | To know which CLI commands actually exist on the system without maintaining a database |
| **`/proc` & `psutil`** | Observes newly spawned processes and their `cmdline` | To detect when a command/binary is launched |
| **`whatis` (local manpages)** | Fetches a one-line summary of a command | To give quick, offline context for matched commands |
| **`/etc/os-release`** | Detects the Linux distribution family | To pick a fitting wiki target (e.g., UbuntuUsers or ArchWiki) |
| **Filesystem / `inotify` (planned / optional)** | Watches file-related events | To surface relevant file/system activity without polling everything blindly |

---

## Quick Start

```bash
chmod +x install.sh
./install.sh
PYTHONPATH=src python3 src/main.py
