import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import splitter
import settings_info
import chatroom.GUI1 as GUI
import chatroom.chat_client as client

from socket import *
from tqdm import tqdm
import json
import os

textfont = QFont("Times", 7)
pause_click = False
cancel_clicked = False

downlpauseconn=[]

class Worker(QThread):

    progress = pyqtSignal()
    createTableRow = pyqtSignal(str, int)
    progressbar = pyqtSignal(int, int, int)
    disablebtn = pyqtSignal()

    def run(self):
        print("inside run fun()")
        # self.file_socket()

    # socket for file transfer

    def file_socket(self):
        global downlpauseconn
        global cancel_clicked
        ip_file = "localhost"
        port_file = 14000
        server_file = socket(AF_INET, SOCK_STREAM)
        server_file.bind((ip_file, port_file))
        server_file.listen()
        while True:
            # hostname_file = gethostname()
            # ip_file = gethostbyname(hostname_file)
            print("Waiting for new connection...")
            file_conn, file_addr = server_file.accept()
            cancel_clicked = False
            downlpauseconn.clear()
            downlpauseconn.append(file_conn)
            self.progress.emit()
            print("Connection established to download")
            self.multi_down(file_conn)

    def multi_down(self, file_conn):
        # receiving data from other peer
        global pause_click
        global cancel_clicked
        main_rec = file_conn.recv(1024).decode("utf-8")
        file_dir, down_dir = main_rec.split("@")
        file_name = file_dir.split("\\")[-1]
        print("First Received file_name and down_dir", main_rec)

        file_data = file_conn.recv(1024).decode('utf-8')
        FILESIZE = int(file_data)
        print("Second Received File Size: ", FILESIZE)

        self.createTableRow.emit(file_name, FILESIZE)

        """ Data transfer """
        bar = tqdm(range(FILESIZE), f"Receiving long.txt",
                   unit="B", unit_scale=True, unit_divisor=1024)
        cnt_size = 0
        with open(f"E:\Computer Network\Local-torrent\client_data\\{file_name}", "w") as f:
            g = open('temp_file.json')
            data = json.load(g)
            v = 0
            for i in data['users']:
                name = i['username']
                if name == "iam":
                    v = i['count']
                    f.seek(v)
                    break
            j = 0
            # while j < v/1024:
            #     j += 1
                # bar.update(1024)


            g.close()
            while True:
                cnt_size += 1
                try:
                    data = file_conn.recv(1024).decode("utf-8")
                except Exception as e:
                    print("Failed to receive packets: ",e)
                    break

                if not data:
                    break
                if cancel_clicked:
                    file_conn.close()
                    return

                f.write(data)
                perc = (cnt_size*1024/FILESIZE)*100
                perc = int(round(perc))

                bar.update(len(data))
                self.progressbar.emit(perc, cnt_size, FILESIZE)

        self.disablebtn.emit()
        print("Total Packets(KB) Received: ",cnt_size)
        print("FILESIZE in bytes: ",FILESIZE)
        print("FILESIZE in KB: ",round(FILESIZE/1024))
        print("FILESIZE in MB: ",round(FILESIZE/(1024*1024)))
        file_conn.close()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Local Torrent")
        self.setGeometry(100, 40, 800, 400)

        self.user_cnt = 0
        self.downl_cnt = 0
        self.no_of_downloads = 0

        self.UI()

    def UI(self):
        # calling all functions
        self.menubar()
        self.tabs()
        self.table()
        self.fileThread()
        self.layouts()

    def fileThread(self):
        # --------------Create worker thread---------------
        self.worker = Worker()
        self.worker.start()
        self.worker.progress.connect(self.onClick_Downloads)
        self.worker.createTableRow.connect(self.createDownloadTableRow)
        self.worker.progressbar.connect(self.changeInProgressBar)
        self.worker.disablebtn.connect(self.disableDownlBtn)

    def disableDownlBtn(self):
        self.pausePlay.setEnabled(False)
        self.pausePlay.setText("Completed")
        self.pausePlay.setStyleSheet("background:#555d50;color:white")
        self.canceldownlbtn.setEnabled(False)
        self.canceldownlbtn.setText("Downloaded")
        self.canceldownlbtn.setStyleSheet("background:#555d50;color:white")

    def changeInProgressBar(self, perc, cnt_size, size):
        item = QTableWidgetItem(f"{round(cnt_size/1024)}/{round(size/(1024*1024))} MB")
        item.setTextAlignment(Qt.AlignCenter)
        self.downl_table.setItem(self.no_of_downloads - 1, 4, item)
        self.pbar.setValue(perc)

    def clickPausePlay(self):
        global pause_click
        global downlpauseconn
        if self.pausePlay.text() == "Pause":
            pause_click = True
            try:
                downlpauseconn[0].send("PAUSEDOWNLOADING".encode("utf-8"))
                self.pausePlay.setText("Resume")
            except Exception as e:
                print("Error on doing Pause: ",e)
            print("\nClicked Pause")
        else:
            try:
                downlpauseconn[0].send("STARTDOWNLOADING".encode("utf-8"))
                self.pausePlay.setText("Pause")
            except Exception as e:
                print("Error on doing Resume: ", e)
            print("\nClicked Resume")

    def clickCancelDownlBtn(self):
        global downlpauseconn
        global cancel_clicked
        try:
            downlpauseconn[0].send("CANCELDOWNLOADING".encode("utf-8"))
            cancel_clicked = True
            self.downl_table.setRowCount(self.no_of_downloads - 1)
            self.no_of_downloads -= 1
        except Exception as e:
            print("Error on doing Pause: ",e)
        print("\nClicked Cancel")

    def createDownloadTableRow(self, fname, size):
        self.pbar = QProgressBar()
        self.pausePlay = QPushButton("Pause")
        self.canceldownlbtn = QPushButton("Cancel")
        print("Buttons Created")
        self.pausePlay.setStyleSheet("background:#6495ed;color:white")
        self.pausePlay.clicked.connect(self.clickPausePlay)
        self.canceldownlbtn.setStyleSheet("background:#a0522d;color:white")
        self.canceldownlbtn.clicked.connect(self.clickCancelDownlBtn)

        self.pbar.setStyleSheet("QProgressBar"
                                "{"
                                "min-height: 7px"
                                "max-height: 7px"
                                "border-radius: 10px"
                                "}")

        self.pbar.setTextVisible(False)
        self.downl_table.setRowCount(self.no_of_downloads+1)
        self.downl_table.setItem(
            self.no_of_downloads, 0, QTableWidgetItem(fname))
        self.downl_table.setCellWidget(self.no_of_downloads, 1,
                                       self.pbar)

        self.downl_table.setCellWidget(self.no_of_downloads, 2,
                                       self.pausePlay)
        self.downl_table.setCellWidget(self.no_of_downloads, 3,
                                       self.canceldownlbtn)

        item = QTableWidgetItem(f"{round(size/(1024*1024))} MB")
        item.setTextAlignment(Qt.AlignCenter)
        self.downl_table.setItem(
            self.no_of_downloads, 4, item)
        # self.downl_table.setItem(
        #     self.no_of_downloads, 5, QTableWidgetItem("Speed"))
        print("Row Added")
        self.no_of_downloads += 1

    def onClickDownloads(self):
        self.downl_cnt = 1
        self.tab_down = QWidget()

        self.downl_table = QTableWidget()
        self.downl_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.downl_table.setStyleSheet("background:white")
        self.downl_table.setColumnCount(5)
        self.downl_table.setShowGrid(False)

        self.downl_table.setHorizontalHeaderItem(
            0, QTableWidgetItem("File Name"))
        self.downl_table.setHorizontalHeaderItem(
            1, QTableWidgetItem("Progress"))
        self.downl_table.setHorizontalHeaderItem(
            2, QTableWidgetItem("Pause/Resume"))
        self.downl_table.setHorizontalHeaderItem(
            3, QTableWidgetItem("Cancel"))
        self.downl_table.setHorizontalHeaderItem(
            4, QTableWidgetItem("Size"))
        # self.downl_table.setHorizontalHeaderItem(
        #     5, QTableWidgetItem("Speed"))

        header = self.downl_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.downl_table.setFont(textfont)
        self.maindownlayout = QVBoxLayout()
        self.maindownlayout.addWidget(self.downl_table)
        self.maindownlayout.setContentsMargins(3, 0, 0, 0)

        self.tab_down.setLayout(self.maindownlayout)

        self.tab.addTab(self.tab_down, "Downloads")

    # Creating Tab Widget

    def tabs(self):
        self.tab = QTabWidget()
        self.tab.setFont(textfont)
        # self.tab1 = QWidget()
        # self.tab2 = QWidget()
        # self.tab.addTab(self.tab1, "Tab 1")
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
        y = self.splitter_obj.x
        # print(y)
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

        # loglabel = QLabel("Connection logs")
        # loglabel.setFont(QFont("Times", 8))
        # loglabel.setAlignment(Qt.AlignCenter)
        # loglabel.setStyleSheet("font-weight: bold;")
        # bottomlayout.addWidget(loglabel, 7)
        logcontent = QWidget()
        logcontent.setStyleSheet("background: white;")
        bottomlayout.addWidget(logcontent, 93)

    # ---------------------------------------------------------------------------------

    def table(self):
        self.users_table = QTableWidget()
        self.users_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.users_table.setStyleSheet("background:white")
        self.users_table.setColumnCount(5)

        self.users_table.setShowGrid(False)
        self.users_table.setHorizontalHeaderItem(0, QTableWidgetItem("Name"))
        self.users_table.setHorizontalHeaderItem(1, QTableWidgetItem("Shared"))
        self.users_table.setHorizontalHeaderItem(2, QTableWidgetItem("IP"))
        self.users_table.setHorizontalHeaderItem(
            3, QTableWidgetItem("Pvt. Message"))
        self.users_table.setHorizontalHeaderItem(
            4, QTableWidgetItem("Get File"))

        self.users_table.setFont(textfont)
        self.users_table.doubleClicked.connect(self.onClickTableBox)
        # self.getFileBtn=QPushButton(self.users_table)
        # self.getFileBtn.setText("GET")
        # self.getFileBtn.setStyleSheet("background-color : #87CEEB")

        # self.getFileBtn.clicked.connect(self.onClickTableBox)

    def onClickTableBox(self):
        self.conn = client.client
        print("Clicked")
        for item in self.users_table.selectedItems():
            row = item.row()
            col = item.column()
            print(row, col)
            if col == 4:
                name = self.users_table.item(row, 0).text()
                self.conn.send(f"FILE_LIST#{name}".encode('utf-8'))
            if col == 3:
                self.client_name_col = self.users_table.item(row, 0).text()
                print("Opening Pvt msg Window")
                self.conn.send(
                    f"PVT_MSG#{self.client_name_col}@".encode('utf-8'))
                print("NOW")

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
        topuserstablelayout = QVBoxLayout()
        topuserstablelayout.setContentsMargins(0, 0, 0, 0)
        # self.users_table = QTableWidget()

        bottomuserstablelayout = QHBoxLayout()
        bottomuserstablelayout.setContentsMargins(0, 0, 0, 0)
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.onClickRefresh)
        self.user_search = QLineEdit()
        self.user_search.textChanged.connect(self.update_display)

        userslayout.addLayout(topuserstablelayout)
        userslayout.addLayout(bottomuserstablelayout)

        self.user_search.setPlaceholderText("Search user")

        self.tab_user = QWidget()
        self.tab.addTab(self.tab_user, "Users")
        self.tab_user.setLayout(userslayout)
        userslayout.setContentsMargins(5, 0, 0, 0)

        topuserstablelayout.addWidget(self.users_table)
        bottomuserstablelayout.addWidget(self.user_search)
        bottomuserstablelayout.addWidget(self.refresh_btn)

        self.myname = GUI.myname

        username = GUI.username
        ip = GUI.ip_list

        username = username[0]
        ip = ip[0]

        username = username.split("'")[1::2]
        ip = ip.split("'")[1::2]

        # print("Before myname:",self.myname[0])
        # print("Before name:",username)
        # print("Before ip:",ip)

        index_myname = username.index(self.myname[0])
        username.remove(self.myname[0])
        ip.pop(index_myname)

        print("Main ", username)
        print("Main ", ip)

        if not len(username) == 0:
            for i in (0, len(username)-1):
                # print(username[i])
                self.users_table.setRowCount(i+1)
                self.users_table.setItem(
                    i, 2, QTableWidgetItem(ip[i]))
                self.users_table.setItem(i, 0, QTableWidgetItem(username[i]))

                item1 = QTableWidgetItem("GET")
                item1.setBackground(QColor("#87CEEB"))
                item1.setTextAlignment(Qt.AlignCenter)
                item1.setFont(QFont("Times", 8))
                self.users_table.setItem(i, 4, item1)

                item2 = QTableWidgetItem("MESSAGE")
                item2.setBackground(QColor("#f9aa33"))
                item2.setTextAlignment(Qt.AlignCenter)
                item2.setFont(QFont("Times", 8))
                self.users_table.setItem(i, 3, item2)

    def update_display(self, text):
        rowCount = self.users_table.rowCount()
        for row in range(rowCount):
            if text.lower() in self.users_table.item(row, 0).text().lower():
                self.users_table.showRow(row)
            else:
                self.users_table.hideRow(row)

    def onClickRefresh(self):
        self.users_table.setRowCount(0)

        username = GUI.username
        ip = GUI.ip_list

        username = username[0]
        ip = ip[0]
        username = username.split("'")[1::2]
        ip = ip.split("'")[1::2]

        index_myname = username.index(self.myname[0])
        username.remove(self.myname[0])
        ip.pop(index_myname)

        if not len(username) == 0:
            for i in (0, len(username)-1):
                # print(username[i])
                self.users_table.setRowCount(i+1)
                self.users_table.setItem(
                    i, 2, QTableWidgetItem(ip[i]))
                self.users_table.setItem(i, 0, QTableWidgetItem(username[i]))

                item1 = QTableWidgetItem("GET")
                item1.setBackground(QColor("#87CEEB"))
                item1.setTextAlignment(Qt.AlignCenter)
                item1.setFont(QFont("Times", 8))
                self.users_table.setItem(i, 4, item1)

                item2 = QTableWidgetItem("MESSAGE")
                item2.setBackground(QColor("#f9aa33"))
                item2.setTextAlignment(Qt.AlignCenter)
                item2.setFont(QFont("Times", 8))
                self.users_table.setItem(i, 3, item2)

        # self.users_table.hideRow(0)

    def onClickSettings(self):
        self.setting_obj = settings_info.SettingsUI()
        self.setting_obj.show()


