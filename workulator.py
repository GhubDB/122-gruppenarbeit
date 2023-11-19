import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QWidget,
    QStackedWidget,
)
from src.settings.user_settings import USER_SETTINGS
from src.time_management.timekeeper import Timekeeper
from src.widgets.datetime import DatetimeDisplay
from src.widgets.timespans import TimespanEditor


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.settings = USER_SETTINGS
        self.setup_central_window()
        self.add_splitters()
        self.add_timespan_editor()
        self.add_datetime_display()
        self.add_timekeeper()

    def setup_central_window(self) -> None:
        self.setObjectName("Central Window")
        self.central_widget = QWidget(self)
        self.setMaximumWidth(413)
        self.setCentralWidget(self.central_widget)
        self.central_grid = QGridLayout(self.central_widget)
        self.central_grid.setObjectName("Central Grid")
        self.central_stacked_widget = QStackedWidget(self.central_widget)
        self.central_stacked_widget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.central_stacked_widget.setLineWidth(0)
        self.central_stacked_widget.setObjectName("Central Stacked Widget")
        self.central_grid.addWidget(self.central_stacked_widget, 0, 0, 1, 1)

    def add_splitters(self) -> None:
        self.timespan_splitter = QtWidgets.QSplitter(Qt.Vertical)
        self.datetime_splitter = QtWidgets.QSplitter(Qt.Horizontal)
        self.central_stacked_widget.addWidget(self.timespan_splitter)
        self.timespan_splitter.addWidget(self.datetime_splitter)

    def add_timespan_editor(self) -> None:
        self.timespan_editor = TimespanEditor()
        self.timespan_splitter.addWidget(self.timespan_editor)

    def add_datetime_display(self) -> None:
        self.datetime = DatetimeDisplay()
        self.datetime_splitter.addWidget(self.datetime)

    def add_timekeeper(self):
        self.timekeeper = Timekeeper(self.timespan_editor, self.datetime)

    def keyPressEvent(self, event: QtGui.QKeyEvent | None) -> None:
        # Add Hotkeys
        mods = event.modifiers()

        if event.key() == Qt.Key_N and (mods & Qt.ControlModifier):
            self.timespan_editor.add_time_edit_row()

        elif event.key() == Qt.Key_D and (mods & Qt.ControlModifier):
            self.timespan_editor.delete_selected_time_edit_row()

        return super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(420, 250)
    win.show()
    sys.exit(app.exec_())
