import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import splitter
import settings_info
import server
import chatroom.GUI as GUI
textfont = QFont("Times", 7)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # self.resize(550, 400)
        self.setWindowTitle("Local Torrent")
        self.setGeometry(100, 40, 800, 450)

        self.user_cnt = 0
        self.downl_cnt = 0
        self.UI()

    def UI(self):
        # calling all functions
        self.menubar()
        self.tabs()
        # self.table()
        self.layouts()

    # Creating Tab Widget
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
        # self.tab.setContentsMargins(0, 0, 0, 0)
        # self.tab.setStyleSheet(
        #     "border: 0 solid white")

# Giving layouts to the application

# QWidget --> HBox --> Splitter(imort QWidget --> HBox) -->
# Splitter(HBox) --> (HBox having 3 QWidgets --> (topright,topleft,bottom))

# topleft(QWidget) --> (VBox having tab Widget)

# topright(QWidget) --> VBox --> ChatRoom(import QWidget --> VBox)
# ChatRoom(VBox) --> (VBox (contains 2 Widgets),HBox (contains 2 Widgets))
    def layouts(self):
        mainWidget = QWidget()
        self.splitter_obj = splitter.Splitter()
        hbox = QHBoxLayout()
        y=self.splitter_obj.x
        print(y)
        # hbox.setSpacing(0)
        self.topleft = self.splitter_obj.topleft
        self.topright = self.splitter_obj.topright
        self.bottom = self.splitter_obj.bottom

        hbox.addWidget(self.splitter_obj)
        mainWidget.setLayout(hbox)

        # to remove outside margins
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(mainWidget)

        # Creating layouts
        topleftlayout = QVBoxLayout()
        topleftlayout.setContentsMargins(0, 0, 0, 0)
        self.topleft.setLayout(topleftlayout)

        self.chat_obj = GUI.ChatRoom()

        toprightlayout = QVBoxLayout()
        toprightlayout.setContentsMargins(0, 0, 0, 0)
        toprightlayout.addWidget(self.chat_obj)
        self.topright.setLayout(toprightlayout)

        bottomlayout = QVBoxLayout()
        bottomlayout.setContentsMargins(0, 0, 0, 0)
        self.bottom.setLayout(bottomlayout)

        # adding widget to three layouts
        topleftlayout.addWidget(self.tab)

        # chatlabel = QLabel("Group Chat")
        # chatlabel.setFont(QFont("Times", 10))
        # chatlabel.setAlignment(Qt.AlignCenter)
        # chatlabel.setStyleSheet("background: orange;font-weight: bold;")
        # toprightlayout.addWidget(chatlabel, 10)
        # chatWiget = QWidget()
        # toprightlayout.addWidget(chatWiget, 80)
        # chatWiget.setStyleSheet("background: white")
        # chattext = QLineEdit()
        # toprightlayout.addWidget(chattext, 10)
        # chattext.setPlaceholderText("Type your Message")
        # toprightlayout.setContentsMargins(0, 24, 0, 0)

        loglabel = QLabel("Connection logs")
        loglabel.setFont(QFont("Times", 8))
        loglabel.setAlignment(Qt.AlignCenter)
        loglabel.setStyleSheet("font-weight: bold;")
        bottomlayout.addWidget(loglabel, 7)
        logcontent = QWidget()
        logcontent.setStyleSheet("background: white;")
        bottomlayout.addWidget(logcontent, 93)

    # ---------------------------------------------------------------------------------

    def onClick_User(self):
        if self.user_cnt == 0:
            self.onClickUser()

    def onClick_Downloads(self):
        if self.downl_cnt == 0:
            self.onClickDownloads()

    def onClickUser(self):
        # self.tab.removeTab(1)
        self.user_cnt = 1
        userslayout = QVBoxLayout()

        self.users_table = QTableWidget()

        self.user_search = QLineEdit()
        self.user_search.setPlaceholderText("Search user")
        self.users_table.setStyleSheet("background:white")
        self.users_table.setColumnCount(5)
        # self.users_table.setRowCount(1)

        self.users_table.setShowGrid(False)
        self.users_table.setHorizontalHeaderItem(0, QTableWidgetItem("Name"))
        self.users_table.setHorizontalHeaderItem(1, QTableWidgetItem("Shared"))
        self.users_table.setHorizontalHeaderItem(2, QTableWidgetItem("IP"))
        self.users_table.setHorizontalHeaderItem(
            3, QTableWidgetItem("Pvt. Message"))
        self.users_table.setHorizontalHeaderItem(
            4, QTableWidgetItem("Get File"))

        self.users_table.setFont(textfont)
        # print(self.tab.currentIndex())
        # self.tab.tabBarDoubleClicked(0)

        self.tab_user = QWidget()
        self.tab.addTab(self.tab_user, "Users")
        self.tab_user.setLayout(userslayout)
        userslayout.setContentsMargins(5, 0, 0, 0)
        userslayout.addWidget(self.users_table)
        userslayout.addWidget(self.user_search)
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
        self.tab.addTab(self.tab_user, "Downloads")


# -------------------------Menu-Bar----------------------------------------------------


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

        self.downloads = QAction("Downloads", self)
        self.view.addAction(self.downloads)
        self.downloads.setIcon(QIcon("images/down.ico"))
        if self.downl_cnt == 0:
            self.downloads.triggered.connect(self.onClick_Downloads)

    def onClickExit(self):
        mbox = QMessageBox.question(
            self, "Warning", "Are you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            sys.exit()
        else:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
