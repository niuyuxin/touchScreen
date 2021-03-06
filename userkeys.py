#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from config import *

class UserKeysUnit(QPushButton):
    def __init__(self, name, key, specKey, iod, speed, parent = None):
        super().__init__(parent)
        self.setObjectName("UserKeysUnit")
        self.indexOfDev = iod
        self.name = name
        self.selfKey = key
        self.specificDevKey = specKey
        self.func = ""
        self.speed = speed
        self.pos = 100
        self.absPos = 100
        self.relPos = 100
        self.zeroPos = 0
        self.setFixedSize(100, 30)
        self.setStyleSheet("background-color: rgba(0, 50, 50, 50)")
        self.setText(name)


class UserKeysDialog(QDialog):
    def __init__(self, allDevList, userKeysList):
        super().__init__()
        self.setWindowFlags(self.windowFlags()|Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.WheelFocus)
        self.currentUserkey = None
        self.subDevList = allDevList
        self.userKeysList = userKeysList
        # create attribute widget
        self.keysAttrGroupBox = QGroupBox()
        self.keysAttrGroupBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.keysAttrLayout = QGridLayout()
        self.renameLabel = QLabel(self.tr("按键重命名："))
        self.renameLineEdit = QLineEdit("...")
        self.keysAttrLayout.addWidget(self.renameLabel, 0, 0)
        self.keysAttrLayout.addWidget(self.renameLineEdit, 0, 1, 1, 2)
        self.functionLabel = QLabel(self.tr("功能指定："))
        self.functionComboBox = QComboBox()
        self.functionComboBox.addItem(self.tr("上升"))
        self.functionComboBox.addItem(self.tr("下降"))
        self.keysAttrLayout.addWidget(self.functionLabel, 1, 0)
        self.keysAttrLayout.addWidget(self.functionComboBox, 1, 1, 1, 2)

        self.deviceAssignedLabel = QLabel(self.tr("设备指定："))
        self.devAssignedComboBox = QComboBox()
        self.devAssignedComboBox.currentIndexChanged.connect(self.onDevAssignedComboBoxCurrentIndexChanged)
        self.keysAttrLayout.addWidget(self.deviceAssignedLabel, 2, 0)
        self.keysAttrLayout.addWidget(self.devAssignedComboBox, 2, 1, 1, 2)

        self.speedLabel = QLabel(self.tr("速度："))
        self.speedSpinBox = QSpinBox()
        self.speedSpinBox.setMaximum(1000)
        self.keysAttrLayout.addWidget(self.speedLabel, 3, 0)
        self.keysAttrLayout.addWidget(self.speedSpinBox, 3, 1, 1, 2)
        self.posLabel = QLabel(self.tr("位置："))
        self.posSpinBox = QSpinBox()
        self.posSpinBox.setMaximum(1000)
        self.keysAttrLayout.addWidget(self.posLabel, 4, 0)
        self.keysAttrLayout.addWidget(self.posSpinBox, 4, 1, 1, 2)
        self.relPosLabel = QLabel(self.tr("相对位置："))
        self.relPosSpinBox = QSpinBox()
        self.relPosSpinBox.setMaximum(1000)
        self.keysAttrLayout.addWidget(self.relPosLabel, 5, 0)
        self.keysAttrLayout.addWidget(self.relPosSpinBox, 5, 1, 1, 2)
        self.absPosLabel = QLabel(self.tr("绝对位置："))
        self.absPosSpinBox = QSpinBox()
        self.absPosSpinBox.setMaximum(1000)
        self.keysAttrLayout.addWidget(self.absPosLabel, 6, 0)
        self.keysAttrLayout.addWidget(self.absPosSpinBox, 6, 1, 1, 2)
        self.zeroPosLabel = QLabel(self.tr("零位置："))
        self.zeroPosSpinBox = QSpinBox()
        self.zeroPosSpinBox.setMaximum(1000)
        self.keysAttrLayout.addWidget(self.zeroPosLabel, 7, 0)
        self.keysAttrLayout.addWidget(self.zeroPosSpinBox, 7, 1, 1, 2)
        self.keysAttrGroupBox.setLayout(self.keysAttrLayout)
        self.applyPushButton = QPushButton(self.tr("应用"))
        self.applyPushButton.setObjectName("userKeysApplyPushButton")
        self.cancelPushButton = QPushButton(self.tr("取消"))
        self.cancelPushButton.setObjectName("userKeysCancelPushButton")
        self.keysAttrLayout.addWidget(self.applyPushButton, 8, 1)
        self.keysAttrLayout.addWidget(self.cancelPushButton, 8, 2)
        self.applyPushButton.clicked.connect(self.onApplyPushButtonClicked)
        self.cancelPushButton.clicked.connect(self.onCancelPushButtonClicked)
        # create button group
        self.setWindowTitle(self.tr("按键自定义"))
        self.buttonGroupBox = QGroupBox()
        self.keysLayout = QVBoxLayout(self.buttonGroupBox)
        self.userButtonGroup = QButtonGroup()
        self.userButtonGroup.buttonPressed.connect(self.onUserButtonGroupButtonPressed)
        for button in self.userKeysList:
            button.show()
            button.setCheckable(True)
            button.setEnabled(True)
            self.userButtonGroup.addButton(button)
            self.keysLayout.addWidget(button)
        self.devAssignedComboBox.addItem("None")
        for dev in self.subDevList: # set all dev
            self.devAssignedComboBox.addItem(self.tr(dev.text()))
        self.secondaryLayout = QHBoxLayout()
        self.secondaryLayout.addWidget(self.buttonGroupBox)
        self.secondaryLayout.addWidget(self.keysAttrGroupBox)
        self.mainLayout = QVBoxLayout(self)
        self.userKeysTipsLabel = QLabel(self.tr("请先选择按键， 再更改属性"))
        self.userKeysTipsLabel.setAlignment(Qt.AlignHCenter)
        self.setObjectName("userKeysTipsLabel")
        self.mainLayout.addWidget(self.userKeysTipsLabel)

        self.mainLayout.addLayout(self.secondaryLayout)
        self.exitPushButton = QPushButton("退出")
        self.exitPushButton.setObjectName("userKeysExitPushButton")
        self.exitPushButton.clicked.connect(self.close)
        self.mainLayout.addWidget(self.exitPushButton, 0, Qt.AlignRight)
        # self.setLayout(self.mainLayout)
        self.cancelPushButton.setDefault(True)
    def onUserButtonGroupButtonPressed(self, button):
        try:
            self.renameLineEdit.setText(button.text())
            self.currentUserkey = button
            self.devAssignedComboBox.setCurrentIndex(button.indexOfDev+1) # first item is none， so...
            self.speedSpinBox.setValue(button.speed)
        except Exception as err:
            print(str(err))
    def onApplyPushButtonClicked(self):
        retValue = self.checkUserInput(self.devAssignedComboBox.currentIndex()-1) #
        if retValue is not None:
            ret = QMessageBox.warning(self,
                                self.tr("警告"),
                                retValue,
                                QMessageBox.Ok | QMessageBox.Cancel)
            if ret == QMessageBox.Ok:
                return
            else:
                self.accept()
        else:
            self.applyUserSelected(self.devAssignedComboBox.currentIndex()-1) # plus None item
    def onCancelPushButtonClicked(self):
        if self.currentUserkey is not None:
            self.currentUserkey.animateClick()
    def onDevAssignedComboBoxCurrentIndexChanged(self, index):
        if index != 0:
            dev = self.subDevList[index-1] # first item is None,
            try:
                self.posSpinBox.setEnabled(True)
                self.zeroPosSpinBox.setEnabled(True)
                self.posSpinBox.setValue(dev.currentPos)
                self.zeroPosSpinBox.setValue(dev.zeroPos)
            except Exception as err:
                print(str(err))
        else:
            self.posSpinBox.setEnabled(False)
            self.zeroPosSpinBox.setEnabled(False)
            self.absPosSpinBox.setEnabled(False)
            self.relPosSpinBox.setEnabled(False)
    def checkUserInput(self, index): # note: when check object for devAsignedComboBox, index should minus 1
        checkedButton = self.userButtonGroup.checkedButton()
        if checkedButton is None:
            notice = self.tr("请选择要指定的按键")
            return notice
        # if self.devAssignedComboBox.currentText() == "None":
        #     notice = self.tr("请选择要指定的设备")
        #     return notice
        for button in self.userKeysList:
            notice = None
            if button == checkedButton:
                pass
            else:
                if index != -1 and index == button.indexOfDev:
                    notice = self.tr("'{}' 已经指定到 '{}', 请重新选择设备".format(button.text(), self.devAssignedComboBox.currentText()))
                    return notice
                elif self.subDevList[index].isUsed == False:
                    notice = self.tr("'{}' 已被禁用， 请重新选择设备。".format(self.subDevList[index].text()))
        return notice
    def applyUserSelected(self, index): # note: devAsignedComboBox index should minus 1
        if self.currentUserkey is not None: # there has no necessary to check this parameter
            if index == self.currentUserkey.indexOfDev:  # same device specification...
                return
            if self.currentUserkey.indexOfDev != -1: # had specific some device
                # self.subDevList[self.currentUserkey.indexOfDev].setChecked(False)
                # self.subDevList[self.currentUserkey.indexOfDev].setEnabled(True)
                self.subDevList[self.currentUserkey.indexOfDev].isReplaced = False # cancel
            else:
                pass
            currentButton = self.userButtonGroup.checkedButton()
            self.currentUserkey.indexOfDev = index
            value = Config.value("UserKeys/{}".format(currentButton.selfKey))
            infoList = value.split(":")
            if index == -1: # cancel device specific, maybe this device is already specific to someone
                name = self.renameLineEdit.text()
                currentButton.setText(name)
                currentButton.specificDevKey = ""
                currentButton.speed = 0
                print("Todo: cancel device specific")
            else:
                try:
                    dev = self.subDevList[index]
                    # dev.setChecked(False)
                    # dev.setEnabled(False)
                    dev.isReplaced = True
                    name = self.renameLineEdit.text()
                    currentButton.setText(name)
                    currentButton.specificDevKey = self.subDevList[index].devKey
                    currentButton.speed = self.speedSpinBox.value()
                    print("Todo: update new button parameter")
                except Exception as e:
                    print(str(e))
            key = "UserKeys/{}".format(currentButton.selfKey)
            value = "{}:{}:{}:{}".format(infoList[0], currentButton.text(), currentButton.speed, currentButton.specificDevKey)
            print(key, value)
            Config.setValue(key, value)
    def hideEvent(self, QCloseEvent):
        self.doSomthingForExit()
        pass
    def doSomthingForExit(self):
        for button in self.userKeysList:
            self.userButtonGroup.removeButton(button)
            button.setChecked(False)
            button.setEnabled(False)
    def showEvent(self, QShowEvent):
        self.move(self.pos())