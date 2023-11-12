import sys
from PyQt5.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QTableView,
    QWidget,
    QSizePolicy,
    QFrame,
)
from PyQt5.QtWidgets import (
    QLabel,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QTimeEdit,
    QAbstractItemView,
)
from PyQt5.QtCore import QTime, Qt, QSize


class TimeEditRow(QWidget):
    def __init__(self):
        super(TimeEditRow, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 0, 0, 0)
        self.time_edit1 = QTimeEdit()
        self.time_edit2 = QTimeEdit()
        self.add_labels()
        self.configure_layout()

    def add_labels(self):
        self.position_label = QLabel()
        self.from_label = QLabel("From:")
        self.to_label = QLabel("To:")
        self.position_label.setMaximumWidth(35)
        self.from_label.setMaximumWidth(50)
        self.to_label.setMaximumWidth(50)

    def configure_layout(self):
        self.layout.addWidget(self.position_label)
        self.layout.addWidget(self.from_label)
        self.layout.addWidget(self.time_edit1)
        self.layout.addWidget(self.to_label)
        self.layout.addWidget(self.time_edit2)
        self.setLayout(self.layout)


class TimespanTableView(QTableView):
    def __init__(self) -> None:
        super().__init__()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(0, 0))
        self.setFrameShape(QFrame.Panel)
        self.setObjectName("Timespan Table")
        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)


class TimespanEditor(QWidget):
    def __init__(self):
        super(TimespanEditor, self).__init__()
        self.rows = []
        self.layout = QVBoxLayout()
        self.timespan_tableview = TimespanTableView()
        self.layout.addWidget(self.timespan_tableview)
        self.add_buttons()
        self.setLayout(self.layout)
        self.add_time_edit_row()

    def add_buttons(self):
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignTop)
        self.button_layout.setSpacing(0)
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_time_edit_row)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_selected_time_edit_row)
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.delete_button)
        self.layout.addLayout(self.button_layout)

    def add_time_edit_row(self) -> None:
        if len(self.rows) >= 10:
            return
        new_row = TimeEditRow()
        new_row.time_edit1.setTime(QTime.currentTime())
        new_row.time_edit2.setTime(QTime.currentTime())
        self.rows.append(new_row)
        # Insert at the bottom
        self.layout.insertWidget(len(self.layout) - 1, new_row)
        self.update_labels()

    def delete_selected_time_edit_row(self) -> None:
        for row in self.rows:
            if row.time_edit1.hasFocus() or row.time_edit2.hasFocus():
                self.rows.remove(row)
                row.deleteLater()
        self.update_labels()

    def update_labels(self) -> None:
        for i, row in enumerate(self.rows):
            row.position_label.setText(str(i + 1) + ".")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimespanEditor()
    window.setWindowTitle("Time Edit Row App")
    window.show()
    sys.exit(app.exec_())
