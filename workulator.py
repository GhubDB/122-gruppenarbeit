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
from src.settings.user_settings import USER_SETTINGS
from src.stylesheets.stylesheets import Stylesheets
from src.time_management.timekeeper import Timekeeper
from src.widgets.datetime_display import DatetimeDisplay
from src.widgets.timespan_editor import TimespanEditor


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.settings = USER_SETTINGS
        self.setup_central_window()
        self.add_splitters()
        self.add_datetime_display()
        self.add_timespan_editor()
        self.add_timekeeper()

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
        self.timespan_editor = TimespanEditor()
        container_layout.addWidget(self.timespan_editor)
        self.timespan_editor_container.setLayout(container_layout)
        self.app_container_layout.addWidget(self.timespan_editor_container)

    def add_datetime_display(self) -> None:
        self.datetime_display_container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        self.datetime = DatetimeDisplay()
        container_layout.addWidget(self.datetime)
        self.datetime_display_container.setLayout(container_layout)
        self.app_container_layout.addWidget(self.datetime_display_container)

    def add_timekeeper(self):
        self.timekeeper = Timekeeper(self.timespan_editor, self.datetime)

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        # Add Hotkeys
        mods = event.modifiers()

        if event.key() == Qt.Key_N and (mods & Qt.ControlModifier):
            self.timespan_editor.add_time_edit_row()

        return super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Stylesheets.elegantdark)
    win = MainWindow()
    win.resize(420, 250)
    win.show()
    sys.exit(app.exec_())
