'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
import logging
from xcirculardichro.gui.view.dataitemdelegate import DataItemDelegate
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR,\
    METHOD_EXIT_STR
logger = logging.getLogger(__name__)

class DataNavigatorView(qtWidgets.QTreeView):
    
    def __init__(self, parent=None, dataModel=None):
        super(DataNavigatorView, self).__init__(parent)
        self.setModel(dataModel)
#        self.setItemDelegateForColumn(0, DataItemDelegate(parent))
#        self.setRootIsDecorated(False)        
#        self.model().rowsInserted[qtCore.QModelIndex,int,int].connect(self.dataAdded)
        #self.dataChanged.connect(self.dataChanged)
        
#     @qtCore.pyqtSlot(qtCore.QModelIndex, int, int)
#     def dataAdded(self,parent, startRow, endRow):
#         logger.debug(METHOD_ENTER_STR % ((parent, startRow, endRow),))
# #        print("parent %s, start %d, end %d" % (parent, start, end))
#         #print("index.row,col %d,%d" %(parent.row(),parent.col()))
#         delegate = DataItemDelegate(self.parent())
#         addedRows = list(range(startRow, endRow+1))
#         logger.debug ("added Rows: %s" % addedRows)
#         
#         self.setItemDelegateForColumn(0, delegate)
#         for row in addedRows:
#             logger.debug("setting persistent editor %d, %d" % (row, 0 ))
#             try:
#                 self.openPersistentEditor(self.model().index(row, 0))
#                 #delegate = self.itemDelegate(self.model().index(row, 0))
# 
#             except Exception as ex:
#                 logger.exception(ex)
#         logger.debug(METHOD_EXIT_STR % parent)

                    