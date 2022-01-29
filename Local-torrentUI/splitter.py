import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Splitter(QWidget):

    def __init__(self):
        super(Splitter, self).__init__()
        # print("Called init")
        self.initUI()

    def initUI(self):
        # print("Inside initUI")

        hbox = QHBoxLayout(self)
        self.x=10
        self.topright = QWidget()
        self.topleft = QWidget()
        self.bottom = QWidget()
        # self.topleft.setStyleSheet("background:pink")
        # self.bottom.setStyleSheet("background:brown")

        splitter1 = QSplitter(Qt.Horizontal)
        # self.topright.setStyleSheet("background:orange")
        splitter1.addWidget(self.topleft)
        splitter1.addWidget(self.topright)
        splitter1.setSizes([70, 30])

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.bottom)
        splitter2.setSizes([70, 30])

        hbox.addWidget(splitter2)
        # to remove outside margins
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        self.setLayout(hbox)


def main():
    app = QApplication(sys.argv)
    ex = Splitter()
    ex.resize(550, 400)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
