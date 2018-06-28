#!/usr/bin/env python
# -*- coding:utf8 -*-

from ui import ui_independentctrlwidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class IndependentCtrlWidget(QWidget, ui_independentctrlwidget.Ui_independentCtrlWidget):
    selectedList = pyqtSignal(list)
    def __init__(self, subDevList, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.allDevList = subDevList
        self.showAllDev(self.allDevList)
        """ up dev and down dev selection """
        self.devSelectButtonGroup = QButtonGroup()
        self.devSelectButtonGroup.setExclusive(True)
        self.devSelectButtonGroup.addButton(self.subDownDevPushButton)
        self.devSelectButtonGroup.addButton(self.subUpDevPushButton)
        self.subUpDevPushButton.clicked.connect(self.onDevSelect)
        self.subDownDevPushButton.clicked.connect(self.onDevSelect)
        self.subUpDevPushButton.animateClick()
        self.confirmButtonBox.rejected.connect(self.onConfirmButtonBoxReject)
        self.confirmButtonBox.accepted.connect(self.onConfirmButtonBoxAccept)

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
        for i in range(len(subDevList)):
            count = 0
            widget = QWidget()
            gridLayout = QGridLayout()
            gridLayout.setSpacing(10)
            widget.setLayout(gridLayout)
            for subDev in subDevList[i]:
                subDev.setFixedSize(100, 100)
                if not subDev.isUsed:
                    subDev.setEnabled(False)
                else:
                    subDev.setToolTip("")
                    subDev.setEnabled(True)
                if i == 0:
                    self.subUpDevScrollArea.setWidget(widget)
                else:
                    self.subDownDevScrollArea.setWidget(widget)
                gridLayout.addWidget(subDev, count/10, count%10)
                count += 1
    def onConfirmButtonBoxReject(self):
        for item in self.searchCheckedButton(self.allDevList):
            item.setChecked(False)
            print(item.text(), "已取消选中")
    def onConfirmButtonBoxAccept(self):
        #for item in self.searchCheckedButton(self.allDevList):
         #   print(item.text())
        self.selectedList.emit(self.searchCheckedButton(self.allDevList))
    def searchCheckedButton(self, allDevList):
        checkedList = []
        for devList in allDevList:
            for item in devList:
                if item.isUsed and item.isChecked():
                    checkedList.append(item)
        return checkedList