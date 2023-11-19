from dataclasses import dataclass
from PyQt5.QtCore import QTime


@dataclass
class UserSettings:
    target_hours_worked: QTime


DEFAULT_SETTINGS = UserSettings(target_hours_worked=QTime(8, 0))


class SettingsStore:
    def __init__(self):
        self.user_settins: UserSettings = None
        self.is_settings_loaded = False
        self.load_user_settings()

    def load_user_settings(self):
        # TODO: implement
        self.is_settings_loaded = False
        self.user_settins = DEFAULT_SETTINGS

    @property
    def get(self):
        return self.user_settins

    def set_target_hours_worked(self, target_hours: QTime):
        self.user_settins.target_hours_worked = target_hours


USER_SETTINGS = SettingsStore()
