'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import PyQt5.QtGui as qtGui
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
import logging
from xcirculardichro import METHOD_ENTER_STR
logger = logging.getLogger(__name__)

class DataItem(qtGui.QStandardItem):

    def __init__(self, name, parent=None):
        super(DataItem, self).__init__(name)
        logger.debug(METHOD_ENTER_STR % name)
        self._name = name
        self._children = []
        self._parent=parent
        if parent is not None:
            parent.addChild(self)

    def child(self, row):
        logger.debug(METHOD_ENTER_STR)
        return self._children[row]
    
    def childCount(self):
        logger.debug(METHOD_ENTER_STR)
        return len(self._children)
                
    def addChild(self, child):
        logger.debug(METHOD_ENTER_STR)
        self._children.append(child)

    def name(self):
        logger.debug(METHOD_ENTER_STR % self._name)
        return self._name
    
    def parent(self):
        logger.debug(METHOD_ENTER_STR)
        return self._parent
    
    def row(self):
        logger.debug(METHOD_ENTER_STR)
        if self._parent is not None:
            return self._parent._chidren.index()
        
    def setName(self, name):
        logger.debug(METHOD_ENTER_STR % self.name)
        self._name = name
        
    def text(self):
        return self._name