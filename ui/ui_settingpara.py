# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\PythonCode\PyQtCode\touchScreen\ui\settingpara.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingPara(object):
    def setupUi(self, SettingPara):
        SettingPara.setObjectName("SettingPara")
        SettingPara.resize(240, 177)
        self.formLayout = QtWidgets.QFormLayout(SettingPara)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(SettingPara)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(SettingPara)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.currentPosSpinBox = QtWidgets.QSpinBox(SettingPara)
        self.currentPosSpinBox.setObjectName("currentPosSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.currentPosSpinBox)
        self.label_3 = QtWidgets.QLabel(SettingPara)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.upLimittedPosSpinBox = QtWidgets.QSpinBox(SettingPara)
        self.upLimittedPosSpinBox.setObjectName("upLimittedPosSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.upLimittedPosSpinBox)
        self.label_4 = QtWidgets.QLabel(SettingPara)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.downLimittedPosSpinBox = QtWidgets.QSpinBox(SettingPara)
        self.downLimittedPosSpinBox.setObjectName("downLimittedPosSpinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.downLimittedPosSpinBox)
        self.label_5 = QtWidgets.QLabel(SettingPara)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.zeroPosSpinBox = QtWidgets.QSpinBox(SettingPara)
        self.zeroPosSpinBox.setObjectName("zeroPosSpinBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.zeroPosSpinBox)
        self.settingParaButtonBox = QtWidgets.QDialogButtonBox(SettingPara)
        self.settingParaButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.settingParaButtonBox.setObjectName("settingParaButtonBox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.settingParaButtonBox)
        self.devNameLabel = QtWidgets.QLabel(SettingPara)
        self.devNameLabel.setFrameShape(QtWidgets.QFrame.Panel)
        self.devNameLabel.setObjectName("devNameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.devNameLabel)

        self.retranslateUi(SettingPara)
        QtCore.QMetaObject.connectSlotsByName(SettingPara)

    def retranslateUi(self, SettingPara):
        _translate = QtCore.QCoreApplication.translate
        SettingPara.setWindowTitle(_translate("SettingPara", "Form"))
        self.label.setText(_translate("SettingPara", "设备："))
        self.label_2.setText(_translate("SettingPara", "当前位置："))
        self.label_3.setText(_translate("SettingPara", "软上限："))
        self.label_4.setText(_translate("SettingPara", "软下限："))
        self.label_5.setText(_translate("SettingPara", "零位："))
        self.devNameLabel.setText(_translate("SettingPara", "TextLabel"))

