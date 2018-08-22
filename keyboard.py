#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class KeyBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(Qt.WindowModal)
        self.setFocusPolicy(Qt.NoFocus)
        self.setWindowTitle("Keyboard")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowSystemMenuHint| Qt.WindowDoesNotAcceptFocus|Qt.FramelessWindowHint)
        self.focusWidget = None
        self.initKeyWidget()
        self.setFixedSize(self.sizeHint())
        qApp.focusChanged.connect(self.focusChanged)

    def initKeyWidget(self):
        self.gridLayout = QGridLayout()
        keyStr = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "回车", "删除","退出"]
        row = 0
        count = 0
        for key in keyStr:
            btn = QPushButton(key)
            btn.setFocusPolicy(Qt.NoFocus)
            font = btn.font()
            font.setPointSize(15)
            font.setBold(True)
            btn.setFont(font)
            # btn.setStyleSheet("color:pink; font-weight: bold;")
            btn.setFixedSize(70, 70)
            btn.clicked.connect(self.onButtonClicked)
            if count != 0 and count%4 == 0:
                row += 1
            self.gridLayout.addWidget(btn, row, count%4)
            count += 1
        self.setLayout(self.gridLayout)

    def focusChanged(self, oldWidget, newWidget):
        try:
            if newWidget is not None and newWidget.isVisible():
                if newWidget.inherits("QLineEdit") or newWidget.inherits("QSpinBox"):
                    self.focusWidget = newWidget
                    width = qApp.desktop().screenGeometry().width()
                    height = qApp.desktop().screenGeometry().height()
                    globalPos = self.focusWidget.mapToGlobal(QPoint(0, 0))
                    moveWidth = globalPos.x() + self.focusWidget.geometry().width() # QCursor.pos().x()
                    moveHeight = globalPos.y() + self.focusWidget.geometry().height()# QCursor.pos().y()
                    if moveWidth + self.frameGeometry().width() > width:
                        moveWidth = moveWidth - self.frameGeometry().width()-self.focusWidget.geometry().width()
                    if moveHeight + self.frameGeometry().height() > height:
                        moveHeight = moveHeight - self.frameGeometry().height()-self.focusWidget.geometry().height()
                    self.move(moveWidth, moveHeight)
                    self.setVisible(True)
                    self.repaint()
                    self.raise_()
                else:
                    self.setVisible(False)
            elif self.focusWidget is not None:
                    qApp.setActiveWindow(self.focusWidget)
            else:
                self.setVisible(False)
        except Exception as e:
            print(str(e))
    def closeEvent(self, QCloseEvent):
        try:
            self.focusWidget.clearFocus()
            self.focusWidget = None
        except Exception as e:
            print(str(e))
    def onButtonClicked(self):
        try:
            btn = self.sender()
            if not isinstance(btn, QPushButton): return
            keyValue =  btn.text()
            if keyValue in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]:
                tabKey = QKeyEvent(QEvent.KeyPress, Qt.Key_2, Qt.NoModifier, keyValue)
                QApplication.sendEvent(self.focusWidget, tabKey)
            elif keyValue == "删除":
                tabKey = QKeyEvent(QEvent.KeyPress, Qt.Key_Backspace, Qt.NoModifier, "backspace")
                QCoreApplication.sendEvent(self.focusWidget, tabKey)
            elif keyValue == "回车":
                tabKey = QKeyEvent(QEvent.KeyPress, Qt.Key_Enter, Qt.NoModifier, "enter")
                QCoreApplication.sendEvent(self.focusWidget, tabKey)
            else:
                self.close()
        except Exception as e:
            print(str(e))