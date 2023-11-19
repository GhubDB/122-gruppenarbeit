from datetime import datetime, timedelta
import sys
from PyQt5.QtWidgets import (
    QSpacerItem,
    QLabel,
    QVBoxLayout,
    QWidget,
    QApplication,
    QHBoxLayout,
    QSizePolicy,
    QDateTimeEdit,
    QTimeEdit,
)
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtCore import QTime, Qt, QDate

from src.settings.user_settings import USER_SETTINGS, UserSettings


class DatetimeDisplay(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.seconds_remaining: int = 0

        self.add_layout()
        self.add_statusbar()
        self.add_current_time()
        self.add_elapsed_and_remaining_time()
        self.show_current_time()

    def add_layout(self):
        self.layout = QVBoxLayout()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setMaximumHeight(210)
        self.setLayout(self.layout)

    def add_statusbar(self):
        container = QWidget()
        self.statusbar_layout = QHBoxLayout()
        self.statusbar_layout.setContentsMargins(0, 0, 0, 0)
        self.add_date_edit()
        self.add_target_workhours_edit()
        container.setLayout(self.statusbar_layout)
        self.layout.addWidget(container)

    def add_date_edit(self):
        date = QLabel("Date:")
        date.setMaximumWidth(33)
        palette = date.palette()
        palette.setColor(date.foregroundRole(), QColor("#68d9fe"))
        date.setPalette(palette)
        date_edit = QDateTimeEdit(QDate.currentDate(), calendarPopup=True)
        date_edit.setMinimumDate(QDate.currentDate().addDays(-9365))
        date_edit.setMaximumDate(QDate.currentDate().addDays(9365))
        date_edit.setDisplayFormat("dd.MM.yyyy")
        self.statusbar_layout.addWidget(date)
        self.statusbar_layout.addWidget(date_edit)

    def add_target_workhours_edit(self):
        target_hours = QLabel("Target Hours:")
        palette = target_hours.palette()
        palette.setColor(target_hours.foregroundRole(), QColor("#68d9fe"))
        target_hours.setPalette(palette)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.target_hours_worked_edit = QTimeEdit(USER_SETTINGS.get.target_hours_worked)
        self.target_hours_worked_edit.timeChanged.connect(
            USER_SETTINGS.set_target_hours_worked
        )
        self.statusbar_layout.addItem(spacer)
        self.statusbar_layout.addWidget(target_hours)
        self.statusbar_layout.addWidget(self.target_hours_worked_edit)

    def add_current_time(self) -> None:
        font = QFont("Arial", 90, QFont.Bold)
        self.current_time = QLabel()
        self.current_time.setAlignment(Qt.AlignCenter)
        palette = self.current_time.palette()
        palette.setColor(self.current_time.foregroundRole(), QColor("#68d9fe"))
        self.current_time.setPalette(palette)
        self.current_time.setFont(font)
        self.current_time.setStyleSheet("background: transparent;")
        self.layout.addWidget(self.current_time)

    def add_elapsed_and_remaining_time(self) -> None:
        self.elapsed_and_remaining = QWidget()
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.elapsed_and_remaining.setLayout(h_layout)
        self.elapsed_and_remaining.setStyleSheet("background: transparent;")
        self.add_elapsed_time(h_layout)
        self.add_remaining_time(h_layout)
        self.layout.addWidget(self.elapsed_and_remaining)

    def add_elapsed_time(self, layout) -> None:
        font = QFont("Arial", 40, QFont.Bold)
        self.elapsed_time = QLabel("+00:00:00")
        palette = self.elapsed_time.palette()
        palette.setColor(self.elapsed_time.foregroundRole(), QColor("#bdf7bc"))
        self.elapsed_time.setPalette(palette)
        self.elapsed_time.setFont(font)
        layout.addWidget(self.elapsed_time)

    def add_remaining_time(self, layout) -> None:
        font = QFont("Arial", 40, QFont.Bold)
        self.remaining_time = Label(
            self, "-" + USER_SETTINGS.get.target_hours_worked.toString("hh:mm:ss")
        )
        palette = self.remaining_time.palette()
        palette.setColor(self.remaining_time.foregroundRole(), QColor("#f7d5bc"))
        self.remaining_time.setPalette(palette)
        self.remaining_time.setFont(font)
        layout.addWidget(self.remaining_time)

    def update_time_display(self, hours_worked):
        self.show_current_time()
        self.show_hours_worked(hours_worked)
        self.show_hours_remaining(hours_worked)

    def show_current_time(self) -> None:
        current_time = QTime.currentTime()
        label_time = current_time.toString("hh:mm:ss")
        self.current_time.setText(label_time)

    def show_hours_worked(self, hours_worked: QTime):
        label_time = hours_worked.toString("hh:mm:ss")
        self.elapsed_time.setText("+" + label_time)

    def show_hours_remaining(self, hours_worked: QTime):
        self.seconds_remaining = hours_worked.secsTo(
            USER_SETTINGS.get.target_hours_worked
        )
        if self.seconds_remaining >= 0:
            remaining_time_str = self.seconds_to_hhmmss(self.seconds_remaining)
        else:
            remaining_time_str = "00:00:00"
        self.remaining_time.setText("-" + remaining_time_str)

    def seconds_to_hhmmss(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        time_str = "{:02}:{:02}:{:02}".format(int(h), int(m), int(s))
        return time_str

    def get_target_hour(self):
        current_time = datetime.now()
        if 0 > self.seconds_remaining:
            target_time = current_time - timedelta(seconds=self.seconds_remaining)
        else:
            target_time = current_time + timedelta(seconds=self.seconds_remaining)
        target_time_str = target_time.strftime("%H:%M")
        return "To: " + target_time_str


class Label(QLabel):
    def __init__(self, parent: DatetimeDisplay, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.date_time_display: DatetimeDisplay = parent
        self.hover = False

    def enterEvent(self, event):
        self.setText(self.date_time_display.get_target_hour())
        self.hover = True

    def leaveEvent(self, event):
        self.hover = False

    def setText(self, args):
        if self.hover:
            return

        super().setText(args)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = DatetimeDisplay()
    window.show()
    App.exit(App.exec_())
