'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import logging
from xcirculardichro import METHOD_ENTER_STR, METHOD_EXIT_STR

logger = logging.getLogger(__name__)

class DataNode(object):
    '''
    Class to represent a node of data.  This  will be the base class for
    a hierarchy of nodes.  Ultimately, these nodes may represent a file,
    scan in a file, header information, point in a scan, etc.
    '''
    
    def __init__(self, name, parent=None):
        self._name = name
        self._children = []
        self._parent=parent
        self._isChecked = False
        if parent is not None:
            self._parent.addChild(self)
        
    def child(self, row):
        #logger.debug(METHOD_ENTER_STR)
        #logger.debug(METHOD_EXIT_STR % self._children[row])
        return self._children[row]
    
    def childCount(self):
        #logger.debug(METHOD_ENTER_STR)
        return len(self._children)
                
    def addChild(self, child):
        #logger.debug(METHOD_ENTER_STR % child)
        self._children.append(child)
        child.setParent(self)

    def name(self):
        #logger.debug(METHOD_ENTER_STR % self._name)
        return self._name
    
    def parent(self):
        #logger.debug(METHOD_ENTER_STR % self._parent)
        return self._parent
    
    def row(self):
        #logger.debug(METHOD_ENTER_STR)
        if self._parent is not None:
            return self._parent._children.index(self)
        
    def setName(self, name):
        #logger.debug(METHOD_ENTER_STR % self.name)
        self._name = name
        
    def setParent(self, parent):
        #logger.debug(METHOD_ENTER_STR % parent)
        self._parent = parent
    
    def isChecked(self):
        #logger.debug(METHOD_ENTER_STR % self._isChecked)
        return self._isChecked
    
    def setChecked(self, checked):
        #logger.debug(METHOD_ENTER_STR % checked)
        self._isChecked = checked

    def shortName(self):
        return self._name

    def __repr__(self):
        return self._name