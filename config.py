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
    version = "18.07.08.9"
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
            offStage = ["乐池升降台", "前辅助升降台", "主升降台1", "主升降台2", "主升降台3", "演员活门1", "演员活门2", "演员活门3",
                       "演员升降小车1", "演员升降小车2",
                       "侧辅助升降台1", "侧辅助升降台2", "侧辅助升降台3", "侧辅助升降台4", "侧辅助升降台5", "侧辅助升降台6",
                       "侧台车台1", "侧台车台2", "侧台车台3", "侧台车台4", "侧台车台5", "侧台车台6",
                       "侧补偿台1", "侧补偿台2", "侧补偿台3", "侧补偿台4", "侧补偿台5", "侧补偿台6",
                       "后辅助升降台", "车载转台行走", "车载转台旋转", "后补偿台", "芭蕾舞台"
                       ]
            onStage = [
                        "台口外单点吊机1", "台口外单点吊机2", "台口外单点吊机3", "台口外单点吊机4", "台口外单点吊机5", "台口外单点吊机6",
                        "字幕机吊杆",
                        "大幕机", "假台口上片", "假台口侧片1", "假台口侧片2",
                        "电动吊杆1", "电动吊杆2", "电动吊杆3", "电动吊杆4", "电动吊杆5", "电动吊杆6", "电动吊杆7", "电动吊杆8", "电动吊杆9", "电动吊杆10",
                        "电动吊杆11", "电动吊杆12", "电动吊杆13", "电动吊杆14", "电动吊杆15", "电动吊杆16", "电动吊杆17", "电动吊杆18", "电动吊杆19", "电动吊杆20",
                        "灯光吊杆1", "灯光吊杆2", "灯光吊杆3", "灯光吊杆4", "灯光吊杆5",
                        "侧灯光吊架1", "侧灯光吊架2",
                        "侧电动吊杆1", "侧电动吊杆2",
                        "侧台装景吊机",
                        "主舞台单点吊机1", "主舞台单点吊机2", "主舞台单点吊机3", "主舞台单点吊机4", "主舞台单点吊机5", "主舞台单点吊机6",
                        "后台景灯吊杆"
                        ]
            """
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
            """
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
                set.setValue("UserKeys/UserKey{}".format(item), "18063000{}:自定义{}:{}:".format(item, item+1, 0))
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
