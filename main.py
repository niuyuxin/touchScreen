#!/usr/bin/evn python
# -*- coding -*-

import sys
from PyQt5.QtWidgets import *
import mainwindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = mainwindow.MainWindow()
    form.show()
    app.exec_()