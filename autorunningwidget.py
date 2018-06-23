#!/usr/bin/env python
# -*- coding:utf8 -*-

from ui import ui_autorunningwidget
from PyQt5.QtWidgets import *

class AutoRunningWidget(QWidget, ui_autorunningwidget.Ui_autoRunningWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.runningItemsGrid = QGridLayout()
        self.runningItemsWidget.setLayout(self.runningItemsGrid)
        self.runningItemsGrid.addWidget(QPushButton("Test Button for others"))