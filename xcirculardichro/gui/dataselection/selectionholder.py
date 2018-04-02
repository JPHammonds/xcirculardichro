'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro import METHOD_ENTER_STR, METHOD_EXIT_STR
from xcirculardichro.gui.dataselection import DummySelectionDisplay
from xcirculardichro.gui.dataselection import SpecDisplay
from xcirculardichro.gui.dataselection import IntermediateDataSelection
from xcirculardichro.data import SpecFileDataNode
from xcirculardichro.data import IntermediateDataNode
logger = logging.getLogger(__name__)


class SelectionHolder(qtWidgets.QWidget):
    '''
    A place holder for holding options for selecting data to plot hand how to
    plot.  This class will pass along a list of selected data nodes to be 
    plotted and display the options based on type of nodes passed in.  Types 
    planned consist of things like SpecDataFileNodes, ScanNodes, some classes 
    for intermediate data (that may depend on the type)
    '''
    dataSelectionsChanged = qtCore.pyqtSignal(name="dataSelectionsChanged")
    plotOptionChanged = qtCore.pyqtSignal(name="plotOptionChanged")
    pointSelectionAxisChanged = qtCore.pyqtSignal(int, name="pointSelectionAxisChanged")
    pointSelectionTypeChanged = qtCore.pyqtSignal(int, name="pointSelectionTypeChanged")
    pointSelectionReloadPicks = qtCore.pyqtSignal(list, list, name="pointSelectReloadPicks")
    rangeSelectionChanged = qtCore.pyqtSignal(list, list, name="rangeSelectionChanged")
    rangeValuesChanged = qtCore.pyqtSignal(list,list, name='rangeValuesChanged')
    
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
        self._selectionWidget.plotOptionChanged.connect(self.handlePlotOptionChanged)
        self._selectionWidget.pointSelectionAxisChanged[int].connect(self.handleRangeSelectionAxisChanged)
        self._selectionWidget.pointSelectionTypeChanged[int].connect(self.handleRangeSelectionTypeChanged)
        self._selectionWidget.pointSelectionReloadPicks.connect(self.handleRangeSelectionReloadPicks)
        self._selectionWidget.rangeValuesChanged.connect(self.handleDataRangesChanged)

    def calcPlotData(self, data):
        return self._selectionWidget.calcPlotData(data)
        
    def getCorrectedData(self, x, y):
        return self._selectionWidget.getCorrectedData(x, y)
        
    def getNodeContainingScan(self, scan):
        logger.debug(METHOD_ENTER_STR % scan)
        logger.debug("SelectionWidget %s" % self._selectionWidget)
        return self._selectionWidget.getNodeContainingScan(scan)
    
    def getPlotAxisLabels(self):
        return self._selectionWidget.getPlotAxisLabels()
        
