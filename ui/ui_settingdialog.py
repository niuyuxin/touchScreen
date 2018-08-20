# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingdialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingDialog(object):
    def setupUi(self, SettingDialog):
        SettingDialog.setObjectName("SettingDialog")
        SettingDialog.resize(621, 490)
        self.verticalLayout = QtWidgets.QVBoxLayout(SettingDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(SettingDialog)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tabWidget = QtWidgets.QTabWidget(SettingDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        self.cancelPushButton = QtWidgets.QPushButton(SettingDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelPushButton.sizePolicy().hasHeightForWidth())
        self.cancelPushButton.setSizePolicy(sizePolicy)
        self.cancelPushButton.setAutoDefault(False)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.verticalLayout.addWidget(self.cancelPushButton)

        self.retranslateUi(SettingDialog)
        self.tabWidget.setCurrentIndex(-1)
        self.cancelPushButton.clicked.connect(SettingDialog.close)
        QtCore.QMetaObject.connectSlotsByName(SettingDialog)

    def retranslateUi(self, SettingDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingDialog.setWindowTitle(_translate("SettingDialog", "Dialog"))
        self.label.setText(_translate("SettingDialog", "参数设置， 应用设置点击\"ok\"按钮， 取消点击\"Cancel\""))
        self.cancelPushButton.setText(_translate("SettingDialog", "退出"))

