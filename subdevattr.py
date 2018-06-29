#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QPushButton

class SubDevAttr(QPushButton):
    def __init__(self, p = 0, id = 0, parent = None):
        super(SubDevAttr, self).__init__(parent)
        self.currentPos = int(p)+19
        self.devId = id
        self.upLimitedPos = 1000
        self.downLimitedPos = 0
        self.zeroPos = 0
        self.isUsed = True
        self.isUpLimited = False
        self.isDownLimited = False
        self.isPartialCircuit = False
        self.isSelected = False
        self.setFixedSize(100, 100)
        self.setCheckable(True)
