#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QPushButton

class SubDevAttr(QPushButton):
    def __init__(self, p = 0, id = 0, parent = None):
        super(SubDevAttr, self).__init__(parent)
        self.__pos = p
        self.devId = id
        self.isUsed = True
        self.isUpLimited = False
        self.isDownLimited = False
        self.isPartialCircuit = False
        self.isSelected = False
        self.setFixedSize(100, 100)
        self.setCheckable(True)
