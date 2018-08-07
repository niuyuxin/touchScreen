#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from config import Config
from ui import ui_settingpara
from ui import ui_settingdialog
from PyQt5.QtCore import *
from subdevattr import  *
from tcpsocket import *

class SettingParaWidget(QWidget, ui_settingpara.Ui_SettingPara):
    doneSetting = pyqtSignal(bool)
    def __init__(self, dev, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.device = dev
        self.device.valueChanged.connect(self.onDevValueChanged)
        self.devNameLabel.setText(dev.text())
        self.actualPosLabel.setText(str(dev.currentPos))
        self.calPosSpinBox.setValue(dev.targetPos)
        self.upLimittedPosSpinBox.setValue(dev.upLimitedPos)
        self.downLimittedPosSpinBox.setValue(dev.downLimitedPos)
        self.zeroPosLabel.setText(str(dev.zeroPos))
        self.settingParaButtonBox.accepted.connect(self.accept)
        self.settingParaButtonBox.rejected.connect(self.reject)

    def accept(self):
        self.device.targetPos = self.calPosSpinBox.value()
        self.device.upLimitedPos = self.upLimittedPosSpinBox.value()
        self.device.downLimitedPos = self.downLimittedPosSpinBox.value()
        self.doneSetting.emit(True)

    def reject(self):
        self.calPosSpinBox.setValue(self.device.targetPos)
        self.upLimittedPosSpinBox.setValue(self.device.upLimitedPos)
        self.downLimittedPosSpinBox.setValue(self.device.downLimitedPos)
        self.doneSetting.emit(False)

    def onDevValueChanged(self):
        dev = self.sender()
        if not isinstance(dev, SubDevAttr):
            return
        self.actualPosLabel.setText(str(dev.currentPos))
        self.calPosSpinBox.setValue(dev.targetPos)
        self.upLimittedPosSpinBox.setValue(dev.upLimitedPos)
        self.downLimittedPosSpinBox.setValue(dev.downLimitedPos)
        self.zeroPosLabel.setText(str(dev.zeroPos))
        pass
class ParaSetting(QDialog):
    """
        参数设定界面
    """
    sendDataToTcpSocket = pyqtSignal(int, str, dict)
    def __init__(self, allDev, parent = None):
        super().__init__(parent)
        self.context = ui_settingdialog.Ui_SettingDialog()
        self.context.setupUi(self)
        self.context.cancelPushButton.setDefault(True)
        self.setWindowTitle("Setting Device Parameter")
        self.readyAllSettingItems(allDev)
        self.setFocusPolicy(Qt.WheelFocus)

    def readyAllSettingItems(self, allDevList):
        """ set TabWidget items, each tabWidget 15 items
            allDevList include on the stage and off the stage device
        """
        devList = []
        devListGroup = []
        count = 1
        allList = allDevList
        for dev in allList:
            devList.append(dev)
            if not count%21:
                devListGroup.append(devList)
                devList = []
            count += 1
        devListGroup.append(devList) # 追加不足 18 个元素的数据为一组
        for groupItem in devListGroup:
            vCount = 0
            hCount = 0
            widget = QWidget()
            gridLayout = QGridLayout()
            for item in groupItem:
                sp = SettingParaWidget(item)
                sp.doneSetting.connect(self.somthingChanged)
                gridLayout.addWidget(sp, hCount, vCount)
                vCount += 1
                if vCount >= 7:
                    vCount = 0
                    hCount += 1
            widget.setLayout(gridLayout)
            self.context.tabWidget.addTab(widget, " 第 {} 页".format(devListGroup.index(groupItem)+1))

    def somthingChanged(self, s):
        spw = self.sender()
        if spw is None or not isinstance(spw, SettingParaWidget):
            return
        print("{} is setting...".format(spw.device.text()))
        self.sendDataToTcpSocket.emit(TcpSocket.Call, TcpSocket.ParaSetting,
                                      {"DevId":spw.device.devId,
                                        "targetPos":spw.device.targetPos,
                                       "UpLimited":spw.device.upLimitedPos,
                                       "DownLimited":spw.device.downLimitedPos
                                       })
