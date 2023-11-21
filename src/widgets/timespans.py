import sys
from PyQt5.QtWidgets import (
    QSpacerItem,
    QHBoxLayout,
    QWidget,
    QSizePolicy,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
)
from PyQt5.QtCore import QTime

from src.widgets.time_edit_row import TimeEditRow


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
