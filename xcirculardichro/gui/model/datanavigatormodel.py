'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import PyQt5.QtGui as qtGui
import PyQt5.QtCore as qtCore
import logging
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR
from xcirculardichro.gui.view.dataitem import DataItem
print (__name__)
logger = logging.getLogger(__name__)

class DataNavigatorModel(qtGui.QStandardItemModel):
    
    def __init__(self, parent=None):
        super(DataNavigatorModel, self).__init__(parent)
        self._dataItems = []
        #logger.debug("Flags: %s" % self.flags())
#         logger.debug("RoleNames: %s" % self.roleNames())
#         
# #     def appendDataItem(self, dataItem):
# #         logger.debug(METHOD_ENTER_STR % dataItem)
# #         index = qtCore.QModelIndex()
# #         currentRowCount = self.rowCount(index)
# #         self.beginInsertRows(index, \
# #                              currentRowCount, \
# #                              currentRowCount )
# #         logger.debug("Before insertRow")
# #         self._dataItems.append(dataItem)
# #         #self.insertRow(currentRowCount, dataItem)
# #         logger.debug("After insertRow")
# #         self.endInsertRows()
# 
#     def flags(self, index):
#         return qtCore.Qt.ItemIsEnabled | \
#             qtCore.Qt.ItemIsSelectable | \
#             qtCore.Qt.ItemIsUserCheckable | \
#             qtCore.Qt.ItemIsEditable
# 
#     def setData(self, index, value, role=qtCore.Qt.EditRole):
#         logger.debug(METHOD_ENTER_STR, ((index, value, role),))
# #         dataItem = self.itemFromIndex(index)
# #         dataItem.setData(value)
#         row = index.row()
#         if role == qtCore.Qt.DisplayRole:
#             self._dataItems[row].setName(value)
#             self.dataChanged.emit(index,index)
#         elif role == qtCore.Qt.CheckStateRole:
#             self._dataItems[row].setCheckState(value)
#         elif role == qtCore.Qt.UserRole:
#             self._dataItems[row] = value
#             self.dataChanged.emit(index, index)
#         self.dataChanged.emit(index, index)
# #         
#     def rowCount(self, parent=qtCore.QModelIndex()):
#         logger.debug(METHOD_ENTER_STR % len(self._dataItems))
#         return len(self._dataItems)
# #     
#     def columnCount(self, parent=qtCore.QModelIndex()):
#          
#         if self.rowCount() > 0:
#             return 1
#         else:
#             return 0
#  
#     def data(self, index, role=qtCore.Qt.DisplayRole):
#         logger.debug(METHOD_ENTER_STR % ((index.row(), index.column()),))
#         row = index.row()
#         retVal = None
#         if role == qtCore.Qt.DisplayRole:
#             retVal = self._dataItems[row].name()
#         elif role == qtCore.Qt.CheckStateRole:
#             retVal = self._dataItems[row].checkState()
#         elif role == qtCore.Qt.UserRole:
#             retVal =  self._dataItems[row]
#         else:
#             retVal = qtCore.QVariant(self._dataItems[row].name())
#         logger.debug("role:%s roleNames: %s retVal %s, dataItems %s" % (role, 
#                                                           self.roleNames(), 
#                                                           retVal,
#                                                           self._dataItems[row]))
#         return qtCore.QVariant(retVal)
#      
#     def insertRows(self, startRow, numRows, parent=qtCore.QModelIndex()):
#         logger.debug(METHOD_ENTER_STR % ((startRow, numRows, parent),))
#         self.beginInsertRows(parent, startRow, startRow+numRows-1)
#         for i in range(numRows):
#             logger.debug("inserting @ %s" % startRow)
#             self._dataItems.insert(startRow, DataItem(str(startRow)))
#         logger.debug ("length of data items %d" % len(self._dataItems))
#         self.endInsertRows()
# #         
# #     def removeRows(self, startRow, numRows, parent=qtCore.QModelIndex()):
# #         logger.debug(METHOD_ENTER_STR % ((startRow, numRows, parent),))
# #         self.beginRemoveRows(parent, startRow, startRow+numRows-1)
# #         for i in range(numRows):
# #             value = self._dataItems[startRow]
# #             self._dataItems.remove(value)
# #         self.endRemoveRows()
# #         
#     def setItem(self, row, column, item):
#         logger.debug(METHOD_ENTER_STR % ((row, column, item),))
#     
#         self._dataItems[row] = item
#         super(DataNavigatorModel, self).setItem(row, column, item)
#         index = self.index(row,column)
#         self.dataChanged.emit(index, index, [qtCore.Qt.DisplayRole])
#         logger.debug([self._dataItems[row]  for row in range(len(self._dataItems))])
#         return True
# #         
