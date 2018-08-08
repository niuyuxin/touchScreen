# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingpara.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingPara(object):
    def setupUi(self, SettingPara):
        SettingPara.setObjectName("SettingPara")
        SettingPara.resize(240, 179)
        self.formLayout = QtWidgets.QFormLayout(SettingPara)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(SettingPara)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(SettingPara)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(SettingPara)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(SettingPara)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(SettingPara)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.settingParaButtonBox = QtWidgets.QDialogButtonBox(SettingPara)
        self.settingParaButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.settingParaButtonBox.setObjectName("settingParaButtonBox")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.settingParaButtonBox)
        self.devNameLabel = QtWidgets.QLabel(SettingPara)
        self.devNameLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.devNameLabel.setObjectName("devNameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.devNameLabel)
        self.actualPosLabel = QtWidgets.QLabel(SettingPara)
        self.actualPosLabel.setObjectName("actualPosLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.actualPosLabel)
        self.label_6 = QtWidgets.QLabel(SettingPara)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.zeroPosLabel = QtWidgets.QLabel(SettingPara)
        self.zeroPosLabel.setObjectName("zeroPosLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.zeroPosLabel)
        self.lowerLimitPosLineEdit = QtWidgets.QLineEdit(SettingPara)
        self.lowerLimitPosLineEdit.setObjectName("lowerLimitPosLineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lowerLimitPosLineEdit)
        self.upperLimitPosLineEdit = QtWidgets.QLineEdit(SettingPara)
        self.upperLimitPosLineEdit.setObjectName("upperLimitPosLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.upperLimitPosLineEdit)
        self.targetPosLineEdit = QtWidgets.QLineEdit(SettingPara)
        self.targetPosLineEdit.setObjectName("targetPosLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.targetPosLineEdit)

        self.retranslateUi(SettingPara)
        QtCore.QMetaObject.connectSlotsByName(SettingPara)

    def retranslateUi(self, SettingPara):
        _translate = QtCore.QCoreApplication.translate
        SettingPara.setWindowTitle(_translate("SettingPara", "Form"))
        self.label.setText(_translate("SettingPara", "设备名称："))
        self.label_2.setText(_translate("SettingPara", "当前位置："))
        self.label_3.setText(_translate("SettingPara", "软上限："))
        self.label_4.setText(_translate("SettingPara", "软下限："))
        self.label_5.setText(_translate("SettingPara", "零位："))
        self.devNameLabel.setText(_translate("SettingPara", "TextLabel"))
        self.actualPosLabel.setText(_translate("SettingPara", "0"))
        self.label_6.setText(_translate("SettingPara", "设定位置："))
        self.zeroPosLabel.setText(_translate("SettingPara", "0"))

