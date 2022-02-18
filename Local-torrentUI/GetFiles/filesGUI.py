import sys
import os
# from PySide6 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
textfont = QFont("Times", 7)


class Files(QWidget):

    def __init__(self):
        super(Files, self).__init__()
        print("Inside Files Class!")
        self.initUI()

    def initUI(self):
        self.resize(550, 400)
        self.setWindowTitle("Files")
        # self.fetchFiles()
        self.file_table()
        self.file_layout()

    def file_table(self):
        self.fileTable = QTableWidget()
        self.fileTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.fileTable.setFont(textfont)
        self.fileTable.setColumnCount(3)
        self.fileTable.setHorizontalHeaderItem(
            0, QTableWidgetItem("File name"))
        self.fileTable.setHorizontalHeaderItem(
            1, QTableWidgetItem("File Extension"))
        self.fileTable.setHorizontalHeaderItem(2, QTableWidgetItem("Size"))

    def file_layout(self):
        self.filemainLayout = QVBoxLayout()
        self.fileSearchLayout = QHBoxLayout()
        self.allFilesLayout = QVBoxLayout()
        self.allFilesLayout.setContentsMargins(0, 0, 0, 0)

        self.downbtn = QPushButton("Download")
        self.downbtn.setStyleSheet("color:green;font-weight: bold;")
        self.searchGroupLayout = QGroupBox("Search Files")
        self.searchGroupLayout.setFont(QFont("Times", 8))
        self.searchGroupLayout.setStyleSheet("font-weight: bold")

        self.filemainLayout.addWidget(self.searchGroupLayout)
        self.filemainLayout.addLayout(self.allFilesLayout)

        self.setLayout(self.filemainLayout)

        # Making searchbar for search files from the available list--------------
        self.searchEntry = QLineEdit()
        self.searchEntry.setStyleSheet("font-weight: normal")
        # self.searchBtn = QPushButton("Search")
        # self.searchBtn.setStyleSheet("font-weight: normal")

        self.fileSearchLayout.addWidget(self.searchEntry)
        # self.fileSearchLayout.addWidget(self.searchBtn)

        self.searchGroupLayout.setLayout(self.fileSearchLayout)

        # --------------Add items in table---------------
        self.allFilesLayout.addWidget(self.fileTable)
        self.allFilesLayout.addWidget(self.downbtn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Files()
    ex.show()
    sys.exit(app.exec_())
