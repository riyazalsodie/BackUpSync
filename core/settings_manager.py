import json
import os

class SettingsManager:
    SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".backupsync_settings.json")

    @staticmethod
    def save_settings(data):
        try:
            with open(SettingsManager.SETTINGS_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    @staticmethod
    def load_settings():
        if os.path.exists(SettingsManager.SETTINGS_FILE):
            try:
                with open(SettingsManager.SETTINGS_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")
        return {}
