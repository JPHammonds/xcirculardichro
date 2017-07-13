'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import PyQt4.QtGui as qtGui
import PyQt4.QtCore as qtCore
import logging
from xcirculardichro.gui.model.datanavigatormodel import DataNavigatorModel
from xcirculardichro.gui.view.datanavigatorview import DataNavigatorView
from specguiutils.view.specdatafileitem import SpecDataFileItem
logger = logging.getLogger(__name__)


class DataNavigator(qtGui.QDialog):
    
    specDataSelectionChanged = qtCore.pyqtSignal(SpecDataFileItem, name="dataSelectionChanged")

    def __init__(self, parent=None):
        super(DataNavigator, self).__init__(parent)
        layout = qtGui.QHBoxLayout()
        self.dataNavigatorModel = DataNavigatorModel()
        self.dataNavigatorView = DataNavigatorView()
        self.dataNavigatorView.setModel(self.dataNavigatorModel)
        layout.addWidget(self.dataNavigatorView)
        self.setMinimumWidth(300)
        self.setLayout(layout)
        
        self.dataNavigatorView.clicked.connect(self.itemClicked)
        
    def itemClicked(self, index):
        logger.debug("Entering %s" % index)
        selectedItem = self.dataNavigatorModel.itemFromIndex(index)
        
        if isinstance(selectedItem, SpecDataFileItem):
            logger.debug("Filename %s" % selectedItem.getSpecDataFile().fileName)
            self.specDataSelectionChanged[SpecDataFileItem].emit(selectedItem)