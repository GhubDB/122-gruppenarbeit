import sys
import typing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QWidget,
    QStackedWidget,
)
import qtstylish
from src.settings.user_settings import UserSettings
from src.time_management.timekeeper import Timekeeper
from src.stylesheets.stylesheets import Stylesheets
from src.widgets.datetime import DatetimeDisplay
from src.widgets.timespans import TimespanEditor


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.add_user_settings()
        self.setup_central_window()
        self.add_splitters()
        self.add_timespan_editor()
        self.add_datetime_display()
        self.setStyleSheet(Stylesheets.custom_dark)
        self.add_timekeeper()

    def add_user_settings(self):
        pass
        # self.settings = UserSettings(QTime())

    def setup_central_window(self) -> None:
        self.setObjectName("Central Window")
        self.central_widget = QWidget(self)
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
        self.timekeeper = Timekeeper(self.datetime, self.timespan_editor)

    def keyPressEvent(self, event: QtGui.QKeyEvent | None) -> None:
        mods = event.modifiers()

        if event.key() == Qt.Key_N:
            self.timespan_editor.add_time_edit_row()

        elif Qt.Key_G and (mods & Qt.ControlModifier):
            self.timespan_editor.delete_selected_time_edit_row()

        return super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qtstylish.dark())
    win = MainWindow()
    win.resize(420, 250)
    win.show()
    sys.exit(app.exec_())
