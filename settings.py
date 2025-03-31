import json
import os

class Settings:
    def __init__(self):
        self.settings_file = os.path.expanduser('~/.config/blueberry/settings.json')
        self.settings = {
            'last_directory': '',
            'playlist': [],
            'current_index': -1,
            'current_font': 'default',
            'last_theme': 'classic'
            }
        self.load_settings()

    def load_settings(self):
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")