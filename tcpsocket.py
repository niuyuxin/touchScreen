#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtNetwork import *

class TcpSocket(QTcpSocket):
    def __init__(self):
        super().__init__()
        self.connected.connect(self.onTcpSocketConnected)
        self.readyRead.connect(self.onTcpSocketReadyRead)
        self.disconnected.connect(self.onTcpSocketDisconnected)
        self.error.connect(self.onTcpSocketError)


    def onTcpSocketConnected(self):
        print("Tcp sockett connected")
    def onTcpSocketReadyRead(self):
        print("tcp ready read")
    def onTcpSocketDisconnected(self):
        print("Tcp socket disconnected")
    def onTcpSocketError(self, err):
        print("Tcp socket error", err)