# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'autorunningwidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_autoRunningWidget(object):
    def setupUi(self, autoRunningWidget):
        autoRunningWidget.setObjectName("autoRunningWidget")
        autoRunningWidget.resize(158, 56)
        self.verticalLayout = QtWidgets.QVBoxLayout(autoRunningWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(autoRunningWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(autoRunningWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.runningItemsWidget = QtWidgets.QWidget(autoRunningWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runningItemsWidget.sizePolicy().hasHeightForWidth())
        self.runningItemsWidget.setSizePolicy(sizePolicy)
        self.runningItemsWidget.setObjectName("runningItemsWidget")
        self.verticalLayout.addWidget(self.runningItemsWidget)

        self.retranslateUi(autoRunningWidget)
        QtCore.QMetaObject.connectSlotsByName(autoRunningWidget)

    def retranslateUi(self, autoRunningWidget):
        _translate = QtCore.QCoreApplication.translate
        autoRunningWidget.setWindowTitle(_translate("autoRunningWidget", "Form"))
        self.label.setText(_translate("autoRunningWidget", "时间"))

