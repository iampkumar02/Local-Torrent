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
        self.fetchFiles()
        self.file_layout()

    def file_layout(self):
        self.mainlayout = QVBoxLayout()
        # self.search=QWidget()

    def fetchFiles(self):
        formats = ['.jpg', '.jpeg', '.txt']
        self.file_list = []
        self.extension_list = []
        self.file_dir_list = []

        for path, subfolders, files in os.walk(r'E:\CP'):
            # print(path)
            for file in files:
                filename, extension = os.path.splitext(file)

                if (extension.lower() in formats):
                    self.file_list.append(filename)
                    self.extension_list.append(extension)
                    f = os.path.join(path, file)
                    self.file_dir_list.append(f)
                    # print(f)
        # print(self.file_dir_list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Files()
    ex.show()
    sys.exit(app.exec_())
