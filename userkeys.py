#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *

class UserKeysUnit(QPushButton):
    def __init__(self, name, parent=0):
        super().__init__(parent)
        self.name = "name"
        self.func = ""
        self.speed = 100
        self.pos = 100
        self.absPos = 100
        self.relPos = 100
        self.zeroPos = 0
        self.setText(name)
        self.setCheckable(True)

class UserKyesDialog(QDialog):
    def __init__(self, subDelList):
        super().__init__()
        self.subDevList = []
        for devList in subDelList:
            self.subDevList.extend(devList)
        # create attribute widget
        keysAttrGroupBox = QGroupBox(self.tr("属性"))
        keysAttrGroupBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        keysAttrLayout = QGridLayout()
        renameLabel = QLabel(self.tr("按键重命名："))
        self.renameLineEdit = QLineEdit("...")
        keysAttrLayout.addWidget(renameLabel, 0, 0)
        keysAttrLayout.addWidget(self.renameLineEdit, 0, 1, 1, 2)
        functionLabel = QLabel(self.tr("功能指定："))
        self.functionComboBox = QComboBox()
        self.functionComboBox.addItem(self.tr("上升"))
        self.functionComboBox.addItem(self.tr("下降"))
        keysAttrLayout.addWidget(functionLabel, 1, 0)
        keysAttrLayout.addWidget(self.functionComboBox, 1, 1, 1, 2)

        deviceAssignedLabel = QLabel(self.tr("设备指定："))
        self.devAssignedComboxBox = QComboBox()
        self.devAssignedComboxBox.currentIndexChanged.connect(self.onDevAssignedComboxBoxCurrentIndexChanged)
        keysAttrLayout.addWidget(deviceAssignedLabel, 2, 0)
        keysAttrLayout.addWidget(self.devAssignedComboxBox, 2, 1, 1, 2)

        speedLabel = QLabel(self.tr("速度："))
        self.speedSpinBox = QSpinBox()
        self.speedSpinBox.setMaximum(1000)
        keysAttrLayout.addWidget(speedLabel, 3, 0)
        keysAttrLayout.addWidget(self.speedSpinBox, 3, 1, 1, 2)
        posLabel = QLabel(self.tr("位置："))
        self.posSpinBox = QSpinBox()
        self.posSpinBox.setMaximum(1000)
        keysAttrLayout.addWidget(posLabel, 4, 0)
        keysAttrLayout.addWidget(self.posSpinBox, 4, 1, 1, 2)
        relPosLabel = QLabel(self.tr("相对位置："))
        self.relPosSpinBox = QSpinBox()
        self.relPosSpinBox.setMaximum(1000)
        keysAttrLayout.addWidget(relPosLabel, 5, 0)
        keysAttrLayout.addWidget(self.relPosSpinBox, 5, 1, 1, 2)
        absPosLabel = QLabel(self.tr("绝对位置："))
        self.absPosSpinBox = QSpinBox()
        self.absPosSpinBox.setMaximum(1000)
        keysAttrLayout.addWidget(absPosLabel, 6, 0)
        keysAttrLayout.addWidget(self.absPosSpinBox, 6, 1, 1, 2)
        zeroPosLabel = QLabel(self.tr("零位置："))
        self.zeroPosSpinBox = QSpinBox()
        self.zeroPosSpinBox.setMaximum(1000)
        keysAttrLayout.addWidget(zeroPosLabel, 7, 0)
        keysAttrLayout.addWidget(self.zeroPosSpinBox, 7, 1, 1, 2)
        keysAttrGroupBox.setLayout(keysAttrLayout)
        applyPushButton = QPushButton(self.tr("应用"))
        cancelPushButton = QPushButton(self.tr("取消"))
        keysAttrLayout.addWidget(applyPushButton, 8, 1)
        keysAttrLayout.addWidget(cancelPushButton, 8, 2)
        applyPushButton.clicked.connect(self.onApplyPushButtonClicked)
        cancelPushButton.clicked.connect(self.onCancelPushButtonClicked)
        # create button group
        self.setWindowTitle(self.tr("按键自定义"))
        buttonGroupBox = QGroupBox(self.tr("按键"))
        keysLayout = QVBoxLayout()
        buttonGroupBox.setLayout(keysLayout)
        self.userButtonGroup = QButtonGroup()
        self.userButtonGroup.buttonPressed.connect(self.onUserButtonGroupButtonPressed)
        for dev in self.subDevList: # set dev
            self.devAssignedComboxBox.addItem(self.tr(dev.text()))
        for buttonNum in range(4):
            name = self.tr("按键{}").format(buttonNum)
            button = UserKeysUnit(name, buttonGroupBox)
            self.userButtonGroup.addButton(button)
            keysLayout.addWidget(button)
            if buttonNum == 0:
                button.animateClick()

        self.secondaryLayout = QHBoxLayout()
        self.secondaryLayout.addWidget(buttonGroupBox)
        self.secondaryLayout.addWidget(keysAttrGroupBox)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(QLabel(self.tr("请先选择按键， 再更改属性")))
        self.mainLayout.addLayout(self.secondaryLayout)
        self.setLayout(self.mainLayout)
    def onUserButtonGroupButtonPressed(self, button):
        self.renameLineEdit.setText(button.text())
    def onApplyPushButtonClicked(self):
        print("a")
    def onCancelPushButtonClicked(self):
        print("c")
    def onDevAssignedComboxBoxCurrentIndexChanged(self, index):
        dev = self.subDevList[index]
        self.posSpinBox.setValue(dev.currentPos)
        self.zeroPosSpinBox.setValue(dev.zeroPos)
