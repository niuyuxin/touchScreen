#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import *

class SubDevAttr(QPushButton):
    CW_Raise = (1<<15)
    CW_Stop = (1<<14)
    CW_Drop = (1<<13)
    CW_Mode0 = (1<<12)
    CW_Mode1 = (1<<11)
    CW_Selected = (1<<10)
    CW_Partial = (1<<9)
    CW_Comm = (1<<8)
    CW_WarningRst = (1<<7)
    CW_Upturning = (1<<6)
    CW_Downturning = (1<<5)
    CW_Start = (1<<4)
    CW_Stop = (1<<3)
    valueChanged = pyqtSignal()
    def __init__(self, p = 0, id = 0, key = None, parent = None):
        super(SubDevAttr, self).__init__(parent)
        self.currentPos = p
        self.devId = id
        self.devKey = key
        self.ctrlWord = 0
        self.upLimitedPos = 0
        self.downLimitedPos = 0
        self.targetPos = 0
        self.zeroPos = 0
        self.isUsed = True
        self.isUpLimited = False
        self.isDownLimited = False
        self.isPartialCircuit = False
        self.isReplaced = False
        self.setFixedSize(100, 100)
        self.setCheckable(True)
        self.setFocusPolicy(Qt.NoFocus)

    def setCtrlWord(self, value):
        self.ctrlWord |= value
        self.ctrlWord &= 0xffff

    def clearCtrlWord(self, value):
        self.ctrlWord &= (~value)
        self.ctrlWord &= 0xffff

    def getCtrlWord(self):
        return self.ctrlWord&0xffff