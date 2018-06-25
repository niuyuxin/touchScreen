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
    def __init__(self, allDev, parent = None):
        super().__init__(parent)
        self.context = ui_settingdialog.Ui_SettingDialog()
        self.context.setupUi(self)
        self.setWindowTitle("Setting Device Parameter")
        self.readyAllSettingItems(allDev)

    def readyAllSettingItems(self, allDevList):
        """ set TabWidget items, each tabWidget 15 items
            allDevList include on the stage and off the stage device
        """
        devList = []
        devListGroup = []
        count = 1
        allList = []
        for l in allDevList:
            allList.extend(l)
        for dev in allList:
            devList.append(dev)
            if not count%15:
                devListGroup.append(devList)
                devList = []
            count += 1
        devListGroup.append(devList) # 追加不足 15 个元素的数据为一组
        for groupItem in devListGroup:
            vCount = 0
            hCount = 0
            widget = QWidget()
            gridLayout = QGridLayout()
            for item in groupItem:
                sp = SettingParaWidget(item.text())
                sp.doneSetting.connect(self.somthingChanged)
                gridLayout.addWidget(sp, hCount, vCount)
                vCount += 1
                if vCount >= 5:
                    vCount = 0
                    hCount += 1
            widget.setLayout(gridLayout)
            self.context.tabWidget.addTab(widget, " 组 {} ".format(devListGroup.index(groupItem)+1))
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
            print("Send parameter to Server!", d) # todo
            # self.saveSetting.emit("DeviceInfo", d)
        else:
            print("Get parameter from Server", d) # todo
            # self.getSetting.emit("DeviceInfo", d)
    def showEvent(self, QShowEvent):
        self.getSetting.emit("Get data from server", dict()) # todo get data from server
