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
    QTimeEdit,
)
from PyQt5.QtCore import QTime


class TimeEditRow(QWidget):
    def __init__(self, parent):
        super(TimeEditRow, self).__init__()
        self.datetime = parent
        self.is_active = False
        self.row_layout = QHBoxLayout()
        self.row_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.row_layout)
        self.add_from_time_editor()
        self.add_to_time_editor()
        self.add_buttons()

    def on_time_changed(self, time: QTime):
        # Restricts users from specifying a "To" time that precedes the "From" time.
        from_time = self.time_edit1.time()
        if time.secsTo(from_time) > 0:
            self.time_edit2.setTime(from_time)

    def add_from_time_editor(self):
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
        self.time_edit1 = QTimeEdit()
        self.time_edit1.setDisplayFormat("HH:mm:ss")
        self.time_edit1.setMinimumHeight(25)
        from_layout.addWidget(self.time_edit1)
        self.row_layout.addWidget(from_container)

    def add_to_time_editor(self):
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
        self.time_edit2 = QTimeEdit()
        self.time_edit2.timeChanged.connect(self.on_time_changed)
        self.time_edit2.setDisplayFormat("HH:mm:ss")
        self.time_edit2.setMinimumHeight(25)
        to_layout.addWidget(self.time_edit2)
        self.row_layout.addWidget(to_container)

    def add_buttons(self):
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(5, 0, 0, 0)
        button_container.setLayout(button_layout)
        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setToolTip("Ctrl / Cmd + D")
        self.delete_button.clicked.connect(self.delete_row)
        self.start_button = QPushButton("", self)
        self.start_button.clicked.connect(self.toggle_timer)
        self.start_button.setMinimumHeight(25)
        self.set_button_to_start(self.start_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.start_button)
        self.row_layout.addWidget(button_container)

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

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        # Add Hotkeys
        mods = event.modifiers()

        if event.key() == Qt.Key_D and (mods & Qt.ControlModifier):
            self.delete_row()

        return super().keyPressEvent(event)
