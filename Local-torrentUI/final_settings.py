from ast import Pass
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(560, 450)
        MainWindow.resize(768, 516)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.Personal_info = QtWidgets.QWidget()
        self.Personal_info.setObjectName("Personal_info")
        self.widget = QtWidgets.QWidget(self.Personal_info)
        self.widget.setGeometry(QtCore.QRect(70, 40, 264, 75))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.lineEdit.hide()

        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_5 = QtWidgets.QPushButton(self.widget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_9 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_5.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_5.addWidget(self.label_10)

        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.Personal_info, "")

        self.Downloads = QtWidgets.QWidget()
        self.Downloads.setObjectName("Downloads")

        self.widget1 = QtWidgets.QWidget(self.Downloads)
        self.widget1.setGeometry(QtCore.QRect(53, 42, 351, 25))
        self.widget1.setObjectName("widget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_15 = QtWidgets.QLabel(self.widget1)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 0, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 0, 3, 1, 1)
        self.tabWidget.addTab(self.Downloads, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 768, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Settings"))

        self.label.setText(_translate("MainWindow", "Name:"))
        self.label_2.setText(_translate("MainWindow", "Prashant "))
        self.pushButton.setText(_translate("MainWindow", "Change"))
        self.pushButton_2.setText(_translate("MainWindow", "Save"))
        self.pushButton_5.setText(_translate("MainWindow", "Cancel"))
        self.label_7.setText(_translate("MainWindow", "Upload_amount:"))
        self.label_8.setText(_translate("MainWindow", "400MB"))
        self.label_9.setText(_translate("MainWindow", "Download_amount:"))
        self.label_10.setText(_translate("MainWindow", "300MB"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Personal_info), _translate("MainWindow", "Personal_info"))
        self.label_3.setText(_translate("MainWindow", "Directory:"))
        self.label_15.setText(_translate("MainWindow", "Choosen Directory"))
        self.pushButton_3.setText(_translate("MainWindow", "Browse"))

        self.pushButton_4.setText(_translate("MainWindow", "Save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Downloads), _translate("MainWindow", "Downloads"))

        self.pushButton_3.clicked.connect(self.pushButton_3_handler)
        self.pushButton_4.clicked.connect(self.pushButton_4_handler)
        self.pushButton.clicked.connect(self.pushButton_handler)
        self.pushButton_5.clicked.connect(self.pushButton_5_handler)
        self.pushButton_2.clicked.connect(self.pushButton_2_handler)

    def pushButton_3_handler(self):
        self.open_dialog_box()

    def open_dialog_box(self):
        Directory_name=QFileDialog.getExistingDirectory()
        self.path=Directory_name
        _translate = QtCore.QCoreApplication.translate
        self.label_15.setText(_translate("MainWindow", self.path))
        self.update()

    def update(self):
        self.label_15.adjustSize()

    def pushButton_4_handler(self):
        print(self.path)

    def pushButton_handler(self):
        self.label_2.hide()
        self.lineEdit.show()
    
    def pushButton_5_handler(self):
        self.lineEdit.hide()
        self.label_2.show()

    def pushButton_2_handler(self):
        self.text = self.lineEdit.text()
        # self.lineEdit.textChanged.connect(self.changeText)
        print(self.text)
        self.label_2.setText(self.text)
        self.label_2.adjustSize()
        self.lineEdit.hide()
        self.label_2.show()
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
