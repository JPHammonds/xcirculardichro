'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro.gui.dataselection.dummyselectiondisplay import DummySelectionDisplay
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR
from xcirculardichro.data.specdatafilenode import SpecFileDataNode
from xcirculardichro.gui.dataselection.specdisplay import SpecDisplay
logger = logging.getLogger(__name__)

class SelectionHolder(qtWidgets.QDialog):
    '''
    A place holder for holding options for selecting data to plot hand how to
    plot.  This class will pass along a list of selected data nodes to be 
    plotted and display the options based on type of nodes passed in.  Types 
    planned consist of things like SpecDataFileNodes, ScanNodes, some classes 
    for intermediate data (that may depend on the type)
    '''
    dataSelectionsChanged = qtCore.pyqtSignal(name="dataSelectionsChanged")
    
    def __init__(self, parent=None):
        super(SelectionHolder, self).__init__(parent=parent)
        logger.debug(METHOD_ENTER_STR)
        layout = qtWidgets.QHBoxLayout()
        self._selectionWidget = DummySelectionDisplay()
        self._selectedNodes = []
        
        layout.addWidget(self._selectionWidget)
        self.setLayout(layout)
        self.show()
        self._selectionWidget.dataSelectionsChanged.connect(self.handleDataSelectionsChanged)

    def calcPlotData(self, data):
        return self._selectionWidget.calcPlotData(data)
        
    def getPlotAxisLabels(self):
        return self._selectionWidget.getPlotAxisLabels()
        
    def getDataLabels(self):
        return self._selectionWidget.getDataLabels()

    def getPlotAxisLabelsIndex(self):
        return self._selectionWidget.getPlotAxisLabelsIndex()

    def getSelectedCounterInfo(self):
        counters = self._selectionWidget.counterSelector.getSelectedCounters()
        counterNames = self._selectionWidget.counterSelector.getSelectedCounterNames(counters)
        return counters, counterNames
 
    def getSelectedScans(self):
        return self._selectionWidget.getSelectedScans()
    
    def isMultipleScansSelected(self):
        logger.debug(METHOD_ENTER_STR)
        return self._selectionWidget.isMultipleScansSelected()
           
    @qtCore.pyqtSlot()
    def handleDataSelectionsChanged(self):
        logger.debug(METHOD_ENTER_STR)
        self.dataSelectionsChanged.emit()
           
    def plotIndividualData(self):
        return self._selectionWidget.plotIndividualData()
    
        
    def plotAverageData(self):
        return self._selectionWidget.plotAverageData()
            
    def setDisplayWidget(self, newDisplay):
        logger.debug(METHOD_ENTER_STR)
        if isinstance(newDisplay, self._selectionWidget.__class__):
            return
        else:
            self._selectionWidget.dataSelectionsChanged.disconnect(self.handleDataSelectionsChanged)
            layout = self.layout()
            self._selectionWidget.hide()
            layout.removeWidget(self._selectionWidget)
            self._selectionWidget = newDisplay
            layout.addWidget(self._selectionWidget)
            self._selectionWidget.dataSelectionsChanged.connect(self.handleDataSelectionsChanged)
            logger.debug(self._selectionWidget)
            
    def setSelectedNodes(self, selectedNodes):
        logger.debug(METHOD_ENTER_STR)
        self._selectedNodes = selectedNodes
        
        if len(selectedNodes) == 0:
            self.setDisplayWidget(DummySelectionDisplay())
            return
        if isinstance(self._selectedNodes[0], SpecFileDataNode):
            self.setDisplayWidget(SpecDisplay())
            logger.debug(self._selectionWidget)
            self._selectionWidget.setSelectedNodes(self._selectedNodes)
            return
        
         