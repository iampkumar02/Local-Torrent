import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

textfont = QFont("Times", 7)


class SettingsUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(490, 400)
        self.UI()

    def UI(self):
        self.personalInfo()
        self.viewDownloadDir()
        self.setting_Layouts()
        self.listWidgetDetails()

    def listWidgetDetails(self):
        self.list.addItems(["Personal Information", "Downloads"])

    def personalInfo(self):
        pass

    def viewDownloadDir(self):
        pass

    def setting_Layouts(self):
        # creating layouts-------------------
        self.mainlayout = QHBoxLayout()
        self.leftlayout = QVBoxLayout()
        self.rightlayout = QVBoxLayout()
        self.toprightlayout = QVBoxLayout()
        self.bottomrightlayout = QHBoxLayout()

        # add layouts to its main layout-------------
        self.mainlayout.addLayout(self.leftlayout, 40)
        self.mainlayout.addLayout(self.rightlayout, 60)
        self.rightlayout.addLayout(self.toprightlayout)
        self.rightlayout.addLayout(self.bottomrightlayout)

        # creating widgets to sub-layouts------------
        self.list = QListWidget()
        self.list.setFont(textfont)
        
        self.top_right_widget = QTextEdit()

        self.ok_btn = QPushButton("OK")
        self.ok_btn.setFont(textfont)
        self.ok_btn.setIcon(QIcon("images/ok.jpg"))
        self.ok_btn.setIconSize(QSize(12, 12))

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(textfont)
        self.cancel_btn.setIcon(QIcon("images/cancel.png"))
        self.cancel_btn.setIconSize(QSize(8, 8))
        
        self.bottomrightlayout.setContentsMargins(60, 0, 60, 0)
        # add widgets to sub-layouts-----------------
        self.leftlayout.addWidget(self.list)
        self.toprightlayout.addWidget(self.top_right_widget)
        self.bottomrightlayout.addWidget(self.ok_btn)
        self.bottomrightlayout.addWidget(self.cancel_btn)

        # set layout to main layout------------------
        self.setLayout(self.mainlayout)


if __name__ == "__main__":
    win = QApplication(sys.argv)
    main = SettingsUI()
    main.setGeometry(230, 60, 490, 400)
    main.show()
    win.exec()
