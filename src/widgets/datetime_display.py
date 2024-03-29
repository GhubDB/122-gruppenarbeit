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

from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QTime, Qt, QDate

from src.settings.user_settings import USER_SETTINGS
from src.time_management.helpers import convert_qdate_to_datetime, seconds_to_hhmmss
from src.time_management.time_dto import TimeDTO
from src.widgets.label import Label


class DatetimeDisplay(QWidget):
    def __init__(self, workulator=None) -> None:
        super().__init__()
        self.workulator = workulator
        self.seconds_remaining: int = 0
        self.latest_time_worked: int = 0
        self.current_date: QDate = QDate.currentDate()

        self.add_layout()
        self.add_statusbar()
        self.add_current_time()
        self.add_elapsed_and_remaining_time()
        self.show_current_time()

    def add_layout(self) -> None:
        self.layout = QVBoxLayout()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setLayout(self.layout)

    def add_statusbar(self) -> None:
        container = QWidget()
        self.statusbar_layout = QHBoxLayout()
        self.statusbar_layout.setContentsMargins(0, 0, 0, 0)
        self.add_date_edit()
        self.add_target_workhours_edit()
        container.setLayout(self.statusbar_layout)
        self.layout.addWidget(container)

    def add_date_edit(self) -> None:
        container = QWidget()
        date_edit_layout = QHBoxLayout(container)
        date_edit_layout.setContentsMargins(0, 0, 0, 0)
        container.setLayout(date_edit_layout)
        date = QLabel("Date:")
        date.setMaximumWidth(53)
        palette = date.palette()
        palette.setColor(date.foregroundRole(), QColor("#68d9fe"))
        date.setPalette(palette)
        self.date_edit = QDateTimeEdit(self.current_date, calendarPopup=True)
        self.date_edit.dateChanged.connect(self.on_date_changed)
        self.date_edit.setMinimumDate(QDate.currentDate().addDays(-9365))
        self.date_edit.setMaximumDate(QDate.currentDate().addDays(9365))
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        date_edit_layout.addWidget(date)
        date_edit_layout.addWidget(self.date_edit)
        self.statusbar_layout.addWidget(container)

    def on_date_changed(self, new_date):
        converted_date = convert_qdate_to_datetime(new_date)
        self.workulator.add_time_edit_rows_to_editor(converted_date)

    def add_target_workhours_edit(self) -> None:
        container = QWidget()
        target_workhours_layout = QHBoxLayout(container)
        target_workhours_layout.setContentsMargins(0, 0, 0, 0)
        container.setLayout(target_workhours_layout)
        target_hours = QLabel("Target Hours:")
        palette = target_hours.palette()
        palette.setColor(target_hours.foregroundRole(), QColor("#68d9fe"))
        target_hours.setPalette(palette)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.target_hours_worked_edit = QTimeEdit(USER_SETTINGS.get.target_hours_worked)
        self.target_hours_worked_edit.setMinimumHeight(25)
        self.target_hours_worked_edit.timeChanged.connect(
            USER_SETTINGS.set_target_hours_worked
        )
        self.statusbar_layout.addItem(spacer)
        target_workhours_layout.addWidget(target_hours)
        target_workhours_layout.addWidget(self.target_hours_worked_edit)
        self.statusbar_layout.addWidget(container)

    def add_current_time(self) -> None:
        font = QFont("Arial", 90, QFont.Bold)
        self.current_time = QLabel()
        self.current_time.setAlignment(Qt.AlignCenter)
        palette = self.current_time.palette()
        palette.setColor(self.current_time.foregroundRole(), QColor("#68d9fe"))
        self.current_time.setPalette(palette)
        self.current_time.setFont(font)
        # self.current_time.setStyleSheet("background: transparent;")
        self.layout.addWidget(self.current_time)

    def add_elapsed_and_remaining_time(self) -> None:
        self.elapsed_and_remaining = QWidget()
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.elapsed_and_remaining.setLayout(h_layout)
        # self.elapsed_and_remaining.setStyleSheet("background: transparent;")
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

    def update_time_display(self, time_dto: TimeDTO):
        self.latest_time_worked = time_dto.latest_time_worked
        self.seconds_remaining = time_dto.seconds_remaining
        self.total_time_worked = time_dto.total_time_worked

        self.show_current_time()
        self.show_hours_worked()
        self.show_hours_remaining()

    def show_current_time(self) -> None:
        current_time = QTime.currentTime()
        label_time = current_time.toString("hh:mm:ss")
        self.current_time.setText(label_time)

    def show_hours_worked(self) -> None:
        label_time = seconds_to_hhmmss(self.total_time_worked)
        self.elapsed_time.setText("+" + label_time)

    def show_hours_remaining(self) -> None:
        if self.seconds_remaining >= 0:
            remaining_time_str = seconds_to_hhmmss(self.seconds_remaining)
        else:
            remaining_time_str = "00:00:00"
        self.remaining_time.setText("-" + remaining_time_str)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = DatetimeDisplay()
    window.show()
    App.exit(App.exec_())
