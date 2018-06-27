#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QPushButton

class PushButtonWithAttr(QPushButton):
    def __init__(self, p = 0, parent = None):
        super(PushButtonWithAttr, self).__init__(parent)
        self.__pos = p
        self.isUsed = True
        self.setFixedSize(100, 100)
        self.setCheckable(True)
    def getPos(self):
        return self.__pos
