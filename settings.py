import os
import json

class Settings:
    def __init__(self):
        self.settings_file = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Blueberry', 'settings.json') if os.name == 'nt' else os.path.expanduser('~/.config/blueberry/settings.json')
        self.settings = {
            'last_directory': '',
            'playlist': [],
            'current_index': -1,
            'last_theme': 'classic',
            'current_font': 'Default',
            'shortcuts': {
                'next': 'Ctrl+Right',
                'previous': 'Ctrl+Left',
                'play_pause': 'Space',
                'stop': 'Ctrl+S',
                'volume_up': 'Ctrl+Up',
                'volume_down': 'Ctrl+Down',
                'mute': 'Ctrl+M'
            }
        }
        self.load_settings()

    def load_settings(self):
        try:
            settings_dir = os.path.dirname(self.settings_file)
            os.makedirs(settings_dir, exist_ok=True)
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    for key, value in loaded_settings.items():
                        if key == 'shortcuts' and isinstance(value, dict):
                            self.settings['shortcuts'].update(value)
                        else:
                            self.settings[key] = value
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")