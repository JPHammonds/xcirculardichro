'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
import logging
from xcirculardichro.gui.model.datanavigatormodel import DataNavigatorModel
from xcirculardichro.gui.view.datanavigatorview import DataNavigatorView
from xcirculardichro.gui.view.specdatafileitem import SpecDataFileItem
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR
logger = logging.getLogger(__name__)


class DataNavigator(qtWidgets.QDialog):
    
    specDataSelectionChanged = qtCore.pyqtSignal(SpecDataFileItem, name="dataSelectionChanged")

    def __init__(self, parent=None):
        super(DataNavigator, self).__init__(parent)
        layout = qtWidgets.QHBoxLayout()
        self.dataNavigatorModel = DataNavigatorModel()
        self.dataNavigatorView = DataNavigatorView(dataModel=self.dataNavigatorModel)
        #self.dataNavigatorView.setModel(self.dataNavigatorModel)
        layout.addWidget(self.dataNavigatorView)
        self.setMinimumWidth(300)
        self.setLayout(layout)
        
        self.dataNavigatorView.clicked.connect(self.itemClicked)
        #self.dataNavigatorModel.dataChanged.connect(self.dataChanged)
        
    def appendDataItem(self, dataItem):
        '''
        Append a data Item to the model
        '''
        logger.debug(METHOD_ENTER_STR % dataItem)
        currentNumRows = self.dataNavigatorModel.rowCount()
        self.dataNavigatorModel.insertRows(currentNumRows, 1)
        self.dataNavigatorModel.setItem(currentNumRows, 0, dataItem)
        

#     @qtCore.pyqtSlot(qtCore.QModelIndex, qtCore.QModelIndex)
#     def dataChanged(self, topLeft, bottomRight):
#         logger.debug("Top Left position, bottom right position (%d, %d), (%d,%d)" %
#                      (topLeft.row(), topLeft.column(), 
#                       bottomRight.row(), bottomRight.column()))
        
    def itemClicked(self, index):
        logger.debug("Entering %s" % index)
        selectedItem = self.dataNavigatorModel.itemFromIndex(index)
        
        if isinstance(selectedItem, SpecDataFileItem):
            logger.debug("Filename %s" % selectedItem.getSpecDataFile().fileName)
            self.specDataSelectionChanged[SpecDataFileItem].emit(selectedItem)
    
    def model(self):
        return self.dataNavigatorModel