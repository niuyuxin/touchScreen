#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtNetwork import *
from PyQt5.QtCore import *
from threading import Thread

class TcpSocket(QTcpSocket):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.connected.connect(self.onTcpSocketConnected)
        self.readyRead.connect(self.onTcpSocketReadyRead)
        self.disconnected.connect(self.onTcpSocketDisconnected)
        self.error.connect(self.onTcpSocketError)
        self.connectToHost(QHostAddress("192.168.1.177"), 5000)
        self.connectTimer = QTimer(self)
        self.connectTimer.timeout.connect(self.connectServer)
    def onTcpSocketConnected(self):
        print("Tcp socket connected")
        self.connectTimer.stop()
    def sendData(self, data):
        if self.state() == QAbstractSocket.ConnectedState:
            self.write(data)
        else:
            print("网络不可用")
    def connectServer(self):
        if self.state() == QAbstractSocket.UnconnectedState:
            print("Retry to connect localhost", self.state())
            self.connectToHost(QHostAddress("192.168.1.177"), 5000)
        else:
            print(self.state())
    def onTcpSocketReadyRead(self):
        print("服务器获取到已选择设备")
    def onTcpSocketDisconnected(self):
        print("Tcp socket disconnected")
        self.connectTimer.start(1000)
    def onTcpSocketError(self, err):
        self.close()
        self.connectTimer.start(1000)
    def onSendDataToTcpSocket(self, data):
        self.sendData(data)


