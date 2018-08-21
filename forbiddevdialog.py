#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui import ui_forbiddevdialog

class ForbidDevDialog(QDialog, ui_forbiddevdialog.Ui_ForbidDevDialog):
    ForbiddenOperation = 1<<1
    def __init__(self, subDevList):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModal)
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.previousPushButton)
        self.buttonGroup.addButton(self.nextPushButton)
        self.buttonGroup.setExclusive(True)
        self.vLayout = QVBoxLayout()
        self.forbidDevFrame.setLayout(self.vLayout)
        self.widgetNumber = 0
        # self.createAllWidget(subDevList, self.widgetNumber)
        self.nextPushButton.clicked.connect(self.onNextPushButtonClicked)
        self.previousPushButton.clicked.connect(self.onPreviousPushButtonClicked)
    def createAllWidget(self, subDevList, num = 0):
        count = 0
        self.widgetList = []
        for subList in subDevList:
            for item in subList:
                if item.isChecked() and item.isUsed:
                    item.setEnabled(False)
                    item.setToolTip("设备已启用")
                elif item.isUsed == False:
                    item.setEnabled(True)
                    item.setChecked(True)
                if count%60 == 0:
                    hCount = 0
                    vCount = 0
                    subWidget = QWidget()
                    layout = QGridLayout()
                    subWidget.setLayout(layout)
                    self.widgetList.append(subWidget)
                    self.vLayout.addWidget(subWidget)
                layout.addWidget(item, hCount, vCount)
                vCount += 1
                if vCount >= 12:
                    vCount = 0
                    hCount += 1
                count += 1
        self.showSubWidget(num)
    def showSubWidget(self, num):
        for i in range(len(self.widgetList)):
            self.widgetList[i].setVisible(False)
        self.widgetList[num].setVisible(True)
        self.repaint()

    def onNextPushButtonClicked(self):
        self.widgetNumber += 1
        self.showSubWidget(self.widgetNumber%len(self.widgetList))
    def onPreviousPushButtonClicked(self):
        if self.widgetNumber > 0:
            self.widgetNumber -= 1
        else:
            self.widgetNumber = len(self.widgetList)-1
        self.showSubWidget(self.widgetNumber % len(self.widgetList))
