#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from config import Config
from ui import ui_settingpara
from ui import ui_settingdialog
from PyQt5.QtCore import *
from subdevattr import  *
from tcpsocket import *

class SettingParaWidget(QFrame, ui_settingpara.Ui_SettingPara):
    doneSetting = pyqtSignal(bool)
    def __init__(self, dev, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.device = dev
        self.setFixedSize(self.sizeHint())
        self.setFrameShape(QFrame.Box)
        self.device.valueChanged.connect(self.onDevValueChanged)
        self.devNameLabel.setText(dev.text())
        self.actualPosLabel.setText(str(dev.currentPos))
        regExp = QRegExp("[0-9]{0,6}")
        validator = QRegExpValidator(regExp)
        self.targetPosLineEdit.setText(str(dev.targetPos))
        self.targetPosLineEdit.setValidator(validator)
        self.upperLimitPosLineEdit.setText(str(dev.upLimitedPos))
        self.upperLimitPosLineEdit.setValidator(validator)
        self.lowerLimitPosLineEdit.setText(str(dev.downLimitedPos))
        self.lowerLimitPosLineEdit.setValidator(validator)
        self.zeroPosLabel.setText(str(dev.zeroPos))
        self.okPushButton.clicked.connect(self.accept)
        self.okPushButton.setFocusPolicy(Qt.NoFocus)
        self.cancelButton.clicked.connect(self.reject)
        self.cancelButton.setFocusPolicy(Qt.NoFocus)

    def accept(self):
        try:
            targetPos = int(self.targetPosLineEdit.text())
            upperLimitPos = int(self.upperLimitPosLineEdit.text())
            lowerLimitPos = int(self.lowerLimitPosLineEdit.text())
            if targetPos not in range(lowerLimitPos, upperLimitPos) or \
                lowerLimitPos > upperLimitPos:
                self.reject()
                return
            self.device.targetPos = targetPos
            self.device.upLimitedPos = upperLimitPos
            self.device.downLimitedPos = lowerLimitPos
            self.doneSetting.emit(True)
        except:pass

    def reject(self):
        self.targetPosLineEdit.setText(str(self.device.targetPos))
        self.upperLimitPosLineEdit.setText(str(self.device.upLimitedPos))
        self.lowerLimitPosLineEdit.setText(str(self.device.downLimitedPos))
        self.doneSetting.emit(False)

    def onDevValueChanged(self):
        try:
            dev = self.sender()
            if not isinstance(dev, SubDevAttr):
                return
            self.actualPosLabel.setText(str(dev.currentPos))
            self.targetPosLineEdit.setText(str(dev.targetPos))
            self.upperLimitPosLineEdit.setText(str(dev.upLimitedPos))
            self.lowerLimitPosLineEdit.setText(str(dev.downLimitedPos))
            self.zeroPosLabel.setText(str(dev.zeroPos))
        except: pass
class ParaSetting(QDialog):
    """
        参数设定界面
    """
    sendDataToTcpSocket = pyqtSignal(int, str, dict)
    def __init__(self, allDev, parent = None):
        super().__init__(parent)
        self.context = ui_settingdialog.Ui_SettingDialog()
        self.context.setupUi(self)
        # self.setWindowState(Qt.WindowMaximized)
        self.setWindowFlags(self.windowFlags()|Qt.FramelessWindowHint)
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
            if not count%18:
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
                if vCount >= 6:
                    vCount = 0
                    hCount += 1
            widget.setLayout(gridLayout)
            self.context.tabWidget.addTab(widget, " 第 {} 页".format(devListGroup.index(groupItem)+1))
        self.repaint()
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