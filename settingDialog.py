#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from config import Config
from ui import ui_settingpara
from ui import ui_settingdialog


class SettingParaWidget(QWidget, ui_settingpara.Ui_SettingPara):
    doneSetting = pyqtSignal(bool)
    def __init__(self, name = "", parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.devNameLabel.setText(name)
        self.settingParaButtonBox.accepted.connect(self.accept)
        self.settingParaButtonBox.rejected.connect(self.reject)
    def accept(self):
        self.doneSetting.emit(True)
    def reject(self):
        self.doneSetting.emit(False)

class SettingDialog(QDialog):
    saveSetting = pyqtSignal(str, dict)
    getSetting = pyqtSignal(str, dict)
    def __init__(self, parent = None):
        super().__init__(parent)
        self.context = ui_settingdialog.Ui_SettingDialog()
        self.context.setupUi(self)
        self.setWindowTitle("Setting Device Parameter")
        self.showAllSettingItems()

    def showAllSettingItems(self):
        devList = []
        devGroupList = []
        count = 1
        allList = Config.getGroupValue("SubDevUpStage") + Config.getGroupValue("SubDevDownStage")
        for item in allList:
            devList.append(tuple(str(item[1]).split(":")))
            if not count%15:
                devGroupList.append(devList)
                devList = []
            count += 1
        devGroupList.append(devList)
        for tab in devGroupList:
            vCount = 0
            hCount = 0
            widget = QWidget()
            gridLayout = QGridLayout()
            self.context.tabWidget.addTab(widget, "#######")
            for item in tab:
                sp = SettingParaWidget(item[1])
                sp.doneSetting.connect(self.somthingChanged)
                gridLayout.addWidget(sp, hCount, vCount)
                vCount += 1
                if vCount >= 5:
                    vCount = 0
                    hCount += 1
            widget.setLayout(gridLayout)
    def somthingChanged(self, s):
        spw = self.sender()
        if spw is None or not isinstance(spw, SettingParaWidget):
            return
        d = {"name":spw.devNameLabel.text(),
             "currentPos":spw.currentPosSpinBox.value(),
             "upLimitedPos":spw.upLimittedPosSpinBox.value(),
             "downLimitedPos":spw.downLimittedPosSpinBox.value(),
             "zeroPos":spw.zeroPosSpinBox.value()}
        if s:
            print("Send parameter to Server!") # todo
            # self.saveSetting.emit("DeviceInfo", d)
        else:
            print("Get parameter from Server") # todo
            # self.getSetting.emit("DeviceInfo", d)
    def showEvent(self, QShowEvent):
        self.getSetting.emit("", dict()) # todo