from PyQt5.QtWidgets import QLabel

from src.time_management.helpers import seconds_to_hhmm


class Label(QLabel):
    def __init__(self, parent, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.date_time_display = parent
        self.hover = False

    def enterEvent(self, event) -> None:
        target_hour = seconds_to_hhmm(
            self.date_time_display.seconds_remaining
            + self.date_time_display.latest_time_worked
        )
        self.setText("To: " + target_hour)
        self.hover = True

    def leaveEvent(self, event) -> None:
        self.hover = False

    def setText(self, args) -> None:
        if self.hover:
            return

        super().setText(args)
