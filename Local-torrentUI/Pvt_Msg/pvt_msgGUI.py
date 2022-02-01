import sys
import os
# from PySide6 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import chatroom.chat_client as client
import chatroom.GUI as work

textfont = QFont("Times", 7)


class PvtMessage(QWidget):

    def __init__(self):
        super(PvtMessage, self).__init__()
        print("Inside PvtMessage Class!")
        self.initUI()

    def initUI(self):
        self.resize(550, 400)
        self.setWindowTitle("Private Message")
        # self.fetchmsg()
        self.msg_layout()
        self.checkDatabaseRecords()

    def checkDatabaseRecords(self):
        # if any records are available then append it into showMessageBox
        pass

    def msg_layout(self):
        self.chatlayout = QVBoxLayout()
        self.topchatlayout = QVBoxLayout()
        self.bottomchatlayout = QHBoxLayout()

        self.chatlayout.addLayout(self.topchatlayout, 90)
        self.chatlayout.addLayout(self.bottomchatlayout, 10)

        chatlabel = QLabel("Username")
        chatlabel.setFont(QFont("Times", 10))
        chatlabel.setAlignment(Qt.AlignCenter)
        chatlabel.setStyleSheet("background: #389bd2;font-weight: bold;color:white;")
        self.topchatlayout.addWidget(chatlabel, 12)

        self.chatWidget = QTextEdit()
        self.chatWidget.setReadOnly(True)
        self.chatWidget.setStyleSheet("background: white")
        self.chatWidget.setFont(textfont)
        self.chatWidget.append("Hello")
        self.topchatlayout.addWidget(self.chatWidget, 88)

        self.chattext = QLineEdit()
        self.chattext.setPlaceholderText("Type your Message")
        self.bottomchatlayout.addWidget(self.chattext)

        self.chatbtn = QPushButton("Send")
        # self.chatbtn.clicked.connect(self.onClickedSend)
        self.bottomchatlayout.addWidget(self.chatbtn)

        self.setLayout(self.chatlayout)
        self.PvtChatThread()

    def PvtChatThread(self):
        # --------------Create worker thread---------------
        # self.thread = QThread()
        self.worker = work.Worker()

    def onClickedSend(self):
        send_msg = self.chattext.text()
        self.chattext.clear()
        send_msg = "PVT_MSG#"+send_msg
        # print("I get your message!")
        # self.conn = client.client
        # self.conn.send(send_msg.encode("utf-8"))
    
    def appendPvtMsg(self, pvt_msg):
        print("appendPvtMsg called again!!", pvt_msg)
        # self.chatWidget.append("Hello")
        self.chatWidget.append(pvt_msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PvtMessage()
    ex.show()
    sys.exit(app.exec_())
