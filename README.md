# screenwatcher
Python-based utility that monitors screen changes and exfiltrates screenshots via Telegram Bot API, with self-deletion capability.  Built for authorized penetration testing  and security awareness demonstrations.

Features
Real-time screen-change detection using pixel-diff analysis (mss + numpy)
Automatic screenshot capture on visual change
Telegram Bot API exfiltration
Multiple persistence mechanisms (Registry / Startup Folder)
Self-deletion after execution (low footprint / forensic evasion)
Compiled to standalone .exe via PyInstaller — no Python runtime required
Silent operation (no console window)
Use Cases
Red team persistence and exfiltration demonstrations
Testing endpoint detection & response (EDR) capabilities
Security awareness training — demonstrating how low-footprint spyware operates
Physical security audits — monitoring unattended workstations
Requirements
Python 3.8+
Dependencies: mss, numpy, Pillow, requests
Windows (for Registry/Startup persistence)
bash
pip install mss numpy pillow requests pyinstaller
Usage
1. Configuration
Edit these variables in desktop.py:
BOT_TOKEN = "YOUR_BOT_TOKEN"    # Telegram bot token from @BotFather
CHAT_ID   = "YOUR_CHAT_ID"      # Your Telegram user/group chat ID
2. Run Directly
python desktop.py
3. Compile to EXE
pyinstaller --onefile --noconsole --name ScreenWatcher.exe screenwatcher.py

Technical Details
Component	Description
Screen capture	mss library — cross-platform, fast captures
Change detection	Perceptual diff via NumPy pixel comparison
Exfiltration	HTTP multipart POST to Telegram Bot API
Persistence	HKCU Run registry key or Startup folder
Anti-forensics	Self-deletion + temp directory cleanup
Detection & Prevention
If you're a defender, look for:

Outbound HTTPS requests to api.telegram.org
Processes running from %TEMP% or %LOCALAPPDATA%\Drivers\*
Unusual PyInstaller executables (_MEI* temp folders)
Registry: HKCU\Software\Microsoft\Windows\CurrentVersion\Run\ScreenWatcher
Disclaimer
This tool is intended only for authorized security testing, penetration testing, and educational purposes. You must have explicit written permission from the system owner before deploying it. Unauthorized use is illegal and unethical. The author is not responsible for misuse.
