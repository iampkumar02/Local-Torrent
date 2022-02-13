import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# import chat_client as client
import chatroom.chat_client as client
# from main_UI import MainWindow
import GetFiles.filesGUI as filesGUI
import Pvt_Msg.pvt_msgGUI as msg_GUI
from socket import *
# import filesocket
from tqdm import tqdm
import json
import os
import time
import threading

textfont = QFont("Times", 7)
ip_list = ["192.168.1.7"]
username = ["user1"]
myname = []
cnt_file = -1
pause_click = False
thread_kill = False
db_name_chk = []
cancel_click = False


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    file_progress = pyqtSignal(str)
    pvt_msg_progress = pyqtSignal(str)
    download_progress = pyqtSignal(str)

    print("DONOT PRINT THIS")

    def run(self):
        self.conn = client.client
        self.user_name = input("Enter your username: ")
        myname.clear()
        myname.append(self.user_name)
        print("MY_Name: ", myname)
        print("TYpe: ", myname)
        self.conn.send(self.user_name.encode('utf-8'))
        self.receivingFromServer()

    def receivingFromServer(self):
        while True:
            try:
                message = self.conn.recv(1024).decode('utf-8')
                msg = message.split("#")

                if msg[0] == "IP_LIST":
                    ip = msg[1]
                    ip_list.clear()
                    ip_list.append(ip)
                    print("IP_LIST: ", ip_list)

                elif msg[0] == "USERNAME":
                    name = msg[1]
                    username.clear()
                    username.append(name)
                    print("USER_LIST: ", username)

                elif msg[0] == "FILE_LIST":
                    print("Getting file list from server")
                    self.file_progress.emit(msg[1])

                elif msg[0] == "PVT_MSG":
                    self.pvt_msg_progress.emit(msg[1])

                elif msg[0] == "DOWNLOAD_PORT":
                    print("Connecting to downloading port: ", msg[1])
                    print("Sending...")
                    self.download_progress.emit(msg[1])

                elif msg[0] == "DATABASECHECK":
                    # print("Inside DATABASECHECK: ", msg[1])
                    db_name_chk.clear()
                    db_name_chk.append(msg[1])

                elif not msg[0] == "username?":
                    self.progress.emit(message)

            except Exception as e:
                print('Error!', e)
                self.conn.close()
                self.finished.emit()
                break


