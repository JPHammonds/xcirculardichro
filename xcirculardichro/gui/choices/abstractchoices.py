'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import PyQt4.QtGui as qtGui
import PyQt4.QtCore as qtCore
import logging
logger = logging.getLogger(__name__)

class AbstractChoices(qtGui.QDialog):
    
    subTypeChanged = qtCore.pyqtSignal(int, name='subTypeChanged')
    plotTypeChanged = qtCore.pyqtSignal(int, name='plotTypeChanged')
    
    
    def __init__(self, parent=None):
        super(AbstractChoices, self).__init__(parent)
    