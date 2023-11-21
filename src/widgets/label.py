from PyQt5.QtWidgets import QLabel

from src.time_management.helpers import get_target_hour


class Label(QLabel):
    def __init__(self, parent, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.date_time_display = parent
        self.hover = False

    def enterEvent(self, event):
        self.setText(get_target_hour(self.date_time_display.seconds_remaining))
        self.hover = True

    def leaveEvent(self, event):
        self.hover = False

    def setText(self, args):
        if self.hover:
            return

        super().setText(args)
