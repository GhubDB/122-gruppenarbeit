from dataclasses import dataclass
from PyQt5.QtCore import QTime


@dataclass
class UserSettings:
    target_hours_worked: QTime


DEFAULT_SETTINGS = UserSettings(target_hours_worked=QTime(8, 0))


class SettingsStore:
    def __init__(self):
        self.default_settings: UserSettings = DEFAULT_SETTINGS
        self.user_settins: UserSettings = None
        self.is_settings_loaded = False
        self.load_user_settings()

    def load_user_settings(self):
        # TODO: implement
        pass

    @property
    def get(self):
        if self.is_settings_loaded:
            return self.user_settins

        return self.default_settings


USER_SETTINGS = SettingsStore()
