# ScreenWatcher — Red Team Screen Capture Exfil Tool

**Python-based utility that monitors screen changes and exfiltrates screenshots via Telegram Bot API, with self-deletion capability.**

Built for authorized penetration testing, red team engagements, and security awareness demonstrations.

---

## Features

- Real-time screen-change detection using pixel-diff analysis (mss + numpy)
- Automatic screenshot capture on visual change
- Telegram Bot API exfiltration
- Multiple persistence mechanisms (Registry / Startup Folder)
- Self-deletion after execution (low footprint / forensic evasion)
- Compiled to standalone `.exe` via PyInstaller — no Python runtime required
- Silent operation (no console window)

---

## Use Cases

- Red team persistence and exfiltration demonstrations
- Testing endpoint detection & response (EDR) capabilities
- Security awareness training — demonstrating how low-footprint spyware operates
- Physical security audits — monitoring unattended workstations

---

## Requirements

- Python 3.8+
- Dependencies: `mss`, `numpy`, `Pillow`, `requests`
- Windows (for Registry/Startup persistence)

```bash
pip install mss numpy pillow requests pyinstaller
