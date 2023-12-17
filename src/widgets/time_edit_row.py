from PyQt5.QtGui import QIcon, QColor, QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMessageBox,
    QHBoxLayout,
    QWidget,
    QLabel,
    QWidget,
    QHBoxLayout,
    QPushButton,
)
from PyQt5.QtCore import QTime

from src.time_management.helpers import get_current_time_in_seconds
from src.widgets.click_copy_timeedit import ClickCopyTimeedit


class TimeEditRow(QWidget):
    def __init__(self, parent, from_time=None, to_time=None):
        if from_time is None:
            from_time = get_current_time_in_seconds()
        if to_time is None:
            to_time = get_current_time_in_seconds()

        super(TimeEditRow, self).__init__()
        self.from_time: int = from_time
        self.to_time: int = to_time
        self.datetime = parent
        self.is_active = False
        self.row_layout = QHBoxLayout()
        self.row_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.row_layout)
        self.add_from_time_editor()
        self.add_to_time_editor()
        self.add_buttons()
        self.set_times()

    def add_from_time_editor(self) -> None:
        from_container = QWidget()
        from_layout = QHBoxLayout(from_container)
        from_layout.setContentsMargins(0, 0, 0, 0)
        from_container.setLayout(from_layout)
        from_label = QLabel("From:")
        from_label.setMaximumWidth(53)
        palette = from_label.palette()
        palette.setColor(from_label.foregroundRole(), QColor("#68d9fe"))
        from_label.setPalette(palette)
        from_layout.addWidget(from_label)
        self.from_time_edit = ClickCopyTimeedit()
        self.from_time_edit.setDisplayFormat("HH:mm:ss")
        self.from_time_edit.setMinimumHeight(25)
        self.from_time_edit.timeChanged.connect(self.on_from_time_changed)
        from_layout.addWidget(self.from_time_edit)
        self.row_layout.addWidget(from_container)

    def add_to_time_editor(self) -> None:
        to_container = QWidget()
        to_layout = QHBoxLayout(to_container)
        to_layout.setContentsMargins(5, 0, 0, 0)
        to_container.setLayout(to_layout)
        to_label = QLabel("To:")
        to_label.setMaximumWidth(50)
        palette = to_label.palette()
        palette.setColor(to_label.foregroundRole(), QColor("#68d9fe"))
        to_label.setPalette(palette)
        to_layout.addWidget(to_label)
        self.to_time_edit = ClickCopyTimeedit()
        self.to_time_edit.timeChanged.connect(self.on_to_time_changed)
        self.to_time_edit.setDisplayFormat("HH:mm:ss")
        self.to_time_edit.setMinimumHeight(25)
        to_layout.addWidget(self.to_time_edit)
        self.row_layout.addWidget(to_container)

    def add_buttons(self) -> None:
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(5, 0, 0, 0)
        button_container.setLayout(button_layout)
        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setToolTip("Ctrl / Cmd + D")
        self.delete_button.clicked.connect(self.delete_row)
        self.start_button = QPushButton("", self)
        self.start_button.setToolTip("Ctrl / Cmd + S")
        self.start_button.clicked.connect(self.toggle_timer)
        self.start_button.setMinimumHeight(25)
        self.set_button_to_start(self.start_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.start_button)
        self.row_layout.addWidget(button_container)

    def set_times(self) -> None:
        t = QTime(0, 0)
        to_time = t.addSecs(self.to_time)
        self.to_time_edit.setTime(to_time)
        t = QTime(0, 0)
        from_time = t.addSecs(self.from_time)
        self.from_time_edit.setTime(from_time)

    def on_from_time_changed(self, time: QTime) -> None:
        # Restricts users from specifying a "From" time that precedes the "To" time.
        to_time = self.to_time_edit.time()
        if to_time.secsTo(time) > 0:
            self.from_time_edit.setTime(to_time)

    def on_to_time_changed(self, time: QTime) -> None:
        # Restricts users from specifying a "To" time that precedes the "From" time.
        from_time = self.from_time_edit.time()
        if time.secsTo(from_time) > 0:
            self.to_time_edit.setTime(from_time)

    def set_button_to_start(self, button: QPushButton) -> None:
        button.setText("Start")
        palette = button.palette()
        palette.setColor(button.foregroundRole(), QColor("#bdf7bc"))
        button.setPalette(palette)

    def set_button_to_stop(self, button: QPushButton) -> None:
        button.setText("Stop")
        palette = button.palette()
        palette.setColor(button.foregroundRole(), QColor("#f7d5bc"))
        button.setPalette(palette)

    def delete_row(self) -> None:
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete this timer?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes and not self.is_active:
            self.datetime.rows.remove(self)
            self.deleteLater()

    def toggle_timer(self) -> None:
        self.datetime.unset_active_timer(self)

        if not self.is_active:
            self.set_button_to_stop(self.start_button)
            self.datetime.set_active_timer(self)
            self.is_active = True

        else:
            self.set_button_to_start(self.start_button)
            self.is_active = False

    def add_one_second(self) -> None:
        current_time = self.to_time_edit.time()
        new_time = current_time.addSecs(1)
        self.to_time_edit.setTime(new_time)

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        # Add Hotkeys
        mods = event.modifiers()

        if event.key() == Qt.Key_D and (mods & Qt.ControlModifier):
            self.delete_row()

        if event.key() == Qt.Key_S and (mods & Qt.ControlModifier):
            self.toggle_timer()

        return super().keyPressEvent(event)
