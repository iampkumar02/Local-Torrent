import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainWindow(QWidget):
    sig = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Main")
        self.layout = QVBoxLayout()
        self.text = QTextEdit()
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)

        self.text.textChanged.connect(self.onChange)

    def onChange(self):
        self.sig.emit(self.text.toPlainText())


class SubWindow(QWidget):

    def __init__(self, connect_target: MainWindow):
        super(SubWindow, self).__init__()
        self.setWindowTitle("Sub")
        self.layout = QVBoxLayout()
        self.text = QPlainTextEdit()
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)

        connect_target.sig.connect(self.onSignal)

    def onSignal(self, text):
        self.text.insertPlainText(text + '\r\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window_sub = SubWindow(window)
    window_sub.show()
    sys.exit(app.exec_())