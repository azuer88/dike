#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Main Window')
        self.setWindowIcon(QtGui.QIcon('web.png'))
        self.show()