class ChatRoom(QWidget):

    def __init__(self):
        super(ChatRoom, self).__init__()
        self.cntToResetTable = 0
        self.initUI()

    def initUI(self):

        self.chatlayout = QVBoxLayout()
        self.topchatlayout = QVBoxLayout()
        self.bottomchatlayout = QHBoxLayout()

        self.chatlayout.setContentsMargins(0, 24, 10, 0)
        self.topchatlayout.setContentsMargins(0, 0, 0, 0)
        self.bottomchatlayout.setContentsMargins(0, 0, 0, 0)
        self.chatlayout.addLayout(self.topchatlayout, 90)
        self.chatlayout.addLayout(self.bottomchatlayout, 10)

        chatlabel = QLabel("Group Chat")
        chatlabel.setFont(QFont("Times", 10))
        chatlabel.setAlignment(Qt.AlignCenter)
        chatlabel.setStyleSheet("background: orange;font-weight: bold;")
        self.topchatlayout.addWidget(chatlabel, 12)

        self.chatWidget = QTextEdit()
        self.chatWidget.setReadOnly(True)
        self.chatWidget.setStyleSheet("background: white")
        self.chatWidget.setFont(textfont)
        self.topchatlayout.addWidget(self.chatWidget, 88)

        self.chattext = QLineEdit()
        self.chattext.setPlaceholderText("Type your Message")
        self.bottomchatlayout.addWidget(self.chattext)

        chatbtn = QPushButton("Send")
        chatbtn.clicked.connect(self.onClickedSend)
        self.bottomchatlayout.addWidget(chatbtn)

        # -------------------Pvt Msg Layout--------------------

        self.pvt_msg_obj = msg_GUI.PvtMessage()
        self.chatbtn1 = self.pvt_msg_obj.chatbtn
        self.chattext1 = self.pvt_msg_obj.chattext
        self.chatlabel1 = self.pvt_msg_obj.chatlabel

        self.chatbtn1.clicked.connect(self.onClickedSend1)
        self.chatWidget1 = self.pvt_msg_obj.chatWidget

        self.setLayout(self.chatlayout)
        self.chatThread()

    def chatThread(self):
        # --------------Create worker thread---------------
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.appendMessage)
        self.worker.file_progress.connect(self.getFiles)
        self.worker.pvt_msg_progress.connect(self.getPvtMessage)
        self.worker.download_progress.connect(self.sendingFileToDownload)
        self.thread.start()

    # Sending file to another user by establishing via another socket(P2P)

    def sendingFileToDownload(self, info):
        upload_file_dir, receiver_name, receiver_dir = info.split("@")
        try:
            user = username[0].split("'")[1::2]
            ip_ls = ip_list[0].split("'")[1::2]
            index = user.index(receiver_name)
            receiver_ip = ip_ls[index]
            print("Receiver IP: ", receiver_ip)
        except Exception as e:
            print("Unable to find receiver: ", e)
        receiver_port = 14000
        try:
            self.down_socket = socket(AF_INET, SOCK_STREAM)
            self.down_socket.connect((receiver_ip, receiver_port))
            print("Connection has been established for sending file!")

            global thread_kill
            global cancel_click
            thread_kill = False
            cancel_click = False


            thread = threading.Thread(target=self.receivingConn, args=())
            thread.start()

            FORMAT = "utf-8"
            user = receiver_name
            self.user = user
            FILENAME = "E:\Computer Network\Local-torrent\server_data\\share.txt"
            self.FILESIZE = os.path.getsize(FILENAME)

            f = open('temp_file.json')
            data = json.load(f)

            c = 0
            for i in data['users']:
                v = i['username']
                if v == user:
                    c = 1
                    break
            if not c:
                j = {"username": user, "count": 0}

                with open('temp_file.json', "r+") as file:
                    file_data = json.load(file)
                    file_data["users"].append(j)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
            try:
                self.down_socket.send(
                    f"{upload_file_dir}@{receiver_dir}".encode("utf-8"))
                print("First Sended!", f"{upload_file_dir}@{receiver_dir}")
            except Exception as e:
                print("First not sended")
            time.sleep(1)
            try:
                # data = self.FILESIZE
                self.down_socket.send(f"{self.FILESIZE}".encode(FORMAT))
                print("Second Sended! ", self.FILESIZE)
            except Exception as e:
                print("Second not sended")
            time.sleep(1)

            """ Data transfer. """
            self.bar = tqdm(range(self.FILESIZE), f"Sending long.txt",
                   unit="B", unit_scale=True, unit_divisor=1024)
            self.packets = self.mainSendingFunc(0)

            print("This is your Sended Packets",self.packets)

        except Exception as e:
            print("Unable to connect receiver: ", e)

    def mainSendingFunc(self, packets):
        global thread_kill
        cnt = 0
        SIZE = 1024
        global pause_click
        global cancel_click
        c=0

        with open("E:\Computer Network\Local-torrent\server_data\share.txt", "r") as f:
            g = open('temp_file.json')
            data = json.load(g)
            v = 0
            for i in data['users']:
                name = i['username']
                if name == self.user:
                    v = i['count']
                    f.seek(v)
                    break

            if packets:
                print("File seeked!!")
                f.seek(packets*1024)

            j = 0
            while j < v/1024:
                j += 1
                self.bar.update(1024)

            g.close()
            cnt1 = 0
            cnt_size = 0
            while True:
                data = f.read(SIZE)

                if not data:
                    break
                cnt += 1
                try:
                    cnt_size += 1

                    if pause_click:
                        return cnt_size
                    if cancel_click:
                        self.down_socket.close()
                        return

                    self.down_socket.send(data.encode("utf-8"))
                    self.bar.update(len(data))
                except:
                    print("\nClient stopped receiving!")
                    cnt -= 1
                    print(f"Total No. of Packets sended: {cnt}")
                    print("Size of file sended now: ", cnt_size/1024)
                    cnt1 = 1
                    cnt = v+(cnt*SIZE)
                    temp_file_fetch(self.user, cnt)
                    sys.exit()
            if not cnt1:
                temp_file_fetch(self.user, 0)
            # print("Size of file sended now: ", cnt_size/1024)
            c=cnt_size
        print("Should not execute on pause!")
        thread_kill = True
        self.down_socket.close()
        return c
        # print(f"\nTotal No. of Packets sended: {cnt}")
        # print("total packets: sended: ", cnt_size)

    def receivingConn(self):
        print("Another Receiving thread while downloading")
        while True:
            global thread_kill
            print("Thread Kill: ", thread_kill)
            if thread_kill:
                print("THread True")
                break
            try:
                print("This except")
                data = self.down_socket.recv(1024).decode("utf-8")
                global pause_click
                global cancel_click
                print("Receiving while downloading: ", data)
                if data == "PAUSEDOWNLOADING":
                    print("Pause EXECUTED")
                    pause_click = True
                elif data == "CANCELDOWNLOADING":
                    cancel_click = True
                else:
                    print("Resume EXECUTED")
                    pause_click = False
                    new_thread = threading.Thread(target=self.anotherSendingFun, args=())
                    new_thread.start()

                    print("Packet: ", self.packets)
            except Exception as e:
                print("Unable to receive Pause/Resume: ", e)
                break

    def anotherSendingFun(self):
        print("Before is your Sended Packets", self.packets)
        self.packets = self.mainSendingFunc(self.packets)
        print("After is your Sended Packets", self.packets)


    # Getting all file list of selected user and displaying on new window

    def getFiles(self, file_items):
        global cnt_file
        cnt_file += 1
        if file_items[0] == "@":
            self.client_name = file_items[1:]
            cnt_file = -1
            self.file_obj = filesGUI.Files()
            self.file_obj.show()
            self.fileTable = self.file_obj.fileTable
            self.downbtn = self.file_obj.downbtn
            self.searchbar = self.file_obj.searchEntry
            self.downbtn.clicked.connect(self.onClickDownBtn)
            self.searchbar.textChanged.connect(self.update_display)
        else:
            file_items = file_items.split("'")[1::2]
            # print(file_items)
            file_dir, file_name, file_size = file_items
            file_ext = file_dir.split(".")
            file_ext = file_ext[-1]

            self.fileTable.setRowCount(cnt_file+1)
            # print(file_dir,file_name,file_size)
            self.fileTable.setItem(cnt_file, 0, QTableWidgetItem(file_name))
            self.fileTable.setItem(
                cnt_file, 1, QTableWidgetItem(file_ext.upper()))
            self.fileTable.setItem(cnt_file, 2, QTableWidgetItem(file_size))

    def update_display(self, text):
        rowCount = self.fileTable.rowCount()
        for row in range(rowCount):
            if text.lower() in self.fileTable.item(row, 0).text().lower():
                # widget.show()
                self.fileTable.showRow(row)
            else:
                self.fileTable.hideRow(row)

    def onClickDownBtn(self):
        self.conn = client.client
        print("Download Button Clicked")
        for item in self.fileTable.selectedItems():
            row = item.row()
            col = item.column()
            print(item.text(), row, col)
            tag = "DOWNLOAD#"
            info = tag+item.text()+"@"+self.client_name
            print("Info: ", info)
            self.conn.send(info.encode("utf-8"))
            print("Sucessfully sended info to server")


