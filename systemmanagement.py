#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtWidgets import *
from  PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QRegExpValidator
from ui import ui_systemmanagementwidget
from config import *

class AccountLogin(QDialog):
    accountState = pyqtSignal(bool)
    def __init__(self, parent = None):
        super().__init__(parent)
        self.accountNameLabel = QLabel("用户名：")
        self.accountNameLineEdit = QLineEdit("Administrator")
        self.accountNameLabel.setBuddy(self.accountNameLineEdit)
        self.nameHLayout = QHBoxLayout()
        self.nameHLayout.addWidget(self.accountNameLabel)
        self.nameHLayout.addWidget(self.accountNameLineEdit)

        self.accountPasswdLabel = QLabel("密码:")
        self.accountPasswdLineEdit = QLineEdit()
        self.accountPasswdLineEdit.setEchoMode(QLineEdit.Password)
        self.accountPasswdLabel.setBuddy(self.accountNameLineEdit)
        self.accountHLayout = QHBoxLayout()
        self.accountHLayout.addWidget(self.accountPasswdLabel)
        self.accountHLayout.addWidget(self.accountPasswdLineEdit)

        self.dialogButtonBox  = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.nameHLayout)
        self.mainLayout.addLayout(self.accountHLayout)
        self.mainLayout.addWidget(self.dialogButtonBox)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("请输入用户名和密码")
        self.dialogButtonBox.button(QDialogButtonBox.Ok).clicked.connect(self.userEntry)
        self.dialogButtonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self.accountPasswdLineEdit.setFocus()
        # Fixme for test code
        self.accountPasswdLineEdit.setText("123")
        self.dialogButtonBox.button(QDialogButtonBox.Ok).animateClick()
    def userEntry(self):
        password = self.accountPasswdLineEdit.text()
        if password == Config.value("Password"):
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Password error, please try again!")
class SystemManagement(QDialog, ui_systemmanagementwidget.Ui_SystemManagementWidget):
    somthingChanged = pyqtSignal(str, str)
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.WheelFocus)
        self.setWindowTitle("账号管理")
        regExp = QRegExp(r"((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)")
        self.serverIpLineEdit.setValidator(QRegExpValidator(regExp))
        self.serverIpLineEdit.setText(Config.value(ConfigKeys.serverIp))
        self.serverIpLineEdit.returnPressed.connect(self.onServerIpLineEditingReturnPressed)
        self.repaint()

    def onServerIpLineEditingReturnPressed(self):
        serverIpText = self.sender().text()
        Config.setValue(ConfigKeys.serverIp, serverIpText)
        self.somthingChanged.emit(ConfigKeys.serverIp, serverIpText)
