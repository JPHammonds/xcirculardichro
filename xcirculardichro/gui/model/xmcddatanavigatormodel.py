'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtGui as qtGui
import PyQt5.QtCore as qtCore
from xcirculardichro import METHOD_ENTER_STR, METHOD_EXIT_STR
from platform import node
from xcirculardichro.data.specscannode import SpecScanNode

logger = logging.getLogger(__name__)

class XMCDDataNavigatorModel(qtCore.QAbstractItemModel):
    '''
    data model to hold references to the scan file
    '''
    
    def __init__(self, root, parent=None):
        super(XMCDDataNavigatorModel, self).__init__(parent)
        logger.debug(METHOD_ENTER_STR)
        self._rootNode = root

    def columnCount(self, parent=qtCore.QModelIndex()):
        #logger.debug(METHOD_ENTER_STR)
        return 1
    
    def rowCount(self, parent=qtCore.QModelIndex()):
        #logger.debug(METHOD_ENTER_STR)
        if not parent.isValid():
            node = self._rootNode
        else:
            node = parent.internalPointer()
        #logger.debug(METHOD_EXIT_STR % node.childCount())
        return node.childCount()
    
    def data(self, index, role=qtCore.Qt.DisplayRole):
        #logger.debug("index %s, role %s" %(index, role))
        if role <6:
            logger.debug(METHOD_ENTER_STR % self.roleNames()[role])
        if not index.isValid():
            return qtCore.QVariant()
        
        node = index.internalPointer()
        if role == qtCore.Qt.CheckStateRole:
            if node.isChecked():
                return qtCore.Qt.Checked
            else:
                return qtCore.Qt.Unchecked
        
        if role == qtCore.Qt.DisplayRole or role == qtCore.Qt.EditRole:
            return qtCore.QVariant(node.shortName())
            
        if role == qtCore.Qt.ToolTipRole:
            return qtCore.QVariant(node.name())
            
        
        
#     def headerData(self, section, orientation, qtCore.Qt.DisplayRole):
#         logger.debug(METHOD_ENTER_STR)
        
    def index(self, row, column, parent=qtCore.QModelIndex()):
        logger.debug(METHOD_ENTER_STR)
        node = self.getNode(parent)
        childItem = node.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return qtCore.QModelIndex()
        
    def itemClicked(self, index):
        logger.debug(METHOD_ENTER_STR)
        
    def parent(self, index):
        #logger.debug(METHOD_ENTER_STR)
        node = self.getNode(index)
        #logger.debug("Getting parent for node %s" % node)
        parentNode = node.parent()
        if parentNode == self._rootNode:
            return qtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)
    
        
    def flags(self, index):
        logger.debug(METHOD_ENTER_STR)
        node = index.internalPointer()
        if not isinstance(node, SpecScanNode):
            return qtCore.Qt.ItemIsEnabled | qtCore.Qt.ItemIsSelectable | \
                qtCore.Qt.ItemIsUserCheckable | qtCore.Qt.ItemIsTristate
        else:
            return qtCore.Qt.NoItemFlags
        
    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
            
        return self._rootNode

    def getTopDataSelectedNodes(self):
        topNodes = self._rootNode._children[:]
        checkedNodes = []
        for node in topNodes:
            if node.isChecked():
                checkedNodes.append(node)
        logger.debug(METHOD_EXIT_STR % checkedNodes)
        return checkedNodes
        
        
    def getTopDataNodes(self):
        logger.debug(METHOD_ENTER_STR)
        return  self._rootNode._children[:]
        
            
    def insertRows(self, row, count, parent=qtCore.QModelIndex()):
        logger.debug(METHOD_ENTER_STR)
        node = self.getNode(parent)
        
        self.beginInsertRows(parent, row, row + count - 1)
        
#         for i in range(count):
#             childCount = node.childCount()
#             childNode = DataNode("untitled %s" + str(childCount))
#             #success = node.addChild(row, childNode)
            
        self.endInsertRows()
        firstIndex = self.index(0, 0)
        lastIndex = self.index(self.rowCount()-1, 0)
        self.dataChanged.emit(firstIndex, lastIndex)
        return True
            
    def removeRows(self, startRow, numRows, parent=qtCore.QModelIndex()):
        logger.debug(METHOD_ENTER_STR)
        
    def setData(self, index, value, role):
        success = True
        if not index.isValid():
            return False
         
        node = index.internalPointer()
        if role == qtCore.Qt.CheckStateRole:
            if value == qtCore.Qt.Checked:
                node.setChecked(True)
            else:
                node.setChecked(False)
            # since some nodes force exclusive access need to make sure all 
            # nodes are up to date
            firstIndex = self.index(0, 0)
            lastIndex = self.index(self.rowCount()-1, 0)
            self.dataChanged.emit(firstIndex, lastIndex)
            
        return success