#!/usr/bin/evn python
# -*- coding -*-

import os
import sys
from PyQt5.QtWidgets import *
import mainwindow
from keyboard import *
from rcc import rc_touchscreenresource

if __name__ == "__main__":
    if os.geteuid():
        args = [sys.executable] + sys.argv
        os.execlp('sudo', 'sudo', *args)
    app = QApplication(sys.argv)
    try:
        qssFile = QFile(":/qss/touchscreen.qss")
        qssFile.open(QFile.ReadOnly)
        qApp.setStyleSheet(str(qssFile.readAll(), encoding='utf-8'))
    except Exception as e:
        print("Qss file error:", str(e))
        QMessageBox.warning(None,
                            "Warning",
                            "Maybe you lost style sheet file for this Application",
                            QMessageBox.Ok)
    keyboard = KeyBoard()
    keyboard.hide()

    form = mainwindow.MainWindow()
    form.show()
    app.exec_()