#     def getDataLabels(self):
#         return self._selectionWidget.getDataLabels()

    def getPlotAxisLabelsIndex(self):
        return self._selectionWidget.getPlotAxisLabelsIndex()

    def getSelectedEdgeRangeData(self):
        return self._selectionWidget.getSelectedEdgeRangeData()
        
    def getSelectedCounterInfo(self):
        return self._selectionWidget.getSelectedCounterInfo()
 
    def getSelectedScans(self):
        return self._selectionWidget.getSelectedScans()
    
    def getWriterForSelection(self):
        logger.debug(METHOD_ENTER_STR)
        scansForNode = {}
        selectedNodes = set()
        for scan in self.getSelectedScans():
            logger.debug("Getting Node for %s" % scan)
            nodeForScan = \
                self.getNodeContainingScan(scan)
            selectedNodes.add(nodeForScan)
            if not (nodeForScan in scansForNode.keys()):
                scansForNode[nodeForScan] = []
            scansForNode[nodeForScan].append(scan)
            print("SelectedNodes %s" % selectedNodes)
        selectedNodes = list(selectedNodes)
        
        nodeType = None
        if hasattr(selectedNodes, "__iter__"):
            for node in selectedNodes:
                if node.__class__ is None:
                    raise TypeError("Found a node with Type None. " \
                                    "Need to select a node for "
                                    "display/Writing")
                if nodeType == None:
                    # This is the first type everything else will need 
                    # to match this.
                    nodeType = node.__class__
                    nodeForReturn = node
                else:
                    # Make sure nodes are of the same class.  If not
                    # throw Exception since we cannot use a type based 
                    # writer for all nodes
                    if not isinstance(node, nodeType):
                        raise TypeError("Selected Nodes have different" \
                                        "node types.  Currently only " \
                                        "operations with the same " \
                                        "type are allowed")
        if nodeType is None:
            raise TypeError("Did not find an appropriate Writer")
        logger.debug("nodeType " + str(nodeType))
        return nodeForReturn.getWriterClass()
                        
                

    def isMultipleScansSelected(self):
        logger.debug(METHOD_ENTER_STR)
        return self._selectionWidget.isMultipleScansSelected()
           
    @qtCore.pyqtSlot()
    def handleDataSelectionsChanged(self):
        logger.debug(METHOD_ENTER_STR)
        self.dataSelectionsChanged.emit()
        
    @qtCore.pyqtSlot()
    def handlePlotOptionChanged(self):
        self.plotOptionChanged.emit()
    
    @qtCore.pyqtSlot(int)   
    def handleRangeSelectionAxisChanged(self, index):
        self.pointSelectionAxisChanged[int].emit(index)
    
    def handleRangeSelectionReloadPicks(self, leftSelection, rightSelection):
        self.pointSelectionReloadPicks.emit(leftSelection, rightSelection)
        
    @qtCore.pyqtSlot(int)   
    def handleRangeSelectionTypeChanged(self, index):
        self.pointSelectionTypeChanged[int].emit(index)
 
    def handleDataRangesChanged(self, preEdgeRange, postEdgeRange):
        logger.debug(METHOD_ENTER_STR % ((preEdgeRange, postEdgeRange),))
        self.rangeValuesChanged.emit(preEdgeRange, postEdgeRange)
        
    def hasValidRangeSelectionInfo(self):
        retValue = False
        if self._selectionWidget.hasRangeSelectionWidget() and  \
            self._selectionWidget.hasValidRangeSelectionData():
            retValue = True
        logger.debug(METHOD_EXIT_STR % retValue)
        return retValue

    def isSelectionType(self, selectionType):
        return self._selectionWidget.isType(selectionType)
                    
    def plotAverageData(self):
        '''
        Logical to determine if the plot of this type should be done.  Pass 
        along to the selection widget
        '''
        return self._selectionWidget.plotAverageData()
            
    def plotCorrectedData(self):
        '''
        Logical to determine if the plot of this type should be done.  Pass 
        along to the selection widget
        '''
        return self._selectionWidget.plotCorrectedData()
    
    def plotIndividualData(self):
        '''
        Logical to determine if the plot of this type should be done.  Pass 
        along to the selection widget
        '''
        return self._selectionWidget.plotIndividualData()
    
    def plotNormalizedData(self):
        return self._selectionWidget.plotNormalizedData()
        
    def setDisplayWidget(self, newDisplay):
        logger.debug(METHOD_ENTER_STR)
        if isinstance(newDisplay, self._selectionWidget.__class__):
            return
        else:
            self._selectionWidget.dataSelectionsChanged.disconnect(self.handleDataSelectionsChanged)
            self._selectionWidget.plotOptionChanged.disconnect(self.handlePlotOptionChanged)
            self._selectionWidget.pointSelectionAxisChanged[int].disconnect(self.handleRangeSelectionAxisChanged)
            self._selectionWidget.pointSelectionTypeChanged[int].disconnect(self.handleRangeSelectionTypeChanged)
            self._selectionWidget.pointSelectionReloadPicks.disconnect(self.handleRangeSelectionReloadPicks)
            self._selectionWidget.rangeValuesChanged.disconnect(self.handleDataRangesChanged)
            layout = self.layout()
            self._selectionWidget.hide()
            layout.removeWidget(self._selectionWidget)
            self._selectionWidget = newDisplay
            layout.addWidget(self._selectionWidget)
            self._selectionWidget.dataSelectionsChanged.connect(self.handleDataSelectionsChanged)
            self._selectionWidget.plotOptionChanged.connect(self.handlePlotOptionChanged)
            self._selectionWidget.pointSelectionAxisChanged[int].connect(self.handleRangeSelectionAxisChanged)
            self._selectionWidget.pointSelectionTypeChanged[int].connect(self.handleRangeSelectionTypeChanged)
            self._selectionWidget.pointSelectionReloadPicks.connect(self.handleRangeSelectionReloadPicks)
            self._selectionWidget.rangeValuesChanged.connect(self.handleDataRangesChanged)
            logger.debug(self._selectionWidget)
            
    def setPostionersToDisplay(self, positioners):
        self._selectionWidget.setPositionersToDisplay(positioners)
        
    def setSelectedNodes(self, selectedNodes):
        logger.debug(METHOD_ENTER_STR % selectedNodes)
        self._selectedNodes = selectedNodes
        
        if len(selectedNodes) == 0:
            self.setDisplayWidget(DummySelectionDisplay())
            return
        if isinstance(self._selectedNodes[0], SpecFileDataNode):
            self.setDisplayWidget(SpecDisplay())
            logger.debug(self._selectionWidget)
            self._selectionWidget.setSelectedNodes(self._selectedNodes)
            return
        if isinstance(self._selectedNodes[0],IntermediateDataNode):
            self.setDisplayWidget(IntermediateDataSelection())
            self._selectionWidget.setSelectedNodes(self._selectedNodes)

    def setUserParamsToDisplay(self, userParams):
        self._selectionWidget.setUserParamsToDisplay(userParams)
        
    def setTemperatureParamsToDisplay(self, temperatureParams):
        self._selectionWidget.setTemperatureParamsToDisplay(temperatureParams)
        
    def updateEdgeRanges(self):
        self._selectionWidget.updateEdgeRanges()