# -------------------------Menu-Bar----------------------------------------------------

    def menubar(self):
        # Menu Bar-------------
        self.mb = self.menuBar()
        self.mb.setFont(textfont)
        self.file = self.mb.addMenu("File")
        self.file.setFont(textfont)
        self.view = self.mb.addMenu("View")
        self.view.setFont(textfont)

        # Sub Menu Items-------------
        self.users = QAction("Users", self)
        self.file.addAction(self.users)
        # self.users.setIcon(QIcon("images/usersicon.png"))
        path = os.getcwd()
        parent = os.path.dirname(path)
        # print(dirname)
        self.users.setIcon(
            QIcon(f"{parent}\\images\\usersicon.png"))

        if self.user_cnt == 0:
            self.users.triggered.connect(self.onClick_User)

        self.settings = QAction("Settings", self)
        self.file.addAction(self.settings)
        # self.settings.setIcon(QIcon("images/settingsicon.png"))
        self.settings.setIcon(
            QIcon(f"{parent}\images\settingsicon.png"))
        self.settings.triggered.connect(self.onClickSettings)

        self.exit = QAction("Exit", self)
        self.file.addAction(self.exit)
        self.exit.setIcon(
            QIcon(f"{parent}\images\exiticon.jpg"))
        self.exit.triggered.connect(self.onClickExit)

        self.downloads = QAction("Downloads", self)
        self.view.addAction(self.downloads)
        self.downloads.setIcon(
            QIcon(f"{parent}\images\down.ico"))
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
