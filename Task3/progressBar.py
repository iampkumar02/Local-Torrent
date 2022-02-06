import sys
import os
# from PySide6 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import socket
from tqdm import tqdm
import json
IP = "localhost"
PORT = 4444
ADDR = (IP, PORT)
SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
username = input("Enter username: ")
client.send(username.encode("utf-8"))

data = client.recv(1024).decode('utf-8')
item = data.split("@")
FILENAME = item[0]
FILESIZE = int(item[1])
# client.send("Filename and filesize received".encode("ascii"))

textfont = QFont("Times", 7)


class DownloadProgress(QWidget):

    def __init__(self):
        super(DownloadProgress, self).__init__()
        # print("Inside Files Class!")
        self.initUI()
        # self.show()
        self.thread=QThread()
        self.thread.start()
        # self.receivingData()

    def initUI(self):
        self.resize(550, 400)
        self.setWindowTitle("Progress Bar")
        # self.fetchFiles()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        self.timer = QTimer()
        self.timer.timeout.connect(self.runProgressBar)
        self.timer.setInterval(100)

        self.progressbar = QProgressBar()
        self.startbtn = QPushButton("Start")
        self.startbtn.clicked.connect(self.timerstart)
        stopbtn = QPushButton("Stop")
        stopbtn.clicked.connect(self.timerstop)
        vbox.addWidget(self.progressbar)
        hbox.addWidget(self.startbtn)
        hbox.addWidget(stopbtn)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def receivingData(self):
        client.send("Filename and filesize received".encode("ascii"))
        """ Data transfer """
        # bar = tqdm(range(
        #     FILESIZE), f"Receiving long.txt", unit="B", unit_scale=True, unit_divisor=SIZE)
        cnt_size = 0
        with open("E:\Computer Network\Local-torrent\client_data\\text.txt", "w") as f:
            data_size = client.recv(1024).decode("ascii")
            data_size = int(round(float(data_size)))

            print("Data size: ", data_size)
            g = open('E:\Computer Network\Local-Torrent\\temp_file.json')
            data = json.load(g)
            v = 0
            for i in data['users']:
                name = i['username']
                if name == username:
                    v = i['count']
                    f.seek(v)
                    break
            j = 0
            while j < v/1024:
                j += 1
                # bar.update(1024)

            g.close()
            while True:
                cnt_size += 1
                data = client.recv(SIZE).decode("utf-8")
                if not data:
                    break

                f.write(data)
                perc=(cnt_size/data_size)*100
                perc=int(round(perc))
                # bar.update(len(data))
                self.progressbar.setValue(perc)

        print("Perc: ", perc)
        # client.close()
        print("Size of file received now: ", cnt_size/1024)
        self.thread.quit
        self.thread.deleteLater
    
    def runProgressBar(self):
        # self.progressbar.setValue(80)
        pass
        # self.timer.stop()

    def timerstart(self):
        # self.timer.start()
        self.receivingData()
        self.startbtn.setEnabled(False)

    def timerstop(self):
        self.timer.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DownloadProgress()
    ex.show()
    sys.exit(app.exec_())
