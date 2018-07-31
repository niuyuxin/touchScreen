#!/usr/bin/env python
# -*- coding:utf8 -*-

from ui import ui_singlectrlwidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from config import *

class SingleCtrlWidget(QWidget, ui_singlectrlwidget.Ui_SingleCtrlWidget):
    selectedList = pyqtSignal(list)
    def __init__(self, subDevList, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.devButtonGroup = QButtonGroup(self)
        self.devButtonGroup.setExclusive(False)
        self.devButtonGroup.buttonPressed.connect(self.onDevButtonGroupPressed)
        self.allDevList = subDevList
        self.deviceStateList = {}
        self.showAllDev(self.allDevList)
        """ up dev and down dev selection """
        self.devSelectButtonGroup = QButtonGroup()
        self.devSelectButtonGroup.setExclusive(True)
        self.devSelectButtonGroup.addButton(self.subDownDevPushButton)
        self.devSelectButtonGroup.addButton(self.subUpDevPushButton)
        self.subUpDevPushButton.clicked.connect(self.onDevSelect)
        self.subDownDevPushButton.clicked.connect(self.onDevSelect)
        self.subUpDevPushButton.animateClick()
        self.cancelPushButton.clicked.connect(self.onCancelPushButtonClicked)
        self.confirmPushButton.clicked.connect(self.onConfirmPushButtonClicked)
        self.userConfirmButtonGroup = QButtonGroup(self)
        self.userConfirmButtonGroup.addButton(self.cancelPushButton)
        self.userConfirmButtonGroup.addButton(self.confirmPushButton)

    def onDevSelect(self, whichArea):
        button = self.sender()
        if button is None or not isinstance(button, QPushButton):
            return
        if button == self.subUpDevPushButton and whichArea:
            self.subDownDevScrollArea.hide()
            self.subUpDevScrollArea.show()
        elif button == self.subDownDevPushButton and whichArea:
            self.subUpDevScrollArea.hide()
            self.subDownDevScrollArea.show()

    def showAllDev(self, subDevList):
        """show all device in up-stage and down-stage form """
        allSelectedDev = []
        for sec, devList in self.deviceStateList.items():
            if sec != Config.monitorId:
                for dev in devList:
                    allSelectedDev.append(dev)
        for i in range(len(subDevList)):
            count = 0
            widget = QWidget()
            gridLayout = QGridLayout()
            gridLayout.setSpacing(10)
            widget.setLayout(gridLayout)
            for subDev in subDevList[i]:
                self.devButtonGroup.addButton(subDev)
                subDev.setFixedSize(100, 100)
                if not subDev.isUsed:
                    subDev.setEnabled(False)
                elif subDev.text() in allSelectedDev:
                    subDev.setEnabled(False)
                    subDev.setToolTip(self.tr("设备已在其他区域选中"))
                else:
                    subDev.setToolTip("")
                    subDev.setEnabled(True)
                if i == 0:
                    self.subUpDevScrollArea.setWidget(widget)
                else:
                    self.subDownDevScrollArea.setWidget(widget)
                gridLayout.addWidget(subDev, count/10, count%10)
                count += 1
    def onCancelPushButtonClicked(self):
        for item in self.searchCheckedButton(self.allDevList):
            item.setChecked(False)
            print(item.text(), "已取消选中")
        self.selectedList.emit([])
    def onConfirmPushButtonClicked(self):
        self.selectedList.emit(self.searchCheckedButton(self.allDevList))

    def searchCheckedButton(self, allDevList):
        checkedList = []
        for devList in allDevList:
            for item in devList:
                if item.isUsed and item.isChecked():
                    checkedList.append(item)
        return checkedList

    def onDevButtonGroupPressed(self):
        self.cancelPushButton.setChecked(True)

    @pyqtSlot(str, dict)
    def onHandleExternOrder(self, o, info):
        try:
            if o == "ForbiddenDevice":
                self.setEnabled(not info["Enable"])
            elif o == "DeviceStateChanged":
                sec = info["Section"]
                deviceList = info["Device"]
                if sec in self.deviceStateList.keys():
                    self.releaseSelectedDevice(self.deviceStateList[sec])
                self.deviceStateList[sec] = deviceList
                self.forbidSelectedDevice()
            else:
                print("Unknow order", o)
        except Exception as e:
            print("Error: onHandleExternOrder", str(e))
    def releaseSelectedDevice(self, devList):
        for dev in devList:
            self.getDeviceFromDevList(dev[0]).setEnabled(True)

    def forbidSelectedDevice(self):
        for sec, devList in self.deviceStateList.items():
            if sec == Config.monitorId:
                pass
            else:
                for dev in devList:
                    self.getDeviceFromDevList(dev[0]).setEnabled(False)

    def getDeviceFromDevList(self, name):
        for temp in self.allDevList:
            for subDev in temp:
                if name == subDev.text():
                    return subDev