# -----------------Private Messaging----------------------------


    def getPvtMessage(self, pvt_msg):
        if pvt_msg[0] == "@":
            print("GUI: Opening Pvt Window")
            self.client_name_col = pvt_msg[1:]
            self.chatlabel1.setText(f"Messaging To: {pvt_msg[1:]}")
            self.pvt_msg_obj.show()
        else:
            print("This is one time")
            self.chatWidget1.append(pvt_msg)

    def onClickedSend1(self):
        send_msg = self.chattext1.text()
        self.chattext1.clear()
        send_msg = f"PVT_MSG#{self.client_name_col}@"+send_msg
        print("Sending this msg: ", send_msg)
        self.conn = client.client
        self.conn.send(send_msg.encode("utf-8"))


# -------------- Group Chat-------------------


    def onClickedSend(self):
        send_msg = self.chattext.text()
        self.chattext.clear()
        self.conn = client.client
        self.conn.send(send_msg.encode("utf-8"))

    def appendMessage(self, msg):
        self.chatWidget.append(msg)


def temp_file_fetch(user, cnt):
    with open('temp_file.json', 'r') as g:
        json_data = json.load(g)
        user1 = json_data['users']
        l = len(user1)
        for i in range(0, l):
            name = user1[i]['username']
            if name == user:
                user1[i]['count'] = cnt
                break

        with open('temp_file.json', 'w') as g:
            g.write(json.dumps(json_data, indent=4))
    g.close()


def main():
    app = QApplication(sys.argv)
    ex = ChatRoom()
    ex.resize(500, 350)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
