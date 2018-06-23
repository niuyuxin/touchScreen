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
        self.showAllDev()
        self.setWindowTitle("TouchScreen")
        self.mainWindow.settingPushButton.clicked.connect(self.onSettingPushButtonClicked)
        self.init_mainWindow()
    def init_mainWindow(self):
        """ up dev and down dev selection """
        self.devSelectButtonGroup = QButtonGroup()
        self.devSelectButtonGroup.setExclusive(True)
        self.devSelectButtonGroup.addButton(self.mainWindow.subDownDevPushButton)
        self.devSelectButtonGroup.addButton(self.mainWindow.subUpDevPushButton)
        self.mainWindow.subUpDevPushButton.clicked.connect(self.onDevSelect)
        self.mainWindow.subDownDevPushButton.clicked.connect(self.onDevSelect)
        self.mainWindow.subUpDevPushButton.animateClick()
        """ initialization database """
        self.settingDialog = SettingDialog()
        try:
            self.dataBaseThread = QThread()
            self.dataBase = DataBase()
            self.settingDialog.saveSetting.connect(self.dataBase.insertRecord)
            self.settingDialog.getSetting.connect(self.dataBase.selectRecord)
            self.dataBase.moveToThread(self.dataBaseThread)
        except DataBaseException as err:
            QMessageBox.warning(self,
                                "DataBaseError",
                                str(err),
                                QMessageBox.Yes)
        """ Forbidded dev dialog signals """
        self.forbidDevDialog = 0 # ForbidDevDialog(self.subDevList)
        self.mainWindow.forbidDevPushButton.clicked.connect(self.onForbidDevDialog)
    def onDevSelect(self, whichArea):
        button = self.sender()
        if button is None or not isinstance(button, QPushButton):
            return
        if button == self.mainWindow.subUpDevPushButton and whichArea:
            self.mainWindow.subDownDevScrollArea.hide()
            self.mainWindow.subUpDevScrollArea.show()
        elif button == self.mainWindow.subDownDevPushButton and whichArea:
            self.mainWindow.subUpDevScrollArea.hide()
            self.mainWindow.subDownDevScrollArea.show()
    def rtcTimeout(self):
        """ 实时时钟
        """
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
                button.clicked.connect(self.onSubDevPushButtonAllClicked)
                count += 1
            except: pass
    def onSettingPushButtonClicked(self):
        # todo get data from server
        self.settingDialog.exec_()
    def onSubDevPushButtonAllClicked(self):
        button = self.sender()
        if isinstance(self.forbidDevDialog, ForbidDevDialog) and self.forbidDevDialog.isVisible():
            if button.isChecked():
                button.isUsed = False
                button.setToolTip("设备已禁用")
            else:
                button.isUsed = True
                button.setToolTip("设备已启用")
            print(button.text())

    def test(self):
        print("kkk")

    def onForbidDevDialog(self):
        self.forbidDevDialog = ForbidDevDialog(self.subDevList)
        self.forbidDevDialog.exec_()
        self.showAllDev()
    def showAllDev(self):
        """show all device in up-stage and down stage form """
        for i in range(len(self.subDevList)):
            count = 0
            widget = QWidget()
            gridLayout = QGridLayout()
            widget.setLayout(gridLayout)
            for subDev in self.subDevList[i]:
                if not subDev.isUsed:
                    subDev.setEnabled(False)
                else:
                    subDev.setToolTip("")
                    subDev.setEnabled(True)
                if i == 0:
                    self.mainWindow.subUpDevScrollArea.setWidget(widget)
                else:
                    self.mainWindow.subDownDevScrollArea.setWidget(widget)
                gridLayout.addWidget(subDev, count/10, count%10)
                count += 1

    def closeEvent(self, event):
        return
        reply = QMessageBox.question(self,
                                     "quit application",
                                     "Don't you want to quit application",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            event.ignore()
