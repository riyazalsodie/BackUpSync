import winreg
import sys
import os

class StartupManager:
    APP_NAME = "BackupPro"

    @staticmethod
    def set_startup(enabled=True):
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            if enabled:
                # Use sys.executable to ensure we run the same python/exe
                # If running as script, it will be python.exe script.py
                # For practical purposes in this task, we'll use the current script path
                app_path = os.path.abspath(sys.argv[0])
                # Wrap path in quotes to handle spaces
                command = f'"{sys.executable}" "{app_path}" --minimized'
                winreg.SetValueEx(key, StartupManager.APP_NAME, 0, winreg.REG_SZ, command)
            else:
                try:
                    winreg.DeleteValue(key, StartupManager.APP_NAME)
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Startup manager error: {e}")
            return False

    @staticmethod
    def is_startup_enabled():
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, StartupManager.APP_NAME)
                enabled = True
            except FileNotFoundError:
                enabled = False
            winreg.CloseKey(key)
            return enabled
        except Exception:
            return False
