# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(813, 577)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(mainWindow)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.companyNameLabel = QtWidgets.QLabel(mainWindow)
        self.companyNameLabel.setStyleSheet("background-color: rgb(0, 85, 255);")
        self.companyNameLabel.setObjectName("companyNameLabel")
        self.verticalLayout_3.addWidget(self.companyNameLabel)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.setting = QtWidgets.QGroupBox(mainWindow)
        self.setting.setObjectName("setting")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.setting)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.singleCtrlPushButton = QtWidgets.QPushButton(self.setting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.singleCtrlPushButton.sizePolicy().hasHeightForWidth())
        self.singleCtrlPushButton.setSizePolicy(sizePolicy)
        self.singleCtrlPushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.singleCtrlPushButton.setIconSize(QtCore.QSize(16, 16))
        self.singleCtrlPushButton.setObjectName("singleCtrlPushButton")
        self.verticalLayout_2.addWidget(self.singleCtrlPushButton)
        self.settingDataPushButton = QtWidgets.QPushButton(self.setting)
        self.settingDataPushButton.setObjectName("settingDataPushButton")
        self.verticalLayout_2.addWidget(self.settingDataPushButton)
        self.userKeysPushButton = QtWidgets.QPushButton(self.setting)
        self.userKeysPushButton.setObjectName("userKeysPushButton")
        self.verticalLayout_2.addWidget(self.userKeysPushButton)
        self.forbidDevPushButton = QtWidgets.QPushButton(self.setting)
        self.forbidDevPushButton.setObjectName("forbidDevPushButton")
        self.verticalLayout_2.addWidget(self.forbidDevPushButton)
        self.settingDevPushButton = QtWidgets.QPushButton(self.setting)
        self.settingDevPushButton.setObjectName("settingDevPushButton")
        self.verticalLayout_2.addWidget(self.settingDevPushButton)
        self.accountPushButton = QtWidgets.QPushButton(self.setting)
        self.accountPushButton.setObjectName("accountPushButton")
        self.verticalLayout_2.addWidget(self.accountPushButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.resetInverterPushButton = QtWidgets.QPushButton(self.setting)
        self.resetInverterPushButton.setObjectName("resetInverterPushButton")
        self.verticalLayout_2.addWidget(self.resetInverterPushButton)
        self.clearFaultPushButton = QtWidgets.QPushButton(self.setting)
        self.clearFaultPushButton.setObjectName("clearFaultPushButton")
        self.verticalLayout_2.addWidget(self.clearFaultPushButton)
        self.exitBushButton = QtWidgets.QPushButton(self.setting)
        self.exitBushButton.setObjectName("exitBushButton")
        self.verticalLayout_2.addWidget(self.exitBushButton)
        self.horizontalLayout_3.addWidget(self.setting)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.contextFrame = QtWidgets.QFrame(mainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contextFrame.sizePolicy().hasHeightForWidth())
        self.contextFrame.setSizePolicy(sizePolicy)
        self.contextFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.contextFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.contextFrame.setObjectName("contextFrame")
        self.verticalLayout.addWidget(self.contextFrame)
        self.analogControlGroupBox = QtWidgets.QGroupBox(mainWindow)
        self.analogControlGroupBox.setObjectName("analogControlGroupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.analogControlGroupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.analogControlGroupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)
        self.lcdNumber = QtWidgets.QLCDNumber(self.analogControlGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumber.sizePolicy().hasHeightForWidth())
        self.lcdNumber.setSizePolicy(sizePolicy)
        self.lcdNumber.setFrameShape(QtWidgets.QFrame.Box)
        self.lcdNumber.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumber.setProperty("value", 0.0)
        self.lcdNumber.setObjectName("lcdNumber")
        self.gridLayout_2.addWidget(self.lcdNumber, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.analogControlGroupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(self.analogControlGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setMinimumSize(QtCore.QSize(300, 0))
        self.horizontalSlider.setMaximum(1000)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout_2.addWidget(self.horizontalSlider, 1, 1, 1, 2)
        self.horizontalLayout_2.addLayout(self.gridLayout_2)
        self.raisePushButton = QtWidgets.QPushButton(self.analogControlGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.raisePushButton.sizePolicy().hasHeightForWidth())
        self.raisePushButton.setSizePolicy(sizePolicy)
        self.raisePushButton.setObjectName("raisePushButton")
        self.horizontalLayout_2.addWidget(self.raisePushButton)
        self.stopPushButton = QtWidgets.QPushButton(self.analogControlGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stopPushButton.sizePolicy().hasHeightForWidth())
        self.stopPushButton.setSizePolicy(sizePolicy)
        self.stopPushButton.setObjectName("stopPushButton")
        self.horizontalLayout_2.addWidget(self.stopPushButton)
        self.fallPushButton = QtWidgets.QPushButton(self.analogControlGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fallPushButton.sizePolicy().hasHeightForWidth())
        self.fallPushButton.setSizePolicy(sizePolicy)
        self.fallPushButton.setObjectName("fallPushButton")
        self.horizontalLayout_2.addWidget(self.fallPushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.modelLabel = QtWidgets.QLabel(self.analogControlGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modelLabel.sizePolicy().hasHeightForWidth())
        self.modelLabel.setSizePolicy(sizePolicy)
        self.modelLabel.setMinimumSize(QtCore.QSize(0, 80))
        self.modelLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.modelLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.modelLabel.setObjectName("modelLabel")
        self.horizontalLayout_2.addWidget(self.modelLabel)
        self.verticalLayout.addWidget(self.analogControlGroupBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.versionLabel = QtWidgets.QLabel(mainWindow)
        self.versionLabel.setObjectName("versionLabel")
        self.horizontalLayout.addWidget(self.versionLabel)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.internetLabel = QtWidgets.QLabel(mainWindow)
        self.internetLabel.setObjectName("internetLabel")
        self.horizontalLayout.addWidget(self.internetLabel)
        self.timeLabel = QtWidgets.QLabel(mainWindow)
        self.timeLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.timeLabel.setObjectName("timeLabel")
        self.horizontalLayout.addWidget(self.timeLabel)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(mainWindow)
        self.horizontalSlider.valueChanged['int'].connect(self.lcdNumber.display)
        self.exitBushButton.clicked.connect(mainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Form"))
        self.companyNameLabel.setText(_translate("mainWindow", "江苏时代演艺设备有限公司"))
        self.setting.setTitle(_translate("mainWindow", "设置"))
        self.singleCtrlPushButton.setText(_translate("mainWindow", "单控选择"))
        self.settingDataPushButton.setText(_translate("mainWindow", "设置数据"))
        self.userKeysPushButton.setText(_translate("mainWindow", "按键自定义"))
        self.forbidDevPushButton.setText(_translate("mainWindow", "禁用设置"))
        self.settingDevPushButton.setText(_translate("mainWindow", "设备设定"))
        self.accountPushButton.setText(_translate("mainWindow", "账号管理"))
        self.resetInverterPushButton.setText(_translate("mainWindow", "变频器复位"))
        self.clearFaultPushButton.setText(_translate("mainWindow", "清除故障信息"))
        self.exitBushButton.setText(_translate("mainWindow", "退出"))
        self.analogControlGroupBox.setTitle(_translate("mainWindow", "模拟操作"))
        self.label.setText(_translate("mainWindow", "速度rpm/min"))
        self.label_2.setText(_translate("mainWindow", "速度设置"))
        self.raisePushButton.setText(_translate("mainWindow", "上升"))
        self.stopPushButton.setText(_translate("mainWindow", "停止"))
        self.fallPushButton.setText(_translate("mainWindow", "下降"))
        self.modelLabel.setText(_translate("mainWindow", "TextLabel"))
        self.versionLabel.setText(_translate("mainWindow", "v18.06.20"))
        self.internetLabel.setText(_translate("mainWindow", "网络已断开"))
        self.timeLabel.setText(_translate("mainWindow", "time"))

