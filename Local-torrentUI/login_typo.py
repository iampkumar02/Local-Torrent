import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import main_UI

textfont = QFont("Times", 7)


class SettingsUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Settings")
        self.setFixedSize(490, 400)
        self.UI()
        self.main_obj = main_UI.Main()
        self.main_obj.show()

    def UI(self):
        self.setting_Layouts()
        self.listWidgetDetails()

    def listWidgetDetails(self):
        self.list.addItems(["Personal Information", "Directories"])
        self.list.itemClicked.connect(self.onClicked)

        # ---------------------Personal Info-------------------------------
        self.insidetopright = QFormLayout()
        # creating buttons and labels
        self.lineEdit = QLineEdit()
        self.lineEdit.hide()
        self.lineEdit.setFont(textfont)
        self.label_username = QLabel("Username")
        self.label_username.setStyleSheet("font-weight: bold")
        self.username = QLabel("Klaus Mikaelson")
        self.user = self.username.text()
        self.change_btn = QPushButton("Change")
        self.change_btn.setFont(textfont)
        self.save_btn = QPushButton("Save")
        self.save_btn.setFont(textfont)
        self.label_username.setFont(textfont)
        self.username.setFont(textfont)
        self.username.setStyleSheet("background:white")

        # calling functions on clicking buttons
        self.change_btn.clicked.connect(self.change_btn_clicked)
        self.cancel_btn.clicked.connect(self.cancel_btn_clicked)
        self.save_btn.clicked.connect(self.save_btn_clicked)

        # add widgets to layout
        self.insidetopright.addRow(self.label_username)
        self.insidetopright.addWidget(self.lineEdit)
        self.insidetopright.addRow(self.username)
        self.insidetopright.addRow(self.save_btn)
        self.insidetopright.addRow(self.change_btn)

        self.toprightlayout.addLayout(self.insidetopright)

        # Hidding Widgets
        self.label_username.hide()
        self.username.hide()
        self.change_btn.hide()
        self.save_btn.hide()

        # -------------------Downloads------------------------
        self.dirlayout = QFormLayout()

        self.down_label = QLabel("Download directory")
        self.down_label.setFont(textfont)
        self.down_label.setStyleSheet("font-weight: bold")
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

        # Hidding Widgets
        self.upload_label.hide()
        self.choose_upload.hide()
        self.browse_upload.hide()
        self.down_label.hide()
        self.choose_down.hide()
        self.browse_down.hide()

    def onClicked(self, item):
        if item.text() == "Personal Information":
            self.onClickPersonalInfo()
        if item.text() == "Directories":
            self.onClickDownloads()

    # on clicking personalInfo--------------------------------------------

    def onClickPersonalInfo(self):
        # Showing Widgets
        self.top_right_widget.hide()
        self.label_username.show()
        self.lineEdit.show()
        self.change_btn.show()
        self.save_btn.show()
        # Hidding Widgets
        self.upload_label.hide()
        self.choose_upload.hide()
        self.browse_upload.hide()
        self.down_label.hide()
        self.choose_down.hide()
        self.browse_down.hide()

    def change_btn_clicked(self):
        self.save_btn.setEnabled(True)
        self.username.hide()
        self.lineEdit.show()
        self.text = self.username.text()
        self.lineEdit.insert(self.text)

    def cancel_btn_clicked(self):
        self.lineEdit.clear()
        self.lineEdit.hide()
        self.username.show()

    def save_btn_clicked(self):
        self.save_btn.setEnabled(False)
        self.text = self.lineEdit.text()
        if self.text == "":
            reply = QMessageBox.information(
                self, "Information", "Please, Enter the username")
            self.save_btn.setEnabled(True)
        else:
            print(self.text)
            self.username.setText(self.text)
            self.username.adjustSize()
            self.lineEdit.hide()
            self.username.show()
            self.lineEdit.clear()
            self.ok_btn.setEnabled(True)

    # On click Directories--------------------------------------------------

    def onClickDownloads(self):
        # Showing Widgets
        self.top_right_widget.hide()
        self.upload_label.show()
        self.choose_upload.show()
        self.browse_upload.show()
        self.down_label.show()
        self.choose_down.show()
        self.browse_down.show()
        # Hidding Widgets
        self.label_username.hide()
        self.username.hide()
        self.change_btn.hide()
        self.save_btn.hide()
        self.lineEdit.hide()

    def onClickBrowseDown(self):
        Directory_name = QFileDialog.getExistingDirectory()
        self.down_path = Directory_name
        self.choose_down.setText(self.down_path)
        print(self.down_path)

    def onClickBrowseUpload(self):
        Directory_name = QFileDialog.getExistingDirectory()
        self.upload_path = Directory_name
        self.choose_upload.setText(self.upload_path)
        print(self.upload_path)

    def onClickOkButton(self):
        if self.choose_down.text() != "Choose directory" and self.choose_upload.text() != "Choose directory":
            sys.exit()

    def closeEvent(self, event):
        if self.ok_btn.isEnabled() == True and self.choose_down.text() != "Choose directory" and self.choose_upload.text() != "Choose directory":
            event.accept()
        else:
            reply = QMessageBox.information(
                self, "Warning", "Please, Complete")
            event.ignore()

    def setting_Layouts(self):
        # creating layouts
        self.mainlayout = QHBoxLayout()
        self.leftlayout = QVBoxLayout()
        self.rightlayout = QVBoxLayout()
        self.toprightlayout = QVBoxLayout()
        self.bottomrightlayout = QHBoxLayout()

        # add layouts to its main layout
        self.mainlayout.addLayout(self.leftlayout, 40)
        self.mainlayout.addLayout(self.rightlayout, 60)
        self.rightlayout.addLayout(self.toprightlayout)
        self.rightlayout.addLayout(self.bottomrightlayout)

        # creating widgets
        self.list = QListWidget()
        self.list.setFont(textfont)

        self.top_right_widget = QWidget()
        self.top_right_widget.setStyleSheet("background:white")

        self.ok_btn = QPushButton("OK")
        self.ok_btn.setFont(textfont)
        self.ok_btn.setIcon(QIcon("images/save.jpg"))
        self.ok_btn.setIconSize(QSize(12, 12))
        self.ok_btn.setEnabled(False)
        self.ok_btn.setStyleSheet("background:white")
        self.ok_btn.clicked.connect(self.onClickOkButton)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(textfont)
        self.cancel_btn.setIcon(QIcon("images/cancel.png"))
        self.cancel_btn.setIconSize(QSize(8, 8))
        self.cancel_btn.setStyleSheet("background:white")

        # add widgets to sub-layouts
        self.leftlayout.addWidget(self.list)
        self.toprightlayout.addWidget(self.top_right_widget)
        self.bottomrightlayout.addWidget(self.ok_btn)
        self.bottomrightlayout.addWidget(self.cancel_btn)

        # set layout to main layout
        self.setLayout(self.mainlayout)


if __name__ == "__main__":
    win = QApplication(sys.argv)
    main = SettingsUI()
    main.setGeometry(230, 60, 490, 400)
    main.show()
    win.exec()
