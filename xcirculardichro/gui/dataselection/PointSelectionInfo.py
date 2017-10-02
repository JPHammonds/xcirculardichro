'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR
logger = logging.getLogger(__name__)

class PointSelectionInfo(qtWidgets.QDialog):
    POINT_SELECTIONS = ["Pre-Edge", "Post-Edge"]
    selectorTypeChanged = qtCore.pyqtSignal(int)
        
    def __init__(self, parent=None):
        super(PointSelectionInfo, self).__init__(parent=parent)
        layout = qtWidgets.QVBoxLayout()
        
        self.pointSetSelector = qtWidgets.QComboBox()
        self.pointSetSelector.insertItems(0, self.POINT_SELECTIONS)
        layout.addWidget(self.pointSetSelector)
        self.pointSelections = {}
        for selection in self.POINT_SELECTIONS:
            self.pointSelections[selection] = PointSetInfo(selection)
            layout.addWidget(self.pointSelections[selection])
            
        self.setLayout(layout)
        self.pointSetSelector.currentIndexChanged[int].connect(self.handlePointSetSelectorTypeChanged)
        
    def handlePointSetSelectorTypeChanged(self, index):
        self.selectorTypeChanged[int].emit(index)
        
    def setSelectionIndices(self, selectionType, indices):
        logger.debug(METHOD_ENTER_STR % ((selectionType,indices),))
        self.pointSelections[selectionType].setIndices(indices)
        
    def setSelectionAverage(self, selectionType, average):
        logger.debug(METHOD_ENTER_STR % ((selectionType,average),))
        self.pointSelections[selectionType].setAverage(average)
        
class PointSetInfo(qtWidgets.QDialog):

    def __init__(self, pointSetLabel, parent=None):
        super(PointSetInfo, self).__init__(parent=parent)
        layout = qtWidgets.QHBoxLayout()
        label = qtWidgets.QLabel(str(pointSetLabel))
        layout.addWidget(label)
        label = qtWidgets.QLabel("Indices:")
        layout.addWidget(label)
        self.pointSetIndices = qtWidgets.QLabel("[]")
        layout.addWidget(self.pointSetIndices)
        label = qtWidgets.QLabel("Average:")
        layout.addWidget(label)
        self.pointSetAverage = qtWidgets.QLabel("None")
        layout.addWidget(self.pointSetAverage)
        
        self.setLayout(layout)

    def setIndices(self, indices):
        logger.debug(METHOD_ENTER_STR % indices)
        self.pointSetIndices.setText(str(indices))
        
    def setAverage(self, average):
        logger.debug(METHOD_ENTER_STR % average)
        self.pointSetAverage.setText(str(average))

class PointSetSelector(qtWidgets.QDialog):
    
    def __init__(self, parent=None):
        super(PointSetSelector, self).__init__(parent=parent)
        