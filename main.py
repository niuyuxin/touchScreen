#!/usr/bin/evn python
# -*- coding -*-

import sys
from PyQt5.QtWidgets import *
import mainwindow
import platform

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = mainwindow.MainWindow()
    form.show()
    app.exec_()