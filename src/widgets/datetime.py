import sys
from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
    QApplication,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QTime, Qt

from src.settings.user_settings import UserSettings


class DatetimeDisplay(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setMaximumHeight(190)
        self.setLayout(self.layout)
        self.add_current_time()
        self.add_elapsed_and_remaining_time()
        self.show_current_time()

    def add_current_time(self) -> None:
        font = QFont("Arial", 90, QFont.Bold)
        self.current_time = QLabel()
        self.current_time.setAlignment(Qt.AlignCenter)
        self.current_time.setFont(font)
        self.layout.addWidget(self.current_time)

    def add_elapsed_and_remaining_time(self) -> None:
        self.elapsed_and_remaining = QWidget()
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.elapsed_and_remaining.setLayout(h_layout)
        self.add_elapsed_time(h_layout)
        self.add_remaining_time(h_layout)
        self.layout.addWidget(self.elapsed_and_remaining)

    def add_elapsed_time(self, layout) -> None:
        font = QFont("Arial", 40, QFont.Bold)
        self.elapsed_time = QLabel()
        palette = self.elapsed_time.palette()
        palette.setColor(self.elapsed_time.foregroundRole(), QColor("green"))
        self.elapsed_time.setPalette(palette)
        self.elapsed_time.setFont(font)
        layout.addWidget(self.elapsed_time)

    def add_remaining_time(self, layout) -> None:
        font = QFont("Arial", 40, QFont.Bold)
        self.remaining_time = QLabel()
        palette = self.remaining_time.palette()
        palette.setColor(self.remaining_time.foregroundRole(), QColor("red"))
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

    def show_hours_worked(self, hours_worked):
        self.elapsed_time.setText(hours_worked)

    def show_hours_remaining(self, hours_worked):
        self.remaining_time.setText(
            "-" + UserSettings.target_hours_worked - hours_worked
        )


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = DatetimeDisplay()
    window.show()
    App.exit(App.exec_())
