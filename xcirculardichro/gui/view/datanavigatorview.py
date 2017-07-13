'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import PyQt4.QtGui as qtGui
import PyQt4.QtCore as qtCore
import logging
logger = logging.getLogger(__name__)

class DataNavigatorView(qtGui.QTreeView):
    
    def __init__(self, parent=None, dataModel=None):
        super(DataNavigatorView, self).__init__(parent)
        self.setModel(dataModel)
        
    