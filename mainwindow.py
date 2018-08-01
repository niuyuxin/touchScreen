#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from math import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from ui import ui_mainwindow
from config import  Config
from parasettingdialog import ParaSetting
from subdevattr import SubDevAttr
from forbiddevdialog import *
from singlectrlwidget import *
from systemmanagement import *
from tcpsocket import  TcpSocket
from settingdev import  SettingDevDialog
from userkeys import  *

class MainWindow(QFrame):
    sendDataToTcpSocket = pyqtSignal(int, str, dict)
    tcpSocketManagement = pyqtSignal(int)
    mainWindowOrder = pyqtSignal(str, dict)
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        Config()
        self.rtc = QTimer()
        self.rtc.timeout.connect(self.rtcTimeout)
        self.rtc.start(1000)
        self.mainWindow = ui_mainwindow.Ui_mainWindow()
        self.mainWindow.setupUi(self)
        self.mainWindow.versionLabel.setText(self.getVersion())
        self.setWindowTitle("TouchScreen({})".format(Config.monitorId))
        self.operationButtonGroup = QButtonGroup()
        self.operationButtonGroup.addButton(self.mainWindow.raisePushButton)
        self.operationButtonGroup.addButton(self.mainWindow.stopPushButton)
        self.operationButtonGroup.addButton(self.mainWindow.dropPushButton)
        self.mainWindow.raisePushButton.pressed.connect(self.onOperationPushButtonPressed)
        self.mainWindow.stopPushButton.pressed.connect(self.onOperationPushButtonPressed)
        self.mainWindow.dropPushButton.pressed.connect(self.onOperationPushButtonPressed)
        self.mainWindow.speedSetSlider.valueChanged.connect(self.onSpeedSetSliderValueChanged)
        self.devOperationDict = {1<<0:[], 1<<1:[], 1<<2:[]}
        self.subDevList = [[],[]]
        self.creatSubDev(self.subDevList[0], ConfigKeys.onStageDev)
        self.creatSubDev(self.subDevList[1], ConfigKeys.offStageDev)
        self.userKeysList = []
        self.allDevList = []
        self.allDevList.extend(self.subDevList[0])
        self.allDevList.extend(self.subDevList[1])
        self.creatUserKeys(self.userKeysList, self.allDevList)
        self.init_mainWindow()
    def init_mainWindow(self):
        # independent control widget
        self.singleCtrlWidget = SingleCtrlWidget(self.subDevList, self)
        self.singleCtrlWidget.selectedList.connect(self.onDevOperated)
        self.mainWindowOrder.connect(self.singleCtrlWidget.onHandleExternOrder)
        self.contextLayout = QHBoxLayout()
        self.contextLayout.addWidget(self.singleCtrlWidget)
        self.mainWindow.contextFrame.setLayout(self.contextLayout)
        self.mainWindow.singleCtrlPushButton.clicked.connect(self.onSingleCtrlPushButton)
        self.mainWindow.singleCtrlPushButton.animateClick()
        # setting dialog
        self.paraSetting = ParaSetting(self.allDevList)
        self.mainWindow.settingDataPushButton.clicked.connect(self.onSettingPushButtonClicked)
        self.paraSetting.sendDataToTcpSocket.connect(self.sendDataToTcpSocket)
        # Forbidded dev dialog signals
        self.mainWindow.forbidDevPushButton.clicked.connect(self.onForbidDevDialog)
        # account setting dialog
        self.mainWindow.accountPushButton.clicked.connect(self.onAccountManagement)
        # Tcp socket, creat alone thread
        self.tcpSocket = TcpSocket(self.allDevList)
        self.tcpSocketThread = QThread()
        self.tcpSocket.moveToThread(self.tcpSocketThread)
        self.sendDataToTcpSocket.connect(self.tcpSocket.onDataToSend)
        self.tcpSocketManagement.connect(self.tcpSocket.onTcpSocketManagement)
        self.tcpSocket.tcpState.connect(self.onTcpState)
        self.tcpSocket.tcpGetOrder.connect(self.mainWindowOrder)
        self.tcpSocketThread.started.connect(self.tcpSocket.tcpSocketInit)
        self.tcpSocketThread.start()
        # print("Tcp socket thread = ", self.tcpSocketThread, "current thread = ", self.thread())
        # setting dev dialog
        self.mainWindow.settingDevPushButton.clicked.connect(self.onSettingDevPushButtonClicked)
        # user keys
        self.mainWindow.userKeysPushButton.clicked.connect(self.onUserKeysPushButtonClicked)
        self.showUserKeys(self.userKeysList, self)
    def onDevOperated(self, state, selectedDev):
        try:
            if selectedDev and isinstance(selectedDev, list):
                devInfoList = []
                for dev in selectedDev:
                    devInfoList.append(dev.text())
                print(self.tr("选择了以下设备："), devInfoList)
                self.devOperationDict[state] = selectedDev
                self.pushDeviceState()
            else: # 取消旁路设备
                self.devOperationDict[SettingDevDialog.PartialOperation] = []
                self.devOperationDict[state] = []
                self.pushDeviceState()
        except Exception as e:
            print("onDevOperated", str(e))
    def onSingleCtrlPushButton(self):
        self.mainWindow.modelLabel.setText(self.sender().text())
        self.singleCtrlWidget.show()
    def rtcTimeout(self):
        # real time
        self.mainWindow.timeLabel.setText(QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"))
    def getVersion(self):
        return "PyQt Version {}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])
    def creatUserKeys(self, userKeys = [], allDevList = []):
        for item in Config.getGroupValue(ConfigKeys.userKeys): # all button for user
            try:
                if ":" in item[1]:
                    # id, name, pointtoid = str(item[1]).split(":")
                    infoList = str(item[1]).split(":")
                    indexInSubDevList = 0
                    for dev in allDevList:
                        if dev.devKey == infoList[-1]: # the last info is specific device id
                            dev.isReplaced = True
                            break
                        indexInSubDevList += 1
                    else:
                        indexInSubDevList = -1
                    # print(infoList) # 0,id 1,name 2,speed 3,specificDevKey
                    button = UserKeysUnit(infoList[1], item[0], infoList[-1], indexInSubDevList, int(infoList[2]), self)
                    userKeys.append(button)
            except Exception as err:
                print(str(err))
    def showUserKeys(self, userKeysList, parent):
        for w in userKeysList:
            w.setParent(parent)
        count = 0
        for button in self.userKeysList:
            button.move(400 + count * 200, 0)
            count += 1
            if button.indexOfDev == -1:
                button.hide()
            else:
                button.show()
    def creatSubDev(self, subDevList, whichGroup):
        count = 0
        for item in Config.getGroupValue(whichGroup):
            try:
                sp = ":"
                if sp in item[1]:
                    infoList = str(item[1]).split(sp)
                    button = SubDevAttr(100+count, infoList[0], item[0])
                    button.setText(infoList[1])
                    subDevList.append(button)
                    button.clicked.connect(self.onAllSubDevPushButtonClicked)
                    count += 1
            except Exception as err:
                print("creat sub dev error:{}, {}".format(err, item))

    def onSettingPushButtonClicked(self):
        self.paraSetting.showFullScreen()
        self.paraSetting.exec_()

    def onUserKeysPushButtonClicked(self):
        try:
            userKeys = UserKyesDialog(self.allDevList, self.userKeysList)
            userKeys.exec_()
            self.showUserKeys(self.userKeysList, self)
        except Exception as e:
            print(str(e))
    def onAllSubDevPushButtonClicked(self):
        try:
            button = self.sender()
            activeWin = QApplication.activeWindow()
            if isinstance(activeWin, ForbidDevDialog):
                if button.isChecked():
                    button.isUsed = False
                    button.setToolTip(self.tr("设备已禁用"))
                else:
                    button.isUsed = True
                    button.setToolTip(self.tr("设备已启用"))
            else:
                if button.isChecked():pass
                    # print(button.text(), "设备已选中 key = ", button.devKey)
                else:
                    promot = ""
                    if button.isPartialCircuit:
                        button.isPartialCircuit = False # 取消旁路设备
                        self.devOperationDict[SettingDevDialog.PartialOperation] = self.checkPartialDevice()
                        self.pushDeviceState()
                        promot = "旁路已取消, "
                    print(button.text(), promot+"设备已取消")
        except Exception as e:
            print("onAllSubDevPushButtonClicked", str(e))
    def onTcpState(self, s):
        try:
            if s == QTcpSocket.ConnectedState:
                self.mainWindow.internetLabel.setText(self.tr("网络已连接"))
            elif s == QTcpSocket.ConnectingState:
                self.mainWindow.internetLabel.setText(self.tr("网络正在连接..."))
            else:
                self.mainWindow.internetLabel.setText(self.tr("网络已断开"))
        except Exception as e:
            print(str(e))

    def onSettingDevPushButtonClicked(self): # 设备设定
        settingDev = SettingDevDialog(self.subDevList)
        settingDev.showFullScreen()
        settingDev.exec_()
        self.devOperationDict[SettingDevDialog.PartialOperation] = self.checkPartialDevice()
        self.pushDeviceState()
        self.singleCtrlWidget.showAllDev(self.subDevList)

    def onForbidDevDialog(self): # 设备禁用
        forbidDevDialog = ForbidDevDialog(self.subDevList)
        forbidDevDialog.showFullScreen()
        forbidDevDialog.exec_()
        self.devOperationDict[ForbidDevDialog.ForbiddenOperation] = self.checkForbiddenDevice()
        self.pushDeviceState()
        self.singleCtrlWidget.showAllDev(self.subDevList)

    def onAccountManagement(self):
        login = AccountLogin()
        try:
            if login.exec_():
                a = SystemManagement()
                a.somthingChanged.connect(self.onSystemManagementSomthingChanged)
                a.exec_()
            else:
                return
        except Exception as e:
            print(str(e))
    @pyqtSlot(str, str)
    def onSystemManagementSomthingChanged(self, key, value):
        self.tcpSocketManagement.emit(1)

    def closeEvent(self, event):
        return
        reply = QMessageBox.question(self,
                                     "quit application",
                                     "Don't you want to quit application",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            event.ignore()
        else:
            self.tcpSocketThread.quit()
            self.tcpSocketThread.wait()
            event.accept()
    # def resizeEvent(self, QResizeEvent):
    #     rect = self.pos()
    #     print(rect)
    #     count = 0
    #     for button in self.userKeysList:
    #         button.move(rect.x() + 300 + count*120, 0)
    #         count += 1

    def checkForbiddenDevice(self):
        devList = []
        for subDev in self.subDevList:
            for dev in subDev:
                if not dev.isUsed:
                    devList.append(dev)
        return devList

    def checkPartialDevice(self):
        devList = []
        for subDev in self.subDevList:
            for dev in subDev:
                if dev.isPartialCircuit:
                    devList.append(dev)
        return devList

    def pushDeviceState(self):
        devInfoList = []
        for state, devList in self.devOperationDict.items():
            for dev in devList:
                devInfoList.append([dev.text(), state, dev.ctrlWord])
        self.sendDataToTcpSocket.emit(TcpSocket.Call,
                                      TcpSocket.DeviceStateChanged,
                                      {"Device": devInfoList})

    def onOperationPushButtonPressed(self):
        button = self.sender()
        if not isinstance(button, QPushButton):
            return
        if not button.isDown():
            return
        s = 0
        if button.objectName() == "raisePushButton":
            s = 1
        elif button.objectName() == "dropPushButton":
            s = -1
        elif button.objectName() == "stopPushButton":
            s = 0
        self.sendDataToTcpSocket.emit(TcpSocket.Call, TcpSocket.OperationalCtrl, {"State":s})
    def onSpeedSetSliderValueChanged(self, value):
        self.sendDataToTcpSocket.emit(TcpSocket.Call, TcpSocket.SpeedSet, {"Value": value})