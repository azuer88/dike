#!/usr/bin/env python

import sys

#from pyside.QtCore import
from PySide.QtGui import QApplication

from gui.main import MainWindow

def main():
    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()
    window.raise_()

    return app.exec_()


if __name__ == '__main__':
    main()
