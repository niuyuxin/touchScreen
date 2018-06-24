#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtWidgets import *
from  PyQt5.QtCore import pyqtSignal
from ui import ui_systemmanagementwidget
from config import *

class AccountLogin(QWidget):
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
        self.dialogButtonBox.button(QDialogButtonBox.Ok).clicked.connect(self.userEntry)
        self.dialogButtonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.userCancel)
    def userCancel(self):
        self.accountState.emit(False)
    def userEntry(self):
        password = self.accountPasswdLineEdit.text()
        if password == Config.getValue("PassWord"):
            self.accountState.emit(True)
        else:
            QMessageBox.warning(self,
                                "Warning",
                                "Password error, please try again!")

class SystemManagement(QDialog, ui_systemmanagementwidget.Ui_SystemManagementWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.loginLayout = QHBoxLayout()
        self.accountMangagement = AccountLogin()
        self.loginLayout.addWidget(self.accountMangagement)
        self.accountMangagement.accountState.connect(self.onAccountState)
        self.loginWidget.setLayout(self.loginLayout)
        self.setWindowTitle("账号管理")
        self.loginWidget.show()
        self.informationWidget.hide()
    def onAccountState(self, s):
        if s:
            self.loginWidget.hide()
            self.informationWidget.show()
        else:
            self.close()
    def showEvent(self, QShowEvent):
        self.accountMangagement.accountPasswdLineEdit.setFocus()

