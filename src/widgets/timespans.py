import sys
from os import path
from PyQt5.QtGui import QIcon, QColor, QPalette
from PyQt5.QtWidgets import (
    QSpacerItem,
    QHBoxLayout,
    QWidget,
    QSizePolicy,
    QLabel,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QTimeEdit,
)
from PyQt5.QtCore import QTime, Qt, QSize

BASE_DIR = path.dirname(path.abspath(__file__))
PAUSE_BUTTON_PATH = path.join(BASE_DIR, "assets", "pause.png")
PLAY_BUTTON_PATH = path.join(BASE_DIR, "assets", "play-button.png")


class TimeEditRow(QWidget):
    def __init__(self, parent):
        super(TimeEditRow, self).__init__()
        self.datetime: TimespanEditor = parent
        self.is_active = False
        self.start_icon = QIcon(PLAY_BUTTON_PATH)
        self.stop_icon = QIcon(PAUSE_BUTTON_PATH)
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
        self.time_edit1.setMinimumHeight(30)
        self.time_edit2.setMinimumHeight(30)

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


class TimespanEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.add_attributes()
        self.add_timeedit_container()
        self.add_buttons()
        self.setLayout(self.main_layout)
        self.add_time_edit_row()

    def add_attributes(self):
        self.rows = []
        self.active_timer = None

    def add_timeedit_container(self):
        self.main_layout = QVBoxLayout()
        self.timeedit_container = QWidget()
        self.timeedit_row_layout = QVBoxLayout()
        self.timeedit_row_layout.setContentsMargins(0, 0, 0, 0)
        self.timeedit_container.setLayout(self.timeedit_row_layout)
        self.main_layout.addWidget(self.timeedit_container)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)

    def add_buttons(self):
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        self.add_button = QPushButton("Add Timer")
        self.delete_button = QPushButton("Delete Timer")
        self.add_button.setToolTip("Ctrl / Cmd + N")
        self.delete_button.setToolTip("Ctrl / Cmd + D")
        self.add_button.setMinimumHeight(35)
        self.delete_button.setMinimumHeight(35)
        self.add_button.clicked.connect(self.add_time_edit_row)
        self.delete_button.clicked.connect(self.delete_selected_time_edit_row)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_container.setLayout(button_layout)
        self.main_layout.addWidget(button_container)

    def add_time_edit_row(self) -> None:
        if len(self.rows) >= 10:
            return
        new_row = TimeEditRow(parent=self)
        new_row.time_edit1.setTime(QTime.currentTime())
        new_row.time_edit2.setTime(QTime.currentTime())
        self.rows.append(new_row)
        # Insert at the bottom
        self.timeedit_row_layout.insertWidget(len(self.main_layout) - 1, new_row)

    def delete_selected_time_edit_row(self) -> None:
        for row in self.rows:
            if (
                row.time_edit1.hasFocus() or row.time_edit2.hasFocus()
            ) and not row == self.active_timer:
                self.rows.remove(row)
                row.deleteLater()

    def set_active_timer(self, timer: TimeEditRow):
        self.active_timer = timer

    def unset_active_timer(self, sender):
        if self.active_timer == None:
            return

        if self.active_timer != sender:
            self.active_timer.toggle_timer()

        self.active_timer = None

    def increment_active_timer(self):
        if self.active_timer == None:
            return

        self.active_timer.add_one_second()

    def get_total_time_worked(self) -> QTime:
        total_elapsed_time = QTime(0, 0)
        for row in self.rows:
            time1 = row.time_edit1.time()
            time2 = row.time_edit2.time()
            time_difference = time1.secsTo(time2)
            total_elapsed_time = total_elapsed_time.addSecs(time_difference)

        return total_elapsed_time


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimespanEditor()
    window.setWindowTitle("Time Edit Row App")
    window.show()
    sys.exit(app.exec_())
