#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from math import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from ui import ui_mainwindow
from config import Config
from parasettingdialog import ParaSetting
from subdevattr import SubDevAttr
from forbiddevdialog import *
from singlectrlwidget import *
from systemmanagement import *
from tcpsocket import TcpSocket
from settingdev import SettingDevDialog
from userkeys import *
from analogdetection import *

class MainWindow(QFrame):
    sendDataToTcpSocket = pyqtSignal(int, str, dict)
    tcpSocketManagement = pyqtSignal(int)
    mainWindowOrder = pyqtSignal(str, dict)
    userKeySelected = pyqtSignal(dict)
    runningState = pyqtSignal(int)
    pcf8591Mode = pyqtSignal(int)
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
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
        self.analogDetection = AnalogDetection()
        self.analogDetectionThread = QThread()
        self.analogDetection.moveToThread(self.analogDetectionThread)
        self.analogDetection.ADValueChanged.connect(self.onAnalogDetectionADValueChanged)
        self.userKeySelected.connect(self.analogDetection.onUserKeySelected)
        self.analogDetection.GPIOState.connect(self.onPhysicalKeyClicked)
        self.analogDetectionThread.started.connect(self.analogDetection.init)
        self.pcf8591Mode.connect(self.analogDetection.pcf8591LedMode)
        self.analogDetectionThread.start()
        self.init_mainWindow()
    def init_mainWindow(self):
        # independent control widget
        self.singleCtrlWidget = SingleCtrlWidget(self.subDevList, self)
        self.singleCtrlWidget.selectedList.connect(self.onDevOperated)
        self.mainWindowOrder.connect(self.singleCtrlWidget.onHandleExternOrder)
        self.contextLayout = QHBoxLayout()
        self.contextLayout.addWidget(self.singleCtrlWidget)
        self.contextLayout.setContentsMargins(0,0,0,0)
        self.mainWindow.contextFrame.setLayout(self.contextLayout)
        self.mainWindow.singleCtrlPushButton.clicked.connect(self.onSingleCtrlPushButton)
        self.mainWindow.singleCtrlPushButton.animateClick()
        # setting dialog
        self.mainWindow.settingDataPushButton.clicked.connect(self.onSettingPushButtonClicked)
        self.paraSetting = ParaSetting(self.allDevList)
        self.paraSetting.sendDataToTcpSocket.connect(self.sendDataToTcpSocket)
        # Forbidded dev dialog signals
        self.mainWindow.forbidDevPushButton.clicked.connect(self.onForbidDevDialog)
        self.forbidDevDialog = ForbidDevDialog(self.subDevList)
        self.settingDev = SettingDevDialog(self.subDevList)
        # account setting dialog
        self.mainWindow.accountPushButton.clicked.connect(self.onAccountManagement)
        self.systemManagement = SystemManagement()
        self.systemManagement.somthingChanged.connect(self.onSystemManagementSomthingChanged)
        # self.systemManagement = SystemManagement()
        # self.systemManagement.somthingChanged.connect(self.onSystemManagementSomthingChanged)
        # Tcp socket, creat alone thread
        self.tcpSocket = TcpSocket(self.allDevList)
        self.tcpSocketThread = QThread()
        self.tcpSocket.moveToThread(self.tcpSocketThread)
        self.sendDataToTcpSocket.connect(self.tcpSocket.onDataToSend)
        self.tcpSocketManagement.connect(self.tcpSocket.onTcpSocketManagement)
        self.tcpSocket.tcpState.connect(self.onTcpState)
        self.tcpSocket.tcpGetOrder.connect(self.mainWindowOrder)
        self.tcpSocket.tcpGetOrder.connect(self.onTcpsocketTcpGetOrder)
        self.tcpSocket.paraSetting.connect(self.onTcpSocketParaSetting)
        self.tcpSocketThread.started.connect(self.tcpSocket.tcpSocketInit)
        self.tcpSocketThread.start()
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
                self.pcf8591Mode.emit(AnalogDetection.PCF8591_SELECTED)
            else: # 取消旁路设备
                self.pcf8591Mode.emit(AnalogDetection.PCF8591_NOSELECTED)
                self.devOperationDict[SettingDevDialog.PartialOperation] = []
                self.devOperationDict[state] = []
                self.pushDeviceState()
        except Exception as e:
            print("onDevOperated", str(e))

    def onSingleCtrlPushButton(self):
        self.singleCtrlWidget.show()

    def rtcTimeout(self):
        # real time
        self.mainWindow.timeLabel.setText(QDateTime.currentDateTime().toString("yyyy/MM/dd dddd hh:mm:ss"))
    def getVersion(self):
        return "Version {}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])
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
        """show all seleted user keys"""
        for w in userKeysList:
            w.setParent(parent)
        keyValue = {}
        count = 0
        for button in userKeysList:
            button.move(400 + count * 200, 0)
            if button.indexOfDev == -1:
                button.hide()
            else:
                button.show()
            keyValue[count] = button.indexOfDev
            count += 1
        self.userKeySelected.emit(keyValue)

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
        self.paraSetting.exec_()

    def onUserKeysPushButtonClicked(self):
        try:
            userKeys = UserKeysDialog(self.allDevList, self.userKeysList)
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
                if not button.isChecked():
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
        # settingDev.showFullScreen()
        self.settingDev.createAllWidget(self.subDevList)
        self.settingDev.exec_()
        self.devOperationDict[SettingDevDialog.PartialOperation] = self.checkPartialDevice()
        self.pushDeviceState()
        self.singleCtrlWidget.showAllDev(self.subDevList)

    def onForbidDevDialog(self): # 设备禁用
        # forbidDevDialog.showFullScreen()
        self.forbidDevDialog.createAllWidget(self.subDevList)
        self.forbidDevDialog.exec_()
        self.devOperationDict[ForbidDevDialog.ForbiddenOperation] = self.checkForbiddenDevice()
        self.pushDeviceState()
        self.singleCtrlWidget.showAllDev(self.subDevList)

    def onAccountManagement(self):
        login = AccountLogin()
        try:
            if login.exec_():
                self.systemManagement.exec_()
            else:
                return
        except Exception as e:
            print(str(e))
    @pyqtSlot(str, str)
    def onSystemManagementSomthingChanged(self, key, value):
        self.tcpSocketManagement.emit(1)

    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     "quit application",
                                     "Don't you want to quit application",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            event.ignore()
        else:
            login = AccountLogin()
            if login.exec_():
                self.tcpSocketThread.quit()
                self.tcpSocketThread.wait()
                event.accept()
            else:
                event.ignore()
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
        if SingleCtrlWidget.SelectedOperation in self.devOperationDict.keys() and\
            len(self.devOperationDict[SingleCtrlWidget.SelectedOperation]) == 0:
            if self.isActiveWindow():
                QMessageBox.warning(self,"警告", self.tr("请先选择设备， 然后进行操作！"), QMessageBox.Ok)
            button.setChecked(False)
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

        value = self.mainWindow.speedSetSlider.value()
        self.sendDataToTcpSocket.emit(TcpSocket.Call, TcpSocket.SpeedSet, {"Value": value})
        self.sendDataToTcpSocket.emit(TcpSocket.Call, TcpSocket.OperationalCtrl, {"State":s})

    def onSpeedSetSliderValueChanged(self, value):
        self.mainWindow.lcdNumber.display(value)
        self.sendDataToTcpSocket.emit(TcpSocket.Call, TcpSocket.SpeedSet, {"Value": value})
    def onAnalogDetectionADValueChanged(self, port, value):
        self.mainWindow.speedSetSlider.setValue(value)

    def onTcpSocketParaSetting(self, value):
        try:
            for info in value:
                if len(info) <= 4:
                    continue
                name = info[0]
                dev = None
                for d in self.allDevList:
                    if d.text() == name:
                        dev = d
                        break
                if dev != None:
                    dev.targetPos = info[1]
                    dev.upLimitedPos = info[2]
                    dev.downLimitedPos = info[3]
                    dev.valueChanged.emit()
        except Exception as e:
            print("onTcpSocketParaSetting", str(e))

    def onTcpsocketTcpGetOrder(self, action, info):
        try:
            if action == TcpSocket.ForbiddenDevice:
                enable = info["Enable"]
                self.mainWindow.analogControlGroupBox.setEnabled(not enable)
                if enable:
                    self.mainWindow.modelTextLabel.setText(self.tr("程控模式"))
                else:
                    self.mainWindow.modelTextLabel.setText(self.tr("单控模式"))
        except Exception as e:
            print("onTcpsocketTcpGetOrder", str(e))
    def onPhysicalKeyClicked(self, key, state):
        if key in [AnalogDetection.GPIO_RAISE, AnalogDetection.GPIO_STOP, AnalogDetection.GPIO_DROP]:
            if SingleCtrlWidget.SelectedOperation in self.devOperationDict.keys() and\
                len(self.devOperationDict[SingleCtrlWidget.SelectedOperation]) == 0:
                if self.isActiveWindow():
                    QMessageBox.warning(self,"警告", self.tr("请先选择设备， 然后进行操作！"), QMessageBox.Ok)
                return
            if key == AnalogDetection.GPIO_RAISE:
                self.mainWindow.raisePushButton.animateClick()
            elif key == AnalogDetection.GPIO_STOP:
                self.mainWindow.stopPushButton.animateClick()
            elif key == AnalogDetection.GPIO_DROP:
                self.mainWindow.dropPushButton.animateClick()

