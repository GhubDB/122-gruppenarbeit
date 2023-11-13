from dataclasses import dataclass
from PyQt5.QtCore import QTime


@dataclass
class UserSettings:
    target_hours_worked: QTime


DEFAULT_SETTINGS = UserSettings(target_hours_worked=8)


class SettingsStore:
    def __init__(self):
        self.default: UserSettings = DEFAULT_SETTINGS
        self.user_settins: UserSettings = None
