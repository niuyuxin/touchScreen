#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtNetwork import *
from PyQt5.QtCore import *
from config import *

class TcpSocket(QObject):
    tcpState=pyqtSignal(int)
    def __init__(self, allSubDev, parent = None):
        super().__init__(parent)
        self.allSubDev = allSubDev
        self.tcpSocket = QTcpSocket()
        self.tcpSocket.connected.connect(self.onTcpSocketConnected)
        self.tcpSocket.readyRead.connect(self.onTcpSocketReadyRead)
        self.tcpSocket.disconnected.connect(self.onTcpSocketDisconnected)
        self.tcpSocket.error.connect(self.onTcpSocketError)
        self.connectTimer = QTimer()
        self.connectTimer.timeout.connect(self.connectServer)
        self.connectTimer.start(1000)
    def onTcpSocketConnected(self):
        print("Tcp socket connected")
        self.tcpState.emit(self.tcpSocket.state())
        self.connectTimer.stop()
    def sendData(self, data):
        if self.tcpSocket.state() == QAbstractSocket.ConnectedState:
            self.tcpSocket.write(data)
            self.tcpSocket.waitForBytesWritten()
        else:
            print("网络不可用")
    def connectServer(self, e = 0):
        if e == 1 or self.tcpSocket.state() == QAbstractSocket.UnconnectedState:
            ip = Config.getValue(ConfigKeys.serverIp)
            if ip == None:
                socketIp = QHostAddress(QHostAddress.LocalHost)  # "192.168.1.177"
            else:
                socketIp = ip
            self.tcpSocket.connectToHost(QHostAddress(socketIp), 5000)
        elif self.tcpSocket.state() == QAbstractSocket.ConnectingState:
            self.tcpState.emit(self.tcpSocket.state())
    def onTcpSocketReadyRead(self):
        serverData = str(self.tcpSocket.readAll(), encoding="utf-8")
        print("Get server data:", serverData)
        if "Hello" in serverData:
            try:
                li = [item.text() for item in self.allSubDev]
                self.tcpSocket.write(QByteArray(bytes(str(li), encoding="utf-8")))
            except Exception as e:
                print(str(e))
    def onTcpSocketDisconnected(self):
        print("Tcp socket disconnected")
        self.tcpState.emit(self.tcpSocket.state())
        self.connectTimer.start(1000)
    def onTcpSocketError(self, err):
        self.tcpState.emit(self.tcpSocket.state())
        self.tcpSocket.close()
        self.connectTimer.start(1000)
    def onExternOrderToTcpSocket(self, data = None, order = None):
        if order == 0: # send data
            self.sendData(data)
        elif order == 1: # 重启网络
            self.tcpSocket.disconnectFromHost()



