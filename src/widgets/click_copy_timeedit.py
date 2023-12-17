from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtCore import QEvent, QObject, Qt
from PyQt5.QtWidgets import QTimeEdit, qApp, QApplication


class ClickCopyTimeedit(QTimeEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.installEventFilter(self)

    def eventFilter(self, a0: QObject | None, event: QEvent | None) -> bool:
        # print(event.type())
        # print(event.button() )
        if event.type() == QEvent.MouseButtonPress: 
            print("rb")
            self.copyTimeToClipboard()
            return

        return super().eventFilter(a0, event)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        print(event)
        return super().mousePressEvent(event)

def copyTimeToClipboard(self):
        time = self.time()
        clipboard = QApplication.clipboard()
        clipboard.setText(time.toString(Qt.ISODate))
