from PyQt5.QtCore import QTimer, QObject

from src.widgets.datetime import DatetimeDisplay
from src.widgets.timespans import TimespanEditor


class Timekeeper(QObject):
    def __init__(self, datetime_display, timespan_editor):
        super().__init__()
        self.datetime_display: DatetimeDisplay = datetime_display
        self.timespan_editor: TimespanEditor = timespan_editor
        self.add_timer()

    def add_timer(self) -> None:
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.connect_to_timer(self.push_time_to_datetime_display)

    def connect_to_timer(self, method):
        self.timer.timeout.connect(method)

    def disconnect_from_timer(self, method):
        self.timer.disconnect(method)

    def push_time_to_datetime_display(self):
        total_time_worked = self.timespan_editor.get_total_time_worked()
        self.datetime_display.update_time_display(total_time_worked)

    def to_hours_minutes_seconds(self, time_in_seconds) -> str:
        return time_in_seconds.toString("HH:mm:ss")


if __name__ == "__main__":
    timekeeper = Timekeeper(DatetimeDisplay(), TimespanEditor())
