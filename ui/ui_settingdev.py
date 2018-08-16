# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingdev.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingDevDialog(object):
    def setupUi(self, SettingDevDialog):
        SettingDevDialog.setObjectName("SettingDevDialog")
        SettingDevDialog.resize(486, 496)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SettingDevDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(SettingDevDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.pushButton_3 = QtWidgets.QPushButton(SettingDevDialog)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.frame = QtWidgets.QFrame(SettingDevDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.prevPushButton = QtWidgets.QPushButton(self.frame)
        self.prevPushButton.setObjectName("prevPushButton")
        self.horizontalLayout.addWidget(self.prevPushButton)
        self.indexLabel = QtWidgets.QLabel(self.frame)
        self.indexLabel.setObjectName("indexLabel")
        self.horizontalLayout.addWidget(self.indexLabel)
        self.nextPushButton = QtWidgets.QPushButton(self.frame)
        self.nextPushButton.setObjectName("nextPushButton")
        self.horizontalLayout.addWidget(self.nextPushButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.contentFrame = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contentFrame.sizePolicy().hasHeightForWidth())
        self.contentFrame.setSizePolicy(sizePolicy)
        self.contentFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.contentFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.contentFrame.setObjectName("contentFrame")
        self.verticalLayout.addWidget(self.contentFrame)
        self.verticalLayout_2.addWidget(self.frame)
        self.confirmButtonBox = QtWidgets.QDialogButtonBox(SettingDevDialog)
        self.confirmButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.confirmButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.confirmButtonBox.setObjectName("confirmButtonBox")
        self.verticalLayout_2.addWidget(self.confirmButtonBox)

        self.retranslateUi(SettingDevDialog)
        self.confirmButtonBox.accepted.connect(SettingDevDialog.accept)
        self.confirmButtonBox.rejected.connect(SettingDevDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingDevDialog)

    def retranslateUi(self, SettingDevDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingDevDialog.setWindowTitle(_translate("SettingDevDialog", "Dialog"))
        self.label_2.setText(_translate("SettingDevDialog", "旁路设定，当前只允许选中单个设备\n"
" “ok”选择生效 “cancel”放弃选择"))
        self.pushButton_3.setText(_translate("SettingDevDialog", "旁路"))
        self.prevPushButton.setText(_translate("SettingDevDialog", "上一页"))
        self.indexLabel.setText(_translate("SettingDevDialog", "1/1"))
        self.nextPushButton.setText(_translate("SettingDevDialog", "下一页"))

