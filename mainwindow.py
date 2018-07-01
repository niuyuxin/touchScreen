#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from math import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from ui import ui_mainwindow
from config import  Config
from settingDialog import SettingDialog
from subdevattr import SubDevAttr
from database import *
from forbiddevdialog import *
from autorunningwidget import *
from independentctrlwidget import *
from systemmanagement import *
from tcpsocket import  TcpSocket
from settingdev import  SettingDevDialog
from userkeys import  *

class MainWindow(QWidget):
    sendDataToTcpSocket = pyqtSignal(QByteArray, int)
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        Config()
        self.rtc = QTimer()
        self.rtc.timeout.connect(self.rtcTimeout)
        self.rtc.start(1000)
        self.mainWindow = ui_mainwindow.Ui_mainWindow()
        self.mainWindow.setupUi(self)
        self.mainWindow.versionLabel.setText(self.getVersion())
        self.subDevList = [[],[]]
        self.creatSubDev(self.subDevList[0], ConfigKeys.onStageDev)
        self.creatSubDev(self.subDevList[1], ConfigKeys.offStageDev)
        self.userKeysList = []
        self.allDevList = []
        self.allDevList.extend(self.subDevList[0])
        self.allDevList.extend(self.subDevList[1])
        self.creatUserKeys(self.userKeysList, self.allDevList)
        self.setWindowTitle("TouchScreen")
        self.init_mainWindow()
    def init_mainWindow(self):
        # independent control widget
        self.independentCtrlWidget = IndependentCtrlWidget(self.subDevList, self)
        self.independentCtrlWidget.selectedList.connect(self.onIndependentWidgetSelected)
        self.autoRunningWidget = AutoRunningWidget()
        self.contextLayout = QHBoxLayout()
        self.contextLayout.addWidget(self.independentCtrlWidget)
        self.contextLayout.addWidget(self.autoRunningWidget)
        self.mainWindow.contextFrame.setLayout(self.contextLayout)
        self.mainWindow.independentCtrlPushButton.clicked.connect(self.onIndependentCtrlPushButton)
        self.mainWindow.autoRunningPushButton.clicked.connect(self.onAutoRunningPushButton)
        self.mainWindow.independentCtrlPushButton.animateClick()
        # setting dialog
        self.settingDialog = SettingDialog(self.subDevList)
        self.mainWindow.settingDataPushButton.clicked.connect(self.onSettingPushButtonClicked)
        # data base
        #  Todo
        """
        try:
            self.dataBaseThread = QThread()
            self.dataBase = DataBase()
            self.settingDialog.saveSetting.connect(self.dataBase.insertRecord)
            self.settingDialog.getSetting.connect(self.dataBase.selectRecord)
            self.dataBase.moveToThread(self.dataBaseThread)
            self.dataBaseThread.start()
        except DataBaseException as err:
            QMessageBox.warning(self,
                                "DataBaseError",
                                str(err),
                                QMessageBox.Yes)
                                """
        # Forbidded dev dialog signals
        self.mainWindow.forbidDevPushButton.clicked.connect(self.onForbidDevDialog)
        # account setting dialog
        self.mainWindow.accountPushButton.clicked.connect(self.onAccountManagement)
        # Tcp socket, creat alone thread
        self.tcpSocket = TcpSocket()
        self.tcpSocketThread = QThread()
        self.tcpSocket.moveToThread(self.tcpSocketThread)
        self.sendDataToTcpSocket.connect(self.tcpSocket.onExternOrderToTcpSocket)
        self.tcpSocket.tcpState.connect(self.onTcpState)
        self.tcpSocketThread.start()
        # print("Tcp socket thread = ", self.tcpSocketThread, "current thread = ", self.thread())
        # setting dev dialog
        self.mainWindow.settingDevPushButton.clicked.connect(self.onSettingDevPushButtonClicked)
        # user keys
        self.mainWindow.userKeysPushButton.clicked.connect(self.onUserKeysPushButtonClicked)
        self.showUserKeys(self.userKeysList, self)
    def onIndependentWidgetSelected(self, l):
        data = ""
        if l:
            for i in l:
                data = data + i.text() + ", "
            print(self.tr("选择了以下设备："), data.rstrip(', '))
            self.sendDataToTcpSocket.emit(QByteArray(bytes(data, encoding="utf-8")), 0)
    def onIndependentCtrlPushButton(self):
        self.mainWindow.modelLabel.setText(self.sender().text())
        self.autoRunningWidget.hide()
        self.independentCtrlWidget.show()
    def onAutoRunningPushButton(self):
        self.mainWindow.modelLabel.setText(self.sender().text())
        self.independentCtrlWidget.hide()
        self.autoRunningWidget.show()
    def rtcTimeout(self):
        # real time
        self.mainWindow.timeLabel.setText(QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"))
    def getVersion(self):
        return "PyQt Version {}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])
    def creatUserKeys(self, userKeys = [], allDevList = []):
        for item in Config.getGroupValue(ConfigKeys.userKeys): # all button for user
            try:
                if ":" in item[1]:
                    id, name, pointtoid = str(item[1]).split(":")
                    indexInSubDevList = 0
                    for dev in allDevList:
                        if dev.devKey == pointtoid:
                            dev.isReplaced = True
                            break
                        indexInSubDevList += 1
                    else:
                        indexInSubDevList = -1
                    button = UserKeysUnit(name, item[0], indexInSubDevList, self)
                    userKeys.append(button)
            except Exception as err:
                print(str(err))
    def showUserKeys(self, userKeysList, parent):
        for w in userKeysList:
            w.setParent(parent)
        count = 0
        for button in self.userKeysList:
            button.show()
            button.move(400 + count * 200, 0)
            count += 1
    def creatSubDev(self, subDevList, whichGroup):
        count = 0
        for item in Config.getGroupValue(whichGroup):
            try:
                if ":" in item[1]:
                    key, name, pos = str(item[1]).split(":")
                else:
                    name = item[1]
                    pos = 100
                button = SubDevAttr(100+count, item[0])
                button.setText(name)
                subDevList.append(button)
                button.clicked.connect(self.onAllSubDevPushButtonClicked)
                count += 1
            except:
                print("creat sub dev error")
    def onSettingPushButtonClicked(self):
        # todo get data from server
        self.settingDialog.showFullScreen()
        self.settingDialog.exec_()
    def onSettingDevPushButtonClicked(self):
        settingDev = SettingDevDialog(self.subDevList)
        settingDev.showFullScreen()
        settingDev.exec_()
        self.independentCtrlWidget.showAllDev(self.subDevList)
    def onUserKeysPushButtonClicked(self):
        try:
            userKeys = UserKyesDialog(self.allDevList, self.userKeysList)
            userKeys.exec_()
            self.showUserKeys(self.userKeysList, self)
        except Exception as e:
            print(str(e))
    def onAllSubDevPushButtonClicked(self):
        button = self.sender()
        activeWin = QApplication.activeWindow()
        if isinstance(activeWin, ForbidDevDialog):
            if button.isChecked():
                button.isUsed = False
                button.setToolTip(self.tr("设备已禁用"))
                print(button.text(), "设备已禁用")
            else:
                button.isUsed = True
                button.setToolTip(self.tr("设备已启用"))
                print(button.text(), "设备已启用")
        else:
            if button.isChecked():
                print(button.text(), "设备已选中 id = ", button.devKey)
            else:
                if button.isPartialCircuit:
                    button.isPartialCircuit = False # 取消旁路设备
                    print(button.text(), "设备旁路已取消")
                print(button.text(), "设备已取消")
    def onTcpState(self, s):
        if s == TcpSocket.ConnectedState:
            self.mainWindow.internetLabel.setText(self.tr("网络已连接"))
        elif s == TcpSocket.ConnectingState:
            self.mainWindow.internetLabel.setText(self.tr("网络正在连接..."))
        else:
            self.mainWindow.internetLabel.setText(self.tr("网络已断开"))

    def onForbidDevDialog(self):
        forbidDevDialog = ForbidDevDialog(self.subDevList)
        forbidDevDialog.showFullScreen()
        forbidDevDialog.exec_()
        self.independentCtrlWidget.showAllDev(self.subDevList)
    def onAccountManagement(self):
        login = AccountLogin()
        if login.exec_():
            a = SystemManagement()
            a.somthingChanged.connect(self.onSystemManagementSomthingChanged)
            a.exec_()
        else:
            return
    def onSystemManagementSomthingChanged(self, key, value):
        self.sendDataToTcpSocket.emit(QByteArray(bytes("", encoding="utf-8")), 1)

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