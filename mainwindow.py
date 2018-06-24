#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from math import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui import ui_mainwindow
from config import  Config
from settingDialog import SettingDialog
from pushbuttonwithattr import PushButtonWithAttr
from database import *
from forbiddevdialog import *
from autorunningwidget import *
from independentctrlwidget import *
from systemmanagement import SystemManagement

class MainWindow(QWidget):
    """ 初始化、定时器、版本设置
    """
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
        self.creatSubDev(self.subDevList[0], "SubDevUpStage")
        self.creatSubDev(self.subDevList[1], "SubDevDownStage")
        self.setWindowTitle("TouchScreen")
        self.init_mainWindow()
    def init_mainWindow(self):
        """ independent control widget """
        self.forbidDevDialog = ForbidDevDialog(self.subDevList)
        self.independentCtrlWidget = IndependentCtrlWidget(self.subDevList, self)
        self.autoRunningWidget = AutoRunningWidget()
        self.contextLayout = QHBoxLayout()
        self.contextLayout.addWidget(self.independentCtrlWidget)
        self.contextLayout.addWidget(self.autoRunningWidget)
        self.mainWindow.contextFrame.setLayout(self.contextLayout)
        self.mainWindow.independentCtrlPushButton.clicked.connect(self.onIndependentCtrlPushButton)
        self.mainWindow.autoRunningPushButton.clicked.connect(self.onAutoRunningPushButton)
        self.mainWindow.independentCtrlPushButton.animateClick()
        """ setting dialog """
        self.settingDialog = SettingDialog()
        self.mainWindow.settingPushButton.clicked.connect(self.onSettingPushButtonClicked)
        """ data base """
        #  Todo
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
        """ Forbidded dev dialog signals """
        self.mainWindow.forbidDevPushButton.clicked.connect(self.onForbidDevDialog)
        """ account setting dialog """
        self.mainWindow.accountPushButton.clicked.connect(self.onAccountManagement)
    def onIndependentCtrlPushButton(self):
        self.autoRunningWidget.hide()
        self.independentCtrlWidget.show()
    def onAutoRunningPushButton(self):
        self.independentCtrlWidget.hide()
        self.autoRunningWidget.show()
    def rtcTimeout(self):
        """ real time """
        self.mainWindow.timeLabel.setText(QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"))
    def getVersion(self):
        return "PyQt Version {}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])

    def creatSubDev(self, subDevList, whichGroup):
        count = 0
        for item in Config.getGroupValue(whichGroup):
            try:
                if ":" in item[1]:
                    key, name, pos = str(item[1]).split(":")
                else:
                    name = item[1]
                    pos = 1000
                button = PushButtonWithAttr(pos)
                button.setText(name)
                subDevList.append(button)
                button.clicked.connect(self.onAllSubDevPushButtonClicked)
                count += 1
            except: pass
    def onSettingPushButtonClicked(self):
        # todo get data from server
        self.settingDialog.exec_()
    def onAllSubDevPushButtonClicked(self):
        button = self.sender()
        if isinstance(self.forbidDevDialog, ForbidDevDialog) and self.forbidDevDialog.isVisible():
            if button.isChecked():
                button.isUsed = False
                button.setToolTip("设备已禁用")
                print(button.text(), "设备已禁用")
            else:
                button.isUsed = True
                button.setToolTip("设备已启用")
                print(button.text(), "设备已启用")
        else:
            print(button.text(), "设备已选中")
    def test(self):
        print("kkk")

    def onForbidDevDialog(self):
        self.forbidDevDialog.createAllWidget(self.subDevList)
        self.forbidDevDialog.exec_()
        self.independentCtrlWidget.showAllDev(self.subDevList)
    def onAccountManagement(self):
        a = SystemManagement()
        a.exec_()
    def closeEvent(self, event):
        return
        reply = QMessageBox.question(self,
                                     "quit application",
                                     "Don't you want to quit application",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            event.ignore()
        else:
            event.accept()
