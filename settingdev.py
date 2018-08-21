# /usr/bin/env python
# -*- coding:utf-8 -*-

from ui import ui_settingdev
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from subdevattr import SubDevAttr


class SettingDevUnit(QWidget):
    def __init__(self, subDev=None):
        super().__init__()
        if subDev is not None:
            idLabel = QLabel(subDev.devKey)
            idLabel.setAlignment(Qt.AlignHCenter)
            nameLabel = QLabel(subDev.text())
            nameLabel.setFrameShadow(QFrame.Raised)
            nameLabel.setFrameShape(QFrame.Box)
            nameLabel.setAlignment(Qt.AlignHCenter)
            onStagetCheckBox = QCheckBox("上极限")
            offStageCheckBox = QCheckBox("下极限")
            onStagetCheckBox.setEnabled(False)
            offStageCheckBox.setEnabled(False)
            hLayout = QHBoxLayout()
            hLayout.addWidget(onStagetCheckBox)
            hLayout.addWidget(offStageCheckBox)
            vLayout = QVBoxLayout()
            vLayout.addWidget(idLabel)
            vLayout.addWidget(nameLabel)
            vLayout.addLayout(hLayout)
            subDev.setFixedSize(100, 50)
            vLayout.addWidget(subDev, alignment=Qt.AlignHCenter)
            self.setLayout(vLayout)
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        else:
            idLabel = QLabel("please input subdev")
            self.layout = QVBoxLayout()
            self.layout.addWidget(idLabel)
            self.setLayout(self.layout)

class SettingDevDialog(QDialog, ui_settingdev.Ui_SettingDevDialog):
    PartialOperation = 1<<2
    def __init__(self, subDevList):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags()|Qt.FramelessWindowHint)
        self.vLayout = QVBoxLayout()
        self.contentFrame.setLayout(self.vLayout)
        self.holdSelectedDev = []
        self.widgetNumber = 0
        self.buttonGroup = QButtonGroup()
        # self.createAllWidget(self.buttonGroup, subDevList, self.widgetNumber)
        self.nextPushButton.clicked.connect(self.onNextPushButtonClicked)
        self.previousPushButton.clicked.connect(self.onPreviousPushButtonClicked)
    def createAllWidget(self, buttonGroup, subDevList, num = 0):
        count = 0
        self.widgetList = []
        for subList in subDevList:
            for item in subList:
                if item.isChecked() and not item.isPartialCircuit:
                    item.setChecked(False)
                    self.holdSelectedDev.append(item)
                elif item.isPartialCircuit:
                    item.setChecked(True)
                    item.isPartialCircuit = False
                buttonGroup.addButton(item)
                self.buttonGroup.addButton(QPushButton())
                if item.isUpLimited or item.isDownLimited:
                    item.setEnabled(False)
                if count%28 == 0:
                    hCount = 0
                    vCount = 0
                    subWidget = QWidget()
                    layout = QGridLayout()
                    subWidget.setLayout(layout)
                    self.widgetList.append(subWidget)
                    self.vLayout.addWidget(subWidget)
                layout.addWidget(SettingDevUnit(item), hCount, vCount)
                vCount += 1
                if vCount >= 7:
                    vCount = 0
                    hCount += 1
                count += 1
        self.showSubWidget(num)
    def showSubWidget(self, num):
        for i in range(len(self.widgetList)):
            self.widgetList[i].setVisible(False)
        self.widgetList[num].setVisible(True)
        self.indexLabel.setText("{}/{}".format(num+1, len(self.widgetList)))
        self.repaint()
    def onNextPushButtonClicked(self):
        self.widgetNumber += 1
        self.showSubWidget(self.widgetNumber % len(self.widgetList))

    def onPreviousPushButtonClicked(self):
        if self.widgetNumber > 0:
            self.widgetNumber -= 1
        else:
            self.widgetNumber = len(self.widgetList) - 1
        self.showSubWidget(self.widgetNumber % len(self.widgetList))
    def closeEvent(self, QCloseEvent):
        self.doneSomthing(False)
        QCloseEvent.accept()
    def accept(self):
        self.doneSomthing(True)
        self.done(True)
    def reject(self):
        self.doneSomthing(False)
        self.done(False)
    def doneSomthing(self, retValue):
        try:
            partialDevSelected = self.buttonGroup.checkedButton()
            del self.buttonGroup
            if partialDevSelected is None:
                for item in self.holdSelectedDev:
                    item.setChecked(True)
                return
            if retValue:
                for item in self.holdSelectedDev: # Todo: 旁路设备是否应该禁用已经选中设备？
                    # item.clicked.emit(False)
                    item.setChecked(True)
                partialDevSelected.isPartialCircuit = True
                print(partialDevSelected.text(), "设备旁路已选中 id = ", partialDevSelected.devKey)
            else: # 选中， 未确认
                partialDevSelected.isPartialCircuit = False
                partialDevSelected.setChecked(False)
                # partialDevSelected.clicked.emit(False)
                for item in self.holdSelectedDev:
                    item.setChecked(True)
        except Exception as e:
            print("doneSomthing", str(e))



