#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtNetwork import *
from PyQt5.QtCore import *
from config import *
import  json
import random
import json
import copy

class TcpSocket(QObject):
    tcpState=pyqtSignal(int)
    tcpGetOrder = pyqtSignal(str, dict)
    paraSetting = pyqtSignal(list)
    Call = 2
    CallResult = 3
    CallError = 4
    DeviceStateChanged = "DeviceStateChanged"
    ForbiddenDevice = "ForbiddenDevice"
    ParaSetting = "ParaSetting"
    OperationalCtrl = "OperationalCtrl"
    SpeedSet = "SpeedSet"
    MonitorId = "MonitorId"
    MonitorDevice = "MonitorDevice"
    MonitorDeviceCount = "MonitorDeviceCount"
    MonitorName = "MonitorName"
    BootNotification = "BootNotification"
    UpdateDevice = "UpdateDevice"
    def __init__(self, allSubDev, parent = None):
        super().__init__(parent)
        self.allSubDev = allSubDev
        self.toUpdateDev = []
    def tcpSocketInit(self):
        self.tcpSocket = QTcpSocket(self)
        self.tcpSocket.connected.connect(self.onTcpSocketConnected)
        self.tcpSocket.readyRead.connect(self.onTcpSocketReadyRead)
        self.tcpSocket.disconnected.connect(self.onTcpSocketDisconnected)
        self.tcpSocket.error.connect(self.onTcpSocketError)
        self.connectTimer = QTimer(self)
        self.connectTimer.timeout.connect(self.connectServer)
        self.connectTimer.start(1000)

    def onTcpSocketConnected(self):
        print("Tcp socket connected")
        self.tcpState.emit(self.tcpSocket.state())
        self.connectTimer.stop()
    def connectServer(self, e = 0):
        if e == 1 or self.tcpSocket.state() == QAbstractSocket.UnconnectedState:
            ip = Config.value(ConfigKeys.serverIp)
            if ip == None:
                socketIp = QHostAddress(QHostAddress.LocalHost)  # "192.168.1.177"
            else:
                socketIp = ip
            self.tcpSocket.connectToHost(QHostAddress(socketIp), 5000)
        elif self.tcpSocket.state() == QAbstractSocket.ConnectingState:
            self.tcpState.emit(self.tcpSocket.state())
    def onTcpSocketReadyRead(self):
        temp = self.tcpSocket.readAll()
        serverData = str(temp, encoding="utf-8")
        print("Get server data:", serverData)
        if "Hello" in serverData:
            try:
                di = {TcpSocket.MonitorName:Config.value(ConfigKeys.monitorName),
                      TcpSocket.MonitorId: Config.monitorId,
                      TcpSocket.MonitorDeviceCount:len(self.allSubDev)
                      }
                self.toUpdateDev = copy.copy(self.allSubDev)
                self.onDataToSend(TcpSocket.Call, TcpSocket.BootNotification, di)
            except Exception as e:
                print(str(e))
        else:
            serverDataList = serverData.split('\0')
            for data in serverDataList:
                if len(data) != 0:
                    self.analysisData(data)
    def analysisData(self, data):
        try:
            dataJson = json.loads(data, encoding='UTF-8')
            if len(dataJson) == 4 and dataJson[0] == 2: # 服务器call
                order = dataJson[2]
                self.tcpGetOrder.emit(order, dataJson[3])
            elif len(dataJson) == 4 and dataJson[0] == 3: # 服务器callreturn
                order = dataJson[2]
                if order == TcpSocket.BootNotification:
                    self.updateDev()
                elif order == TcpSocket.UpdateDevice:
                    self.paraSetting.emit(dataJson[3]["Device"])
                    self.updateDev()

        except Exception as e:
            print("analysisData", str(e))

    def onTcpSocketDisconnected(self):
        self.tcpState.emit(self.tcpSocket.state())
        self.connectTimer.start(1000)
        print("Tcp socket disconnected")

    @pyqtSlot(QAbstractSocket.SocketError)
    def onTcpSocketError(self, err):
        self.tcpState.emit(self.tcpSocket.state())
        self.tcpSocket.disconnectFromHost()
        self.connectTimer.start(1000)

    @pyqtSlot(int)
    def onTcpSocketManagement(self, code):
        if code:
            self.tcpSocket.disconnectFromHost()
            print("on tcp socket abort()")

    @pyqtSlot(int, str, dict)
    def onDataToSend(self, messageTypeId, action, data):
        try:
            if not isinstance(messageTypeId, int) or not isinstance(action, str) or not isinstance(data, dict):
                raise "onDataToSend: data type error"
            message = [messageTypeId, self.createUnionId(action), action, data]
            self.sendData(bytes(json.dumps(message, ensure_ascii='UTF-8'), encoding='utf-8')+b'\0')
        except Exception as e:
            print("onDataToSend", str(e))

    def sendData(self, data):
        if self.tcpSocket.state() == QAbstractSocket.ConnectedState:
            self.tcpSocket.write(data)
            self.tcpSocket.waitForBytesWritten()
        else:
            print("网络不可用")

    def createUnionId(self, type):
        time = QDateTime.currentDateTime().toString("yyMMddhhmmsszzz")
        rand = str(random.randint(0, 100))
        return str(type) + '-' + time + '-' + rand

    def updateDev(self):
        devList = []
        for count in range(2):
            if len(self.toUpdateDev) != 0:
                item = self.toUpdateDev.pop(0)
                devList.append((item.devId, item.text()))
            else:
                break
        if devList:
            di = {TcpSocket.MonitorDevice:devList}
            self.onDataToSend(TcpSocket.Call, TcpSocket.UpdateDevice, di)