# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'systemmanagementwidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SystemManagementWidget(object):
    def setupUi(self, SystemManagementWidget):
        SystemManagementWidget.setObjectName("SystemManagementWidget")
        SystemManagementWidget.resize(489, 395)
        self.verticalLayout = QtWidgets.QVBoxLayout(SystemManagementWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.loginWidget = QtWidgets.QWidget(SystemManagementWidget)
        self.loginWidget.setObjectName("loginWidget")
        self.verticalLayout.addWidget(self.loginWidget)
        self.informationWidget = QtWidgets.QWidget(SystemManagementWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.informationWidget.sizePolicy().hasHeightForWidth())
        self.informationWidget.setSizePolicy(sizePolicy)
        self.informationWidget.setObjectName("informationWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.informationWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.informationWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.informationWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.informationWidget)

        self.retranslateUi(SystemManagementWidget)
        QtCore.QMetaObject.connectSlotsByName(SystemManagementWidget)

    def retranslateUi(self, SystemManagementWidget):
        _translate = QtCore.QCoreApplication.translate
        SystemManagementWidget.setWindowTitle(_translate("SystemManagementWidget", "Form"))
        self.pushButton.setText(_translate("SystemManagementWidget", "更改密码"))

