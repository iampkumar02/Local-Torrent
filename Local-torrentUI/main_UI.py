import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import settings_info
import login_typo
# import sockets
import server

textfont = QFont("Times", 7)


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Torrent")
        self.setGeometry(100, 40, 800, 450)
        self.user_cnt = 0
        self.downl_cnt = 0
        # print(self.user_cnt)
        # self.login_obj = login_typo.SettingsUI()
        # self.login_obj.show()
        self.UI()

    def UI(self):
        # calling all functions
        self.menubar()
        self.tabs()
        self.table()
        self.layouts()

    def menubar(self):
        # Menu Bar-------------
        self.mb = self.menuBar()
        self.mb.setFont(textfont)
        self.file = self.mb.addMenu("File")
        self.file.setFont(textfont)
        self.view = self.mb.addMenu("View")
        self.view.setFont(textfont)
        self.windows = self.mb.addMenu("Window")
        self.windows.setFont(textfont)
        self.help = self.mb.addMenu("Help")
        self.help.setFont(textfont)

        # Sub Menu Items-------------
        self.users = QAction("Users", self)
        self.file.addAction(self.users)
        self.users.setIcon(QIcon("images/usersicon.png"))

        if self.user_cnt == 0:
            self.users.triggered.connect(self.onClick_User)

        self.settings = QAction("Settings", self)
        self.file.addAction(self.settings)
        self.settings.setIcon(QIcon("images/settingsicon.png"))
        self.settings.triggered.connect(self.onClickSettings)

        self.exit = QAction("Exit", self)
        self.file.addAction(self.exit)
        self.exit.setIcon(QIcon("images/exiticon.jpg"))
        self.exit.triggered.connect(self.onClickExit)

        self.downloads = QAction("File", self)
        self.view.addAction(self.downloads)
        self.downloads.setIcon(QIcon("images/down.ico"))
        if self.downl_cnt == 0:
            self.downloads.triggered.connect(self.onClick_Downloads)

    def onClick_User(self):
        if self.user_cnt == 0:
            self.onClickUser()

    def onClick_Downloads(self):
        if self.downl_cnt == 0:
            self.onClickDownloads()

    def onClickUser(self):
        # self.tab.removeTab(1)
        self.user_cnt = 1
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(3)
        # self.users_table.setRowCount(1)
        self.users_table.setFont(textfont)

        self.users_table.setShowGrid(False)
        self.users_table.setHorizontalHeaderItem(0, QTableWidgetItem("Name"))
        self.users_table.setHorizontalHeaderItem(1, QTableWidgetItem("Shared"))
        self.users_table.setHorizontalHeaderItem(2, QTableWidgetItem("IP"))

        # print(self.tab.currentIndex())
        # self.tab.tabBarDoubleClicked(0)

        self.tab_user = QWidget()
        self.tab.addTab(self.tab_user, "Users")
        self.tab_user.setLayout(self.eachtablayout)
        self.eachtablayout.setSpacing(0)
        self.eachtablayout.addWidget(self.users_table)
        self.users_table.setItem(0, 0, QTableWidgetItem("username"))

        username = server.users
        ip = server.ip_list
        print(ip)
        # ip=ip[username[0]][0]
        # print(ip)

        if not len(username) == 0:
            for i in (0, len(username)-1):
                # print(username[i])
                self.users_table.setRowCount(i+1)
                self.users_table.setItem(
                    i, 2, QTableWidgetItem(ip[username[i]][0]))
                self.users_table.setItem(i, 0, QTableWidgetItem(username[i]))

    def onClickSettings(self):
        self.setting_obj = settings_info.SettingsUI()
        self.setting_obj.show()

    def onClickDownloads(self):
        self.downl_cnt = 1
        self.tab_user = QWidget()
        self.tab.addTab(self.tab_user, "File list")

    def tabs(self):
        self.tab = QTabWidget()
        self.tab.setFont(textfont)
        self.tab1 = QWidget()
        # self.tab2 = QWidget()
        self.tab.addTab(self.tab1, "Tab 1")
        # self.tab.addTab(self.tab2, "Tab 2")
        self.tab.setTabsClosable(True)
        self.tab.tabsClosable()
        self.tab.setMovable(True)
        self.setCentralWidget(self.tab)
        self.tab.setStyleSheet(
            "border: 0 solid white")

    def table(self):
        self.usertable = QTableWidget()
        self.usertable.setFont(textfont)
        self.usertable.setColumnCount(6)
        self.usertable.setRowCount(6)

        # self.usertable.verticalHeader().hide()
        self.usertable.setShowGrid(False)
        # self.usertable.setStyleSheet(
        #     'QTableView::item {border-bottom: 0.5px solid #d6d9dc;}')

        self.usertable.setHorizontalHeaderItem(0, QTableWidgetItem("File"))
        self.usertable.setHorizontalHeaderItem(1, QTableWidgetItem("Path"))
        self.usertable.setHorizontalHeaderItem(2, QTableWidgetItem("Status"))
        self.usertable.setHorizontalHeaderItem(3, QTableWidgetItem("User"))
        self.usertable.setHorizontalHeaderItem(4, QTableWidgetItem("Speed"))
        self.usertable.setHorizontalHeaderItem(5, QTableWidgetItem("Size"))

        header = self.usertable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Interactive)
        header.setSectionResizeMode(4, QHeaderView.Interactive)
        header.setSectionResizeMode(5, QHeaderView.Interactive)

    def layouts(self):
        # creating layouts----------------------
        self.mainlayout = QVBoxLayout()
        self.eachtablayout = QVBoxLayout()
        self.bottomlayout = QVBoxLayout()

        self.mainlayout.addLayout(self.bottomlayout, 40)
        self.mainlayout.setContentsMargins(0, 280, 0, 0)
        self.mainlayout.setSpacing(0)
        self.eachtablayout.setSpacing(0)
        # self.list = QListWidget()
        # self.list.setFont(textfont)
        # self.list.addItem("List")

        # adding widgets in layouts------------------
        self.bottomlayout.addWidget(self.usertable)

        # set layouts inside Tab---------------------
        self.tab1.setLayout(self.eachtablayout)
        self.tab.setLayout(self.mainlayout)

    def onClickExit(self):
        mbox = QMessageBox.question(
            self, "Warning", "Are you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            sys.exit()
        else:
            pass


if __name__ == "__main__":
    win = QApplication(sys.argv)
    main = Main()
    
    main.show()
    win.exec()
