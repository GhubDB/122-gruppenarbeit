from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QLabel,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QTimeEdit,
)
from PyQt5.QtCore import QTime


class TimeEditRow(QWidget):
    def __init__(self, parent):
        super(TimeEditRow, self).__init__()
        self.datetime = parent
        self.is_active = False
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 0, 0, 0)
        self.add_timeedits()
        self.add_labels()
        self.add_button()
        self.configure_layout()

    def add_timeedits(self):
        self.time_edit1 = QTimeEdit()
        self.time_edit2 = QTimeEdit()
        self.time_edit2.timeChanged.connect(self.on_time_changed)
        self.time_edit1.setDisplayFormat("HH:mm:ss")
        self.time_edit2.setDisplayFormat("HH:mm:ss")
        self.time_edit1.setMinimumHeight(25)
        self.time_edit2.setMinimumHeight(25)

    def on_time_changed(self, time: QTime):
        # Restricts users from specifying a "To" time that precedes the "From" time.
        from_time = self.time_edit1.time()
        if time.secsTo(from_time) > 0:
            self.time_edit2.setTime(from_time)

    def add_labels(self):
        self.from_label = QLabel("From:")
        self.to_label = QLabel("To:")
        self.from_label.setMaximumWidth(53)
        self.to_label.setMaximumWidth(50)
        palette = self.from_label.palette()
        palette.setColor(self.from_label.foregroundRole(), QColor("#68d9fe"))
        self.from_label.setPalette(palette)
        palette = self.to_label.palette()
        palette.setColor(self.to_label.foregroundRole(), QColor("#68d9fe"))
        self.to_label.setPalette(palette)

    def add_button(self):
        self.start_button = QPushButton("", self)
        self.set_button_to_start(self.start_button)
        self.start_button.clicked.connect(self.toggle_timer)

    def set_button_to_start(self, button: QPushButton):
        button.setText("Start")
        palette = button.palette()
        palette.setColor(button.foregroundRole(), QColor("#bdf7bc"))
        button.setPalette(palette)

    def set_button_to_stop(self, button: QPushButton):
        button.setText("Stop")
        palette = button.palette()
        palette.setColor(button.foregroundRole(), QColor("#f7d5bc"))
        button.setPalette(palette)

    def configure_layout(self):
        self.layout.addWidget(self.from_label)
        self.layout.addWidget(self.time_edit1, stretch=1)
        self.layout.addWidget(self.to_label)
        self.layout.addWidget(self.time_edit2, stretch=1)
        self.layout.addWidget(self.start_button)
        self.setLayout(self.layout)

    def toggle_timer(self):
        self.datetime.unset_active_timer(self)

        if not self.is_active:
            self.set_button_to_stop(self.start_button)
            self.datetime.set_active_timer(self)
            self.is_active = True

        else:
            self.set_button_to_start(self.start_button)
            self.is_active = False

    def add_one_second(self):
        current_time = self.time_edit2.time()
        new_time = current_time.addSecs(1)
        self.time_edit2.setTime(new_time)
