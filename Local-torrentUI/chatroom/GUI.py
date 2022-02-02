import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# import chat_client as client
import chatroom.chat_client as client
# from main_UI import MainWindow
import GetFiles.filesGUI as filesGUI
import Pvt_Msg.pvt_msgGUI as msg_GUI

textfont = QFont("Times", 7)
ip_list=["user1"]
username=["192.168.1.7"]
myname=[]


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    progress_file = pyqtSignal()
    progress_pvt_msg = pyqtSignal(str)
    print("DONOT PRINT THIS")

    def run(self):
        self.conn = client.client
        self.user_name=input("Enter your username: ")
        myname.clear()
        myname.append(self.user_name)
        self.conn.send(self.user_name.encode('utf-8'))
        self.receivingFromServer()

    def receivingFromServer(self):
        while True:
            try:
                message = self.conn.recv(1024).decode('utf-8')
                msg=message.split("#")

                if msg[0] == "IP_LIST":
                    ip=msg[1]
                    ip_list.clear()
                    ip_list.append(ip)
                    print("IP_LIST: ",ip_list)

                elif msg[0] == "USERNAME":
                    name = msg[1]
                    username.clear()
                    username.append(name)
                    print("USER_LIST: ", username)

                elif msg[0] == "FILE_LIST":
                    print("Getting file list from server")
                    self.progress_file.emit()
                
                elif msg[0] == "PVT_MSG":
                    self.progress_pvt_msg.emit(msg[1])

                elif not msg[0] == "username?":
                    self.progress.emit(message)

            except Exception as e:
                print('Error!',e)
                self.conn.close()
                self.finished.emit()
                break

class ChatRoom(QWidget):

    def __init__(self):
        super(ChatRoom, self).__init__()
        self.cntToResetTable=0
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
        self.topchatlayout.addWidget(chatlabel,12)

        self.chatWidget = QTextEdit()
        self.chatWidget.setReadOnly(True)
        self.chatWidget.setStyleSheet("background: white")
        self.chatWidget.setFont(textfont)
        self.topchatlayout.addWidget(self.chatWidget,88)

        self.chattext = QLineEdit()
        self.chattext.setPlaceholderText("Type your Message")
        self.bottomchatlayout.addWidget(self.chattext)

        chatbtn=QPushButton("Send")
        chatbtn.clicked.connect(self.onClickedSend)
        self.bottomchatlayout.addWidget(chatbtn)

        # -------------------Pvt Msg Layout--------------------

        self.pvt_msg_obj = msg_GUI.PvtMessage()
        self.chatbtn1 = self.pvt_msg_obj.chatbtn
        self.chattext1 = self.pvt_msg_obj.chattext
        self.chatlabel1= self.pvt_msg_obj.chatlabel
        
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
        self.worker.progress_file.connect(self.getFiles)
        self.worker.progress_pvt_msg.connect(self.getPvtMessage)
        self.thread.start()
    

    def getFiles(self):
        self.file_obj = filesGUI.Files()
        self.file_obj.show()

# -----------------Private Messaging----------------------------
    def getPvtMessage(self,pvt_msg):
        if pvt_msg[0]=="@":
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
        print("Sending this msg: ",send_msg)
        self.conn = client.client
        self.conn.send(send_msg.encode("utf-8"))


# -------------- Group Chat-------------------

    def onClickedSend(self):
        send_msg=self.chattext.text()
        self.chattext.clear()
        self.conn = client.client
        self.conn.send(send_msg.encode("utf-8"))

    def appendMessage(self, msg):
        self.chatWidget.append(msg)


def main():
    app = QApplication(sys.argv)
    ex = ChatRoom()
    ex.resize(500, 350)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
