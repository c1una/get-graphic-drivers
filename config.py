from pathlib import Path
import os, sys

# config


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


DOWNLOADS_PATH = resource_path(Path.home() / "Downloads")


# DOWNLOADS_PATH = str(Path.home() / "Downloads")
NVIDIA_URL = "https://www.nvidia.com/Download/Find.aspx"
AMD_URL = "https://www.amd.com/en/support"
