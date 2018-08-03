#!/usr/bin/env python
# -*- coding:utf8 -*-

import  sys
from PyQt5.QtCore import *
import re
class ConfigKeys():
    version = "Version"
    monitorId = "MonitorId"
    settingFileName = "TouchScreen.ini"
    serverIp = "ServerIp"
    userKeys = "UserKeys"
    onStageDev = "OnStageDev"
    offStageDev = "OffStageDev"
    onStageButtonName = "OnStageButtonName"
    offStageButtonName = "OffStageButtonName"
    monitorName = "MonitorName"
class Config(object):
    version = "18.07.08.1"
    monitorId = 0
    def __init__(self):
        set = QSettings(ConfigKeys.settingFileName, QSettings.IniFormat)
        set.setIniCodec(QTextCodec.codecForName("UTF-8"));
        if Config.version != str(set.value(ConfigKeys.version)):
            set.clear()
            set.setValue("Version", Config.version)
            set.setValue(ConfigKeys.monitorId, 0)
            set.setValue("Password", "123")
            for item in range(100):
                set.setValue("{}/{}{}".format(ConfigKeys.onStageDev, ConfigKeys.onStageButtonName, item), "18062000{}:设备{}:".format(item,item))
            for item in range(99):
                set.setValue("{}/{}{}".format(ConfigKeys.offStageDev, ConfigKeys.offStageButtonName, item), "18062000{}:设备{}:".format(item+100, item+100))
            for item in range(4):
                set.setValue("UserKeys/UserKey{}".format(item), "18063000{}:自定义{}:{}:".format(item, item, item+100))
            set.setValue(ConfigKeys.monitorName, "TouchScreen")
            set.sync()
        Config.monitorId = int(Config.value(ConfigKeys.monitorId))
    @staticmethod
    def setValue(k, v):
        set = QSettings(ConfigKeys.settingFileName, QSettings.IniFormat)
        set.setIniCodec(QTextCodec.codecForName("UTF-8"));
        set.setValue(k, v)
        set.sync()
    @staticmethod
    def value(k):
        set  = QSettings(ConfigKeys.settingFileName, QSettings.IniFormat)
        set.setIniCodec(QTextCodec.codecForName("UTF-8"));
        return set.value(k)
    @staticmethod
    def getGroupValue(gname):
        set  = QSettings(ConfigKeys.settingFileName, QSettings.IniFormat)
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
