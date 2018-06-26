#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtNetwork import *
from PyQt5.QtCore import *
from config import Config

class TcpSocket(QTcpSocket):
    tcpState=pyqtSignal(int)
    def __init__(self, parent = None):
        super().__init__(parent)
        self.socketIp = Config.getValue("ServerIp")
        self.connected.connect(self.onTcpSocketConnected)
        self.readyRead.connect(self.onTcpSocketReadyRead)
        self.disconnected.connect(self.onTcpSocketDisconnected)
        self.error.connect(self.onTcpSocketError)
        self.connectTimer = QTimer()
        self.connectTimer.timeout.connect(self.connectServer)
        self.connectTimer.start(1000)
    def onTcpSocketConnected(self):
        print("Tcp socket connected")
        self.tcpState.emit(self.state())
        self.write(QByteArray(bytes("hello server", encoding="utf-8")))
        self.connectTimer.stop()
    def sendData(self, data):
        if self.state() == QAbstractSocket.ConnectedState:
            self.write(data)
            self.waitForBytesWritten()
        else:
            print("网络不可用")
    def connectServer(self):
        if self.state() == QAbstractSocket.UnconnectedState:
            print("Try to connect {}".format(self.socketIp), self.state())
            self.connectToHost(QHostAddress(self.socketIp), 5000)
        elif self.state() == QAbstractSocket.ConnectingState:
            print("Connecting ...")
    def onTcpSocketReadyRead(self):
        print("get server data", str(self.readAll(), encoding="utf-8"))
    def onTcpSocketDisconnected(self):
        self.tcpState.emit(self.state())
        print("Tcp socket disconnected")
        self.connectTimer.start(1000)
    def onTcpSocketError(self, err):
        self.tcpState.emit(self.state())
        self.close()
        self.connectTimer.start(1000)
    def onSendDataToTcpSocket(self, data):
        self.sendData(data)


