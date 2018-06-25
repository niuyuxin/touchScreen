#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtNetwork import *
from PyQt5.QtCore import *

class TcpSocket(QTcpSocket):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.connected.connect(self.onTcpSocketConnected)
        self.readyRead.connect(self.onTcpSocketReadyRead)
        self.disconnected.connect(self.onTcpSocketDisconnected)
        self.error.connect(self.onTcpSocketError)
        self.connectTimer = QTimer()
        self.connectTimer.timeout.connect(self.onConnectTimerTimeout)
        self.connectTimer.start(1000)


    def onTcpSocketConnected(self):
        print("Tcp sockett connected")
    def onTcpSocketReadyRead(self):
        print("tcp ready read")
    def onTcpSocketDisconnected(self):
        print("Tcp socket disconnected")
    def onTcpSocketError(self, err):
        print("Tcp socket error", err, self.thread())

    def onConnectTimerTimeout(self):
        self.connectToHost("localhost", 50000)
        self.connectTimer.stop()
        print("wait for connected ...", self.thread())
        self.waitForConnected(10000)
        print("timeout .... ")
        self.sender().start(1000)