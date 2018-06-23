# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'independentctrlwidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_independentCtrlWidget(object):
    def setupUi(self, independentCtrlWidget):
        independentCtrlWidget.setObjectName("independentCtrlWidget")
        independentCtrlWidget.resize(196, 154)
        self.verticalLayout = QtWidgets.QVBoxLayout(independentCtrlWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.independentCtrlGroupBox = QtWidgets.QGroupBox(independentCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.independentCtrlGroupBox.sizePolicy().hasHeightForWidth())
        self.independentCtrlGroupBox.setSizePolicy(sizePolicy)
        self.independentCtrlGroupBox.setObjectName("independentCtrlGroupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.independentCtrlGroupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.subUpDevPushButton = QtWidgets.QPushButton(self.independentCtrlGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subUpDevPushButton.sizePolicy().hasHeightForWidth())
        self.subUpDevPushButton.setSizePolicy(sizePolicy)
        self.subUpDevPushButton.setCheckable(True)
        self.subUpDevPushButton.setObjectName("subUpDevPushButton")
        self.horizontalLayout_5.addWidget(self.subUpDevPushButton)
        self.subDownDevPushButton = QtWidgets.QPushButton(self.independentCtrlGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subDownDevPushButton.sizePolicy().hasHeightForWidth())
        self.subDownDevPushButton.setSizePolicy(sizePolicy)
        self.subDownDevPushButton.setCheckable(True)
        self.subDownDevPushButton.setObjectName("subDownDevPushButton")
        self.horizontalLayout_5.addWidget(self.subDownDevPushButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.subUpDevScrollArea = QtWidgets.QScrollArea(self.independentCtrlGroupBox)
        self.subUpDevScrollArea.setWidgetResizable(True)
        self.subUpDevScrollArea.setObjectName("subUpDevScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 73, 69))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.subUpDevScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_4.addWidget(self.subUpDevScrollArea)
        self.subDownDevScrollArea = QtWidgets.QScrollArea(self.independentCtrlGroupBox)
        self.subDownDevScrollArea.setWidgetResizable(True)
        self.subDownDevScrollArea.setObjectName("subDownDevScrollArea")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 73, 69))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.subDownDevScrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_4.addWidget(self.subDownDevScrollArea)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addWidget(self.independentCtrlGroupBox)

        self.retranslateUi(independentCtrlWidget)
        QtCore.QMetaObject.connectSlotsByName(independentCtrlWidget)

    def retranslateUi(self, independentCtrlWidget):
        _translate = QtCore.QCoreApplication.translate
        independentCtrlWidget.setWindowTitle(_translate("independentCtrlWidget", "Form"))
        self.independentCtrlGroupBox.setTitle(_translate("independentCtrlWidget", "设备"))
        self.subUpDevPushButton.setText(_translate("independentCtrlWidget", "台上设备"))
        self.subDownDevPushButton.setText(_translate("independentCtrlWidget", "台下设备"))

