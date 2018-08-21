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
    version = "18.07.08.6"
    monitorId = 0
    def __init__(self, fileDir):
        ConfigKeys.settingFileName = fileDir + '/' + ConfigKeys.settingFileName
        print(ConfigKeys.settingFileName)
        set = QSettings(ConfigKeys.settingFileName, QSettings.IniFormat)
        set.setIniCodec(QTextCodec.codecForName("UTF-8"))
        if Config.version != str(set.value(ConfigKeys.version)):
            set.clear()
            set.setValue("Version", Config.version)
            set.setValue(ConfigKeys.monitorId, 0)
            set.setValue("Password", "123")
            set.setValue("Rocker", 0)
            onStage = ["吊杆1", "吊杆2", "吊杆3", "吊杆4", "吊杆5", "吊杆6", "吊杆7", "吊杆8", "吊杆9", "吊杆10",
                       "单点吊杆1", "单点吊杆2", "单点吊杆3", "单点吊杆4", "单点吊杆5",
                       "灯光吊笼1", "灯光吊笼2", "灯光吊笼3", "灯光吊笼4", "灯光吊笼5", "灯光吊笼6", "灯光吊笼7", "灯光吊笼8",
                       "灯光吊杆1", "灯光吊杆2", "灯光吊杆3", "灯光吊杆4", "灯光吊杆5", "灯光吊杆6", "灯光吊杆7", "灯光吊杆8", "灯光吊杆9", "灯光吊杆10",
                       "大幕对开", "大幕升降"]
            offStage = [
                    "升降台1", "升降台2", "升降台3", "升降台4",
                    "侧车台1", "侧车台2", "侧车台3", "侧车台4", "侧车台5",
                    "转台", "后车台行走", "后车台补台", "侧补台"
            ]
            count = 0
            for item in onStage:
                set.setValue("{}/{}{}".format(ConfigKeys.onStageDev, ConfigKeys.onStageButtonName, count), "18062000{}:{}:".format(count,item))
                set.sync()
                count += 1
            for item in offStage:
                set.setValue("{}/{}{}".format(ConfigKeys.offStageDev, ConfigKeys.offStageButtonName, count), "18062000{}:{}:".format(count, item))
                set.sync()
                count += 1
            for item in range(4):
                set.setValue("UserKeys/UserKey{}".format(item), "18063000{}:自定义{}:{}:".format(item, item+1, item+100))
            set.setValue(ConfigKeys.monitorName, "TouchScreen")
            set.sync()
        Config.monitorId = int(Config.value(ConfigKeys.monitorId))
    @staticmethod
    def setValue(k, v):
        set = QSettings(ConfigKeys.settingFileName, QSettings.IniFormat)
        set.setIniCodec(QTextCodec.codecForName("UTF-8"))
        set.setValue(k, v)
        set.sync()
    @staticmethod
    def value(k):
        set  = QSettings(ConfigKeys.settingFileName, QSettings.IniFormat)
        set.setIniCodec(QTextCodec.codecForName("UTF-8"))
        return set.value(k)
    @staticmethod
    def getGroupValue(gname):
        set  = QSettings(ConfigKeys.settingFileName, QSettings.IniFormat)
        set.setIniCodec(QTextCodec.codecForName("UTF-8"))
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
