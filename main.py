#!/usr/bin/evn python
# -*- coding -*-

import sys
from PyQt5.QtWidgets import *
import mainwindow
from keyboard import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("touchscreen.qss", 'r') as qssFile:
            styleSheet = qssFile.readlines()
        qApp.setStyleSheet("".join(styleSheet))
    except Exception as e:
        print(str(e))
        QMessageBox.warning(None,
                            "Warning",
                            "Maybe you lost style sheet file for this Application",
                            QMessageBox.Ok)
    keyboard = KeyBoard()
    keyboard.hide()
    form = mainwindow.MainWindow()
    form.show()
    app.exec_()