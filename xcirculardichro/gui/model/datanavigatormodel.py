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
               
#     def addItem(self, item):
#         logger.debug("Enter")
#         self.beginInsertRows(qtCore.QModelIndex(), self.rowCount(), self.rowCount() + 1)
#         self.appendRow(item)
#         self.data.append(item)
#         logger.debug("Data %s " % self.data)
#         self.endInsertRows()
#         
#     def removeItemAt(self, index):
#         logger.debug("Enter %d " % index.row())
#         logger.debug("Data %s " % self.data)
#         self.beginRemoveRows(index, index.row(), index.row())
#         self.data.pop(index.row())
#         self.endInsertRows()