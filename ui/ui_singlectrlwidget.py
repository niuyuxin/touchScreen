# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'singlectrlwidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SingleCtrlWidget(object):
    def setupUi(self, SingleCtrlWidget):
        SingleCtrlWidget.setObjectName("SingleCtrlWidget")
        SingleCtrlWidget.resize(629, 493)
        self.verticalLayout = QtWidgets.QVBoxLayout(SingleCtrlWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tipsLabel = QtWidgets.QLabel(SingleCtrlWidget)
        self.tipsLabel.setObjectName("tipsLabel")
        self.verticalLayout.addWidget(self.tipsLabel)
        self.independentCtrlGroupBox = QtWidgets.QGroupBox(SingleCtrlWidget)
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 290, 342))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.subUpDevScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_4.addWidget(self.subUpDevScrollArea)
        self.subDownDevScrollArea = QtWidgets.QScrollArea(self.independentCtrlGroupBox)
        self.subDownDevScrollArea.setWidgetResizable(True)
        self.subDownDevScrollArea.setObjectName("subDownDevScrollArea")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 289, 342))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.subDownDevScrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_4.addWidget(self.subDownDevScrollArea)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addWidget(self.independentCtrlGroupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(40)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.confirmPushButton = QtWidgets.QPushButton(SingleCtrlWidget)
        self.confirmPushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.confirmPushButton.setCheckable(True)
        self.confirmPushButton.setObjectName("confirmPushButton")
        self.horizontalLayout.addWidget(self.confirmPushButton)
        self.cancelPushButton = QtWidgets.QPushButton(SingleCtrlWidget)
        self.cancelPushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.cancelPushButton.setCheckable(True)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SingleCtrlWidget)
        QtCore.QMetaObject.connectSlotsByName(SingleCtrlWidget)

    def retranslateUi(self, SingleCtrlWidget):
        _translate = QtCore.QCoreApplication.translate
        SingleCtrlWidget.setWindowTitle(_translate("SingleCtrlWidget", "Form"))
        self.tipsLabel.setText(_translate("SingleCtrlWidget", "请选择设备"))
        self.independentCtrlGroupBox.setTitle(_translate("SingleCtrlWidget", "设备"))
        self.subUpDevPushButton.setText(_translate("SingleCtrlWidget", "台上设备"))
        self.subDownDevPushButton.setText(_translate("SingleCtrlWidget", "台下设备"))
        self.confirmPushButton.setText(_translate("SingleCtrlWidget", "确认"))
        self.cancelPushButton.setText(_translate("SingleCtrlWidget", "全部取消"))
