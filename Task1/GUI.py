import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import client

textfont = QFont("Times", 7)


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        self.conn = client.client
        user_name=input("Enter your username: ")
        self.conn.send(user_name.encode('utf-8'))
        while True:
            try:
                message = self.conn.recv(1024).decode('utf-8')
                if not message == "username?":
                    self.progress.emit(message)
            except:
                print('Error!')
                client.close()
                self.finished.emit()
                break



class ChatRoom(QWidget):

    def __init__(self):
        super(ChatRoom, self).__init__()
        self.initUI()

    def initUI(self):
        
        self.chatlayout = QVBoxLayout()
        self.topchatlayout = QVBoxLayout()
        self.bottomchatlayout = QHBoxLayout()

        self.chatlayout.setContentsMargins(0, 24, 0, 0)
        self.topchatlayout.setContentsMargins(0, 0, 0, 0)
        self.bottomchatlayout.setContentsMargins(0, 0, 0, 0)
        self.chatlayout.addLayout(self.topchatlayout, 90)
        self.chatlayout.addLayout(self.bottomchatlayout, 10)


        chatlabel = QLabel("Group Chat")
        chatlabel.setFont(QFont("Times", 10))
        chatlabel.setAlignment(Qt.AlignCenter)
        chatlabel.setStyleSheet("background: orange;font-weight: bold;")
        self.topchatlayout.addWidget(chatlabel)

        self.chatWidget = QTextEdit()
        self.chatWidget.setReadOnly(True)
        self.chatWidget.setStyleSheet("background: white")
        self.chatWidget.setFont(textfont)
        self.topchatlayout.addWidget(self.chatWidget)

        self.chattext = QLineEdit()
        self.chattext.setPlaceholderText("Type your Message")
        self.bottomchatlayout.addWidget(self.chattext)

        chatbtn=QPushButton("Send")
        chatbtn.clicked.connect(self.onClickedSend)
        self.bottomchatlayout.addWidget(chatbtn)

        self.setLayout(self.chatlayout)


        # --------------Create worker thread---------------
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.appendMessage)
        self.thread.start()

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
