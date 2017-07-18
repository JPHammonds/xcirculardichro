'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import PyQt4.QtGui as qtGui
import PyQt4.QtCore as qtCore
import logging
logger = logging.getLogger(__name__)

class DataNavigatorModel(qtGui.QStandardItemModel):
    
    def __init__(self, parent=None):
        super(DataNavigatorModel, self).__init__(parent)
        self.data = []
               
