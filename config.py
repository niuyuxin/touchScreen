#!/usr/bin/env python
# -*- coding:utf8 -*-

import  sys
from PyQt5.QtCore import *
import re

class Config(object):
    version = "18.06.21"
    def __init__(self):
        set = QSettings("TouchScreen.ini", QSettings.IniFormat)
        set.setIniCodec(QTextCodec.codecForName("UTF-8"));
        if Config.version != str(set.value("Version")):
            set.setValue("Version", Config.version)
            for item in range(100):
                set.setValue("SubDevUpStage/subButtonName{}".format(item), "subButtonName{}:设备{}:1000".format(item,item))
                set.setValue("SubDevDownStage/subButtonName{}".format(item), "subButtonName{}:设备{}:1000".format(item, item))
            set.sync()
    @staticmethod
    def saveConfig(k, v):
        set = QSettings("TouchScreen.ini", QSettings.IniFormat)
        set.setValue(k, v)
        set.sync()
    @staticmethod
    def getValue(k):
        set  = QSettings("TouchScreen.ini", QSettings.IniFormat)
        return set.value(k)
    @staticmethod
    def getGroupValue(gname):
        set  = QSettings("TouchScreen.ini", QSettings.IniFormat)
        set.setIniCodec(QTextCodec.codecForName("UTF-8"));
        set.beginGroup(gname)
        kvList = []
        count = 0
        sortedKeys = sorted(set.allKeys(),key = lambda k:int(re.search(r'(\d+)', k).group()))
        for key in sortedKeys:
            t = (key, set.value(key))
            kvList.append(t)
            count += 1
        set.endGroup()
        return kvList
if __name__ == "__main__":
    c = Config()
    print(Config.getGroupValue("SubDevUpStage"))
