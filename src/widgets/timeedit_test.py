import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QApplication,
    QTableView,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QTimeEdit,
)


class TimeEditModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()

        # Initialize the model with column headers
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["From", "To", "Delete", "Play", " "])

    def add_time_edit_row(self):
        from_time = QTimeEdit()
        to_time = QTimeEdit()
        delete_button = QPushButton("Delete")
        play_button = QPushButton("Play")

        row = self.rowCount()
        self.setItem(row, 0, QStandardItem("From:"))
        # self.setIndexWidget(self.index(row, 1), from_time)
        self.setItem(row, 2, QStandardItem("To:"))
        # self.setIndexWidget(self.index(row, 3), to_time)
        # self.setIndexWidget(self.index(row, 4), delete_button)
        # self.setIndexWidget(self.index(row, 5), play_button)

        # Connect slots for the buttons
        delete_button.clicked.connect(self.delete_row)
        play_button.clicked.connect(self.toggle_play_pause)

    def delete_row(self):
        button = self.sender()
        if button:
            index = self.indexAt(button.pos())
            if index.isValid():
                self.removeRow(index.row())

    def toggle_play_pause(self):
        button = self.sender()
        if button:
            if button.text() == "Play":
                button.setText("Pause")
            else:
                button.setText("Play")


class TimeEditTableView(QTableWidget):
    def __init__(self, model):
        super().__init__()
        self.setModel(model)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setColumnWidth(0, 80)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 60)
        self.setColumnWidth(3, 60)
        self.setColumnWidth(4, 60)


class TimeEditApp(QWidget):
    def __init__(self):
        super().__init__()

        self.model = TimeEditModel()
        self.table_view = TimeEditTableView(self.model)

        add_button = QPushButton("Add Time Edit Row")
        add_button.clicked.connect(self.model.add_time_edit_row)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        layout.addWidget(add_button)

        self.setLayout(layout)
        self.setWindowTitle("Time Edit Example")
        self.setGeometry(100, 100, 600, 400)


def main():
    app = QApplication(sys.argv)
    window = TimeEditApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
