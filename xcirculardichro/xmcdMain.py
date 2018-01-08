'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import sys
import PyQt5.QtWidgets as qtWidgets
from xcirculardichro.gui.xmcdmainwindow import XMCDMainWindow


def main():
    app = qtWidgets.QApplication(sys.argv)
    mainWindow = XMCDMainWindow()
#    mainWindow.show()
    sys.exit(app.exec_())