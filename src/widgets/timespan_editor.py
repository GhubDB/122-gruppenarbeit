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
from src.settings.user_settings import USER_SETTINGS
from src.time_management.time_dto import TimeDTO

from src.widgets.time_edit_row import TimeEditRow


class TimespanEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.add_attributes()
        self.add_timeedit_container()
        self.add_button()
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

    def add_button(self):
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 5, 0, 0)
        self.add_button = QPushButton("Add Timer")
        self.add_button.setToolTip("Ctrl / Cmd + N")
        self.add_button.setMinimumHeight(35)
        self.add_button.clicked.connect(self.add_time_edit_row)
        button_layout.addWidget(self.add_button)
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
        zero_time = QTime(0, 0)
        row_tuples = [
            (
                zero_time.secsTo(row.time_edit1.time()),
                zero_time.secsTo(row.time_edit2.time()),
            )
            for row in self.rows
        ]
        sorted_rows = sorted(row_tuples, key=lambda row: row[0])

        minStart = sorted_rows[0][0]
        maxEnd = sorted_rows[0][0]
        gap = 0

        for i, row in enumerate(sorted_rows):
            #  If there is a gap, increment total gap length
            if sorted_rows[i][0] > maxEnd:
                gap = gap + sorted_rows[i][0] - maxEnd

            # Update latest end time
            if sorted_rows[i][1] > maxEnd:
                maxEnd = sorted_rows[i][1]

        return maxEnd - minStart - gap

    def get_latest_time_worked(self) -> QTime:
        zero_time = QTime(0, 0)
        max_time_in_seconds = 0
        end_times = [zero_time.secsTo(row.time_edit2.time()) for row in self.rows]
        for time_in_seconds in end_times:
            if time_in_seconds > max_time_in_seconds:
                max_time_in_seconds = time_in_seconds

        return max_time_in_seconds

    def get_time_dto(self) -> TimeDTO:
        total_time_worked = self.get_total_time_worked()
        target_hours_worked_in_sedconds = QTime(0, 0).secsTo(
            USER_SETTINGS.get.target_hours_worked
        )
        seconds_left_to_work = target_hours_worked_in_sedconds - total_time_worked
        return TimeDTO(
            total_time_worked=total_time_worked,
            latest_time_worked=self.get_latest_time_worked(),
            seconds_remaining=seconds_left_to_work,
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimespanEditor()
    window.setWindowTitle("Time Edit Row App")
    window.show()
    sys.exit(app.exec_())
