#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtSql import  QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QObject

class DataBaseException(Exception):pass
class DataBase(QObject):
    dataBaseName = "TouchScreen.db"
    dataBaseVersion = "180622"
    def __init__(self, parent = None):
        super().__init__(parent)
        self.dataBase = QSqlDatabase.addDatabase("QSQLITE", DataBase.dataBaseName)
        self.dataBase.setDatabaseName(DataBase.dataBaseName)
        self.dataBase.setUserName("root")
        self.dataBase.setPassword("123456")
        if not self.dataBase.open():
            raise DataBaseException("Can not create Data {}!".format(DataBase.dataBaseName))
        sqlQuery = QSqlQuery(self.dataBase)
        update = True
        tables = self.dataBase.tables()
        print(tables)
        if "VersionInfo" in tables:
            if sqlQuery.exec_("SELECT * FROM {}".format("VersionInfo")):
                if sqlQuery.next():
                    print(sqlQuery.value(1))
        else:
            sqlQuery.exec_("""CREATE TABLE VersionInfo (
                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                        version VARCHAR(20) NOT NULL,
                        description VARCHAR(40) NOT NULL)""")
            sqlQuery.exec_("INSERT INTO VersionInfo (version, description) "
                        "VALUES ({ver}, 'Initialization version')".format(ver=DataBase.dataBaseVersion))
            ret = sqlQuery.exec_("""CREATE TABLE DeviceInfo (
                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                        name VARCHAR NOT NULL,
                        currentPos INTEGER NOT NULL,
                        upLimitedPos INTEGER NOT NULL,
                        downLimitedPos INTEGER NOT NULL,
                        zeroPos INTEGER NOT NULL)""")
    def insertRecord(self, table = "", item = dict()):
        print("insertRecord", item)
    def selectRecord(self, table = "", item = dict()):
        print("select Record", item)
