import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (
    QFrame,
    QApplication,
    QGridLayout,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QStackedWidget,
)
from src.database.CRUD_db import Database
from src.settings.user_settings import USER_SETTINGS
from src.stylesheets.stylesheets import Stylesheets
from src.time_management.helpers import (
    convert_qdate_to_datetime,
    convert_qtime_to_int,
)
from src.time_management.timekeeper import Timekeeper
from src.widgets.datetime_display import DatetimeDisplay
from src.widgets.time_edit_row import TimeEditRow
from src.widgets.timespan_editor import TimespanEditor


class MainWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        self.settings = USER_SETTINGS
        self.add_database()
        self.setup_central_window()
        self.add_splitters()
        self.add_datetime_display()
        self.add_timespan_editor()
        self.add_timekeeper()

    def add_database(self):
        self.database = Database()

    def setup_central_window(self) -> None:
        self.setObjectName("Central Window")
        self.central_widget = QWidget(self)
        self.setMaximumWidth(413)
        self.setCentralWidget(self.central_widget)
        self.central_grid = QGridLayout(self.central_widget)
        self.central_grid.setObjectName("Central Grid")
        self.central_stacked_widget = QStackedWidget(self.central_widget)
        self.central_stacked_widget.setFrameShape(QFrame.NoFrame)
        self.central_stacked_widget.setLineWidth(0)
        self.central_stacked_widget.setObjectName("Central Stacked Widget")
        self.central_grid.addWidget(self.central_stacked_widget, 0, 0, 1, 1)

    def add_splitters(self) -> None:
        self.app_container = QWidget()
        self.app_container_layout = QVBoxLayout()
        self.app_container_layout.setContentsMargins(0, 0, 0, 0)
        self.central_stacked_widget.addWidget(self.app_container)
        self.app_container.setLayout(self.app_container_layout)

    def add_timespan_editor(self) -> None:
        self.timespan_editor_container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        self.timespan_editor = TimespanEditor(self)
        container_layout.addWidget(self.timespan_editor)
        self.timespan_editor_container.setLayout(container_layout)
        self.app_container_layout.addWidget(self.timespan_editor_container)
        converted_date = self.get_current_date()
        self.add_time_edit_rows_to_editor(converted_date)

    def add_datetime_display(self) -> None:
        self.datetime_display_container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        self.datetime_display = DatetimeDisplay(self)
        container_layout.addWidget(self.datetime_display)
        self.datetime_display_container.setLayout(container_layout)
        self.app_container_layout.addWidget(self.datetime_display_container)

    def add_timekeeper(self):
        self.timekeeper = Timekeeper(self.timespan_editor, self.datetime_display)

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        # Add Hotkeys
        mods = event.modifiers()

        if event.key() == Qt.Key_N and (mods & Qt.ControlModifier):
            self.timespan_editor.add_time_edit_row()

        return super().keyPressEvent(event)

    def get_current_date(self):
        current_date = self.datetime_display.date_edit.date()
        return convert_qdate_to_datetime(current_date)

    # database
    def save_editor_values_to_database(self, time_edit_row: TimeEditRow):
        converted_date = self.get_current_date()
        self.database.insert_time_entry_into_db(
            converted_date,
            time_edit_row.identifier,
            convert_qtime_to_int(time_edit_row.from_time_edit),
            convert_qtime_to_int(time_edit_row.to_time_edit),
        )

    def add_time_edit_rows_to_editor(self, date):
        time_entries = self.database.read_time_entries_from_db(date)
        self.timespan_editor.add_time_edit_rows(time_entries)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Stylesheets.elegantdark)
    win = MainWindow(app)
    win.resize(420, 250)
    win.show()
    sys.exit(app.exec_())
