# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forbiddevdialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ForbidDevDialog(object):
    def setupUi(self, ForbidDevDialog):
        ForbidDevDialog.setObjectName("ForbidDevDialog")
        ForbidDevDialog.resize(593, 471)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ForbidDevDialog.sizePolicy().hasHeightForWidth())
        ForbidDevDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(ForbidDevDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.previousPushButton = QtWidgets.QPushButton(ForbidDevDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previousPushButton.sizePolicy().hasHeightForWidth())
        self.previousPushButton.setSizePolicy(sizePolicy)
        self.previousPushButton.setCheckable(True)
        self.previousPushButton.setObjectName("previousPushButton")
        self.horizontalLayout.addWidget(self.previousPushButton)
        self.nextPushButton = QtWidgets.QPushButton(ForbidDevDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextPushButton.sizePolicy().hasHeightForWidth())
        self.nextPushButton.setSizePolicy(sizePolicy)
        self.nextPushButton.setCheckable(True)
        self.nextPushButton.setChecked(False)
        self.nextPushButton.setObjectName("nextPushButton")
        self.horizontalLayout.addWidget(self.nextPushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(ForbidDevDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.forbidDevWidget = QtWidgets.QWidget(ForbidDevDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.forbidDevWidget.sizePolicy().hasHeightForWidth())
        self.forbidDevWidget.setSizePolicy(sizePolicy)
        self.forbidDevWidget.setObjectName("forbidDevWidget")
        self.verticalLayout.addWidget(self.forbidDevWidget)

        self.retranslateUi(ForbidDevDialog)
        QtCore.QMetaObject.connectSlotsByName(ForbidDevDialog)

    def retranslateUi(self, ForbidDevDialog):
        _translate = QtCore.QCoreApplication.translate
        ForbidDevDialog.setWindowTitle(_translate("ForbidDevDialog", "禁用设备列表"))
        self.previousPushButton.setText(_translate("ForbidDevDialog", "Previous"))
        self.nextPushButton.setText(_translate("ForbidDevDialog", "Next"))

