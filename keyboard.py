#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class KeyBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)
        self.setWindowTitle("Keyboard")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus)
        self.focusWidget = None
        self.initKeyWidget()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        qApp.focusChanged.connect(self.focusChanged)

    def initKeyWidget(self):
        self.gridLayout = QGridLayout()
        keyStr = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "删除","退出"]
        row = 0
        count = 0
        for key in keyStr:
            btn = QPushButton(key)
            btn.setFocusPolicy(Qt.NoFocus)
            btn.clicked.connect(self.onButtonClicked)
            btn.setFixedSize(70, 70)
            if count != 0 and count%3 == 0:
                row += 1
            self.gridLayout.addWidget(btn, row, count%3)
            count += 1
        self.setLayout(self.gridLayout)

    def focusChanged(self, old, new):
        try:
            if new is not None and not self.isAncestorOf(new):
                if new.inherits("QSpinBox"):
                    self.focusWidget = new
                    width = qApp.desktop().screenGeometry().width()
                    height = qApp.desktop().screenGeometry().height()
                    moveWidth = QCursor.pos().x()
                    moveHeight = QCursor.pos().y()
                    if moveWidth + self.frameGeometry().width() > width:
                        moveWidth = moveWidth - self.frameGeometry().width()
                    if moveHeight + self.frameGeometry().height() > height:
                        moveHeight = moveHeight - self.frameGeometry().height()
                    self.move(moveWidth, moveHeight)
                    self.setVisible(True)
                else:
                    self.setVisible(False)
        except Exception as e:
            print(str(e))
    def closeEvent(self, QCloseEvent):
        try:
            self.focusWidget.clearFocus()
        except Exception as e:
            print(str(e))

    def onButtonClicked(self):
        try:
            keyValue =  self.sender().text()
            if keyValue in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                value = self.focusWidget.value()
                self.focusWidget.setValue(value*10 + int(keyValue))
                # tabKey = QKeyEvent(QEvent.KeyPress, Qt.Key_2, Qt.NoModifier)
                # QCoreApplication.sendEvent(self, tabKey)
            elif keyValue == "删除":
                value = self.focusWidget.value()
                self.focusWidget.setValue(value // 10)
                # tabKey = QKeyEvent(QEvent.KeyPress, Qt.Key_Backspace, Qt.NoModifier)
                # QCoreApplication.sendEvent(self, tabKey)
            else:
                self.close()
        except Exception as e:
            print(str(e))