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
        # self.personalInfo()
        # self.viewDownloadDir()
        self.setting_Layouts()
        self.listWidgetDetails()

    def listWidgetDetails(self):
        self.list.addItems(["Personal Information", "Directories"])
        self.list.itemClicked.connect(self.onClicked)

    def onClicked(self, item):
        if item.text() == "Personal Information":
            self.onClickPersonalInfo()
        if item.text() == "Directories":
            self.onClickDownloads()

    # on clicking personalInfo---------------------------------

    def onClickPersonalInfo(self):
        self.save_btn.setEnabled(True)
        cnt = self.toprightlayout.count()
        print(cnt)
        if cnt >= 2:
            try:
                for i in range(self.insidetopright.count()):
                    # self.insidetopright.itemAt(i).widget().removeItem()
                    layout_item = self.insidetopright.itemAt(i)
                    self.insidetopright.removeItem(layout_item)

            except Exception as e:
                print("Error!", e)

        cnt = self.toprightlayout.count()
        print(cnt)
        if cnt >= 2:
            try:
                for i in range(self.dirlayout.count()):
                    layout_item = self.dirlayout.itemAt(i)
                    self.dirlayout.removeItem(layout_item)
                    # self.dirlayout.itemAt(i).widget().deleteLater()
            except Exception as e:
                print("Error!", e)

        # ----------------------------------------------------------

        self.top_right_widget.hide()
        self.insidetopright = QHBoxLayout()
        # creating buttons and labels
        self.lineEdit = QLineEdit()
        self.lineEdit.hide()
        self.lineEdit.setFont(textfont)
        self.label_username = QLabel("Username:")
        self.username = QLabel("Klaus Mikaelson")
        self.user = self.username.text()
        self.change_btn = QPushButton("Change")
        self.label_username.setFont(textfont)
        self.username.setFont(textfont)
        self.username.setStyleSheet("background:white")
        self.change_btn.setFont(textfont)

        # calling functions on clicking buttons
        self.change_btn.clicked.connect(self.change_btn_clicked)
        self.cancel_btn.clicked.connect(self.cancel_btn_clicked)
        self.save_btn.clicked.connect(self.save_btn_clicked)

        # add widgets to layout
        self.insidetopright.addWidget(self.label_username)
        self.insidetopright.addWidget(self.lineEdit)
        self.insidetopright.addWidget(self.username)
        self.insidetopright.addWidget(self.change_btn)
        self.insidetopright.setContentsMargins(10, 10, 0, 320)

        self.toprightlayout.addLayout(self.insidetopright)

    def change_btn_clicked(self):
        self.username.hide()
        self.lineEdit.show()
        self.text = self.username.text()
        self.lineEdit.insert(self.text)

    def cancel_btn_clicked(self):
        self.lineEdit.clear()
        self.lineEdit.hide()
        self.username.show()

    def save_btn_clicked(self):
        self.text = self.lineEdit.text()
        print(self.text)
        self.username.setText(self.text)
        self.username.adjustSize()
        self.lineEdit.hide()
        self.username.show()
        self.lineEdit.clear()
        if self.text == "":
            self.username.setText(self.user)

    # On click Directories-----------------------------------------

    def onClickDownloads(self):
        self.top_right_widget.hide()
        cnt = self.toprightlayout.count()
        print(cnt)
        if cnt >= 2:
            try:
                for i in range(self.insidetopright.count()):
                    # self.insidetopright.itemAt(i).widget().removeItem()
                    layout_item = self.insidetopright.itemAt(i)
                    self.insidetopright.removeItem(layout_item)

            except Exception as e:
                print("Error!", e)

        cnt = self.toprightlayout.count()
        print(cnt)
        if cnt >= 2:
            try:
                for i in range(self.dirlayout.count()):
                    layout_item = self.dirlayout.itemAt(i)
                    self.dirlayout.removeItem(layout_item)
                    # self.dirlayout.itemAt(i).widget().deleteLater()
            except Exception as e:
                print("Error!", e)

        self.save_btn.setEnabled(False)

        self.dirlayout = QFormLayout()

        self.down_label = QLabel("Download directory")
        self.down_label.setFont(textfont)
        self.down_label.setStyleSheet("font-weight: bold")
        # self.down_label.setFont(QFont.setBold(True))
        self.choose_down = QLabel("Choose directory")
        self.choose_down.setFont(textfont)
        self.browse_down = QPushButton("Browse")
        self.browse_down.setFont(textfont)
        self.browse_down.clicked.connect(self.onClickBrowseDown)

        self.upload_label = QLabel("Upload directory")
        self.upload_label.setFont(textfont)
        self.upload_label.setStyleSheet("font-weight: bold")
        self.choose_upload = QLabel("Choose directory")
        self.choose_upload.setFont(textfont)
        self.browse_upload = QPushButton("Browse")
        self.browse_upload.setFont(textfont)
        self.browse_upload.clicked.connect(self.onClickBrowseUpload)

        self.dirlayout.addRow(self.down_label)
        self.dirlayout.addRow(self.browse_down, self.choose_down)
        self.dirlayout.addRow(self.upload_label)
        self.dirlayout.addRow(self.browse_upload, self.choose_upload)
        self.toprightlayout.addLayout(self.dirlayout)

    def onClickBrowseDown(self):
        Directory_name = QFileDialog.getExistingDirectory()
        self.down_path = Directory_name
        self.choose_down.setText(self.down_path)
        print(self.down_path)
        if not (self.choose_down.text() == "Choose directory" or self.choose_upload.text() == "Choose directory"):
            self.save_btn.setEnabled(True)

    def onClickBrowseUpload(self):
        Directory_name = QFileDialog.getExistingDirectory()
        self.upload_path = Directory_name
        self.choose_upload.setText(self.upload_path)
        print(self.upload_path)
        if not (self.choose_down.text() == "Choose directory" or self.choose_upload.text() == "Choose directory"):
            self.save_btn.setEnabled(True)
            print(self.save_btn.isEnabled())

    def closeEvent(self, event):
        if self.save_btn.isEnabled()==True and self.username.text()!="":
            event.accept()
        else:
            reply = QMessageBox.information(
                self, "Warning", "Please, Complete")
            event.ignore()

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

        self.top_right_widget = QWidget()
        self.top_right_widget.setStyleSheet("background:white")

        self.save_btn = QPushButton("Save")
        self.save_btn.setFont(textfont)
        self.save_btn.setIcon(QIcon("images/save.jpg"))
        self.save_btn.setIconSize(QSize(12, 12))
        self.save_btn.setStyleSheet("background:white")

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(textfont)
        self.cancel_btn.setIcon(QIcon("images/cancel.png"))
        self.cancel_btn.setIconSize(QSize(8, 8))
        self.cancel_btn.setStyleSheet("background:white")

        self.bottomrightlayout.setContentsMargins(60, 0, 60, 0)
        # add widgets to sub-layouts-----------------
        self.leftlayout.addWidget(self.list)
        self.toprightlayout.addWidget(self.top_right_widget)
        self.bottomrightlayout.addWidget(self.save_btn)
        self.bottomrightlayout.addWidget(self.cancel_btn)

        # set layout to main layout------------------
        self.setLayout(self.mainlayout)


if __name__ == "__main__":
    win = QApplication(sys.argv)
    main = SettingsUI()
    main.setGeometry(230, 60, 490, 400)
    main.show()
    win.exec()
