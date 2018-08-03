'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import logging
from xcirculardichro import METHOD_ENTER_STR, METHOD_EXIT_STR
import traceback
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
        logger.debug(METHOD_ENTER_STR % row)
        
        logger.debug("Children of %s:\n%s" % (self, self._children))
        for child in self._children:
            logger.debug("Child:%s" % (child))
        logger.debug("_children %s" % self._children)
        if row > len(self._children):
            logger.debug(traceback.extract_stack())
            raise ValueError("Tried to retrieve Row %d  when there "
                             "are only %d rows" % (row,len(self._children)))
            
        retVal = None
        if len(self._children) > 0:
            retVal = self._children[row]
        else:
            retVal = None
        logger.debug(METHOD_EXIT_STR % retVal)
        return retVal

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
    
    def removeChild(self, node):
        logging.debug(METHOD_ENTER_STR % node)
        for child in self._children:
            if child == node:
                logging.debug("len(self._children)%s" % len(self._children))
                self._children.remove(child)
                logging.debug("len(self._children)%s" % len(self._children))
                node.setParent(None)
                child = None
                            
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
        logger.debug(METHOD_ENTER_STR % checked)
        self._isChecked = checked

    def shortName(self):
        return self._name

    def __repr__(self):
        return self._name