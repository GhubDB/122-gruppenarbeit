from PyQt5.QtCore import QTimer, QObject
from src.settings.user_settings import USER_SETTINGS

from src.widgets.datetime_display import DatetimeDisplay
from src.widgets.timespan_editor import TimespanEditor


class Timekeeper(QObject):
    def __init__(self, timespan_editor, datetime_display):
        super().__init__()
        self.settings = USER_SETTINGS
        self.datetime_display: DatetimeDisplay = datetime_display
        self.timespan_editor: TimespanEditor = timespan_editor
        self.add_timer()
        self.connect_to_timers()

    def add_timer(self) -> None:
        self.timer = QTimer(self)
        self.timer.start(1000)

    def connect_to_timers(self):
        self.connect_to_timer(self.push_time_to_datetime_display)
        self.connect_to_timer(self.increment_active_timer)

    def connect_to_timer(self, method):
        self.timer.timeout.connect(method)

    def disconnect_from_timer(self, method):
        self.timer.disconnect(method)

    def push_time_to_datetime_display(self):
        total_time_worked = self.timespan_editor.get_total_time_worked()
        self.datetime_display.update_time_display(total_time_worked)

    def increment_active_timer(self):
        self.timespan_editor.increment_active_timer()
