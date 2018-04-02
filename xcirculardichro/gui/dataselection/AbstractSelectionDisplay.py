'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
from abc import abstractmethod
import logging
from PyQt5 import QtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro import METHOD_ENTER_STR, METHOD_EXIT_STR
from specguiutils import XMCDException

logger = logging.getLogger(__name__)

OVERRIDE_METHOD_STR ="Must subclass this and override this method"

class AbstractSelectionDisplay(QtWidgets.QSplitter):

    dataSelectionsChanged = \
        qtCore.pyqtSignal(name="dataSelectionsChanged")
    plotOptionChanged = qtCore.pyqtSignal(name="plotOptionChanged")    
    pointSelectionTypeChanged = \
        qtCore.pyqtSignal(int, name="pointSelectionTypeChanged")
    pointSelectionAxisChanged = \
        qtCore.pyqtSignal(int, name="pointSelectionAxisChanged")
    pointSelectionReloadPicks = \
        qtCore.pyqtSignal(list, list, name="pointSelectReloadPicks")
    rangeValuesChanged = qtCore.pyqtSignal(list, list, name='rangeValuesChanged')

    def __init__(self, parent=None):
        super(AbstractSelectionDisplay, self).__init__(parent=parent)
        self.setOrientation(qtCore.Qt.Vertical)
        self._selectedNodes = []
        self.selectedScans = []
        self.selectionType = None
        
    @qtCore.pyqtSlot(int)
    def handleSelectorTypeChanged(self, index):
        logger.debug(METHOD_ENTER_STR % index)
        self.pointSelectionTypeChanged[int].emit(index)
        
    @qtCore.pyqtSlot(int)
    def handleSelectorAxisChanged(self, index):
        logger.debug(METHOD_ENTER_STR % index)
        self.pointSelectionAxisChanged[int].emit(index)
    
    def hasRangeSelectionWidget(self):
        return False
    
    def hasValidRangeSelectionData(self):
        return False
    
    def isDataIncreasingX(self, dataSet):
        logger.debug(METHOD_ENTER_STR % dataSet)
        retValue = False
        if dataSet[0] <= dataSet[-1]:
            retValue = True
        logger.debug(METHOD_EXIT_STR % retValue)
        return retValue
        
    @abstractmethod
    def isMultipleScansSelected(self):
        logger.debug(METHOD_ENTER_STR)
        raise NotImplementedError(OVERRIDE_METHOD_STR)
        
    @abstractmethod
    def calcPlotData(self, data):
        raise NotImplementedError(OVERRIDE_METHOD_STR)
        
    @abstractmethod
    def getCorrectedData(self, x, y):
        raise NotImplementedError(OVERRIDE_METHOD_STR)
        
    @abstractmethod
    def getPlotAxisLabels(self):
        raise NotImplementedError(OVERRIDE_METHOD_STR)
        
#     @abstractmethod
#     def getDataLabels(self):
#         raise NotImplementedError("Must subclass this and override this method")

    def getNodeContainingScan(self, scan):
        logging.debug(METHOD_EXIT_STR % scan)
        nodeContainingScan = self._selectedNodes[0]
        for node in self._selectedNodes:
            for scanInNode in node.scans:
                if scanInNode == scan:
                    nodeContainingScan = node
        logging.debug(METHOD_EXIT_STR % nodeContainingScan)
        return nodeContainingScan
        
    @abstractmethod
    def getPostEdgeRange(self):
        raise NotImplementedError(OVERRIDE_METHOD_STR)
    
    @abstractmethod
    def getPreEdgeRange(self):
        raise NotImplementedError(OVERRIDE_METHOD_STR)
    
    @abstractmethod
    def getPlotAxisLabelsIndex(self):
        raise NotImplementedError(OVERRIDE_METHOD_STR)

    @abstractmethod
    def getSelectedCounterInfo(self):
        raise NotImplementedError(OVERRIDE_METHOD_STR)

    @abstractmethod
    def getSelectedScans(self):
        raise NotImplementedError(OVERRIDE_METHOD_STR)
    
    @abstractmethod
    def getSelectedEdgeRangeData(self):
        raise NotImplementedError(OVERRIDE_METHOD_STR)
        
    @abstractmethod
    def getSelectedScansRange(self):
        raise NotImplementedError(OVERRIDE_METHOD_STR)
        
    def isType(self, selectionType):
        logger.debug(METHOD_ENTER_STR % ((selectionType, self.selectionType),))
        return selectionType == self.selectionType
    
    @abstractmethod
    def plotAverageData(self):
        '''
        Logical to determine if the plot of this type should be done. 
        '''
        raise NotImplementedError(OVERRIDE_METHOD_STR)
            
    @abstractmethod
    def plotCorrectedData(self):
        '''
        Logical to determine if the plot of this type should be done. 
        '''
        raise NotImplementedError(OVERRIDE_METHOD_STR)

    @abstractmethod
    def plotIndividualData(self):
        '''
        Logical to determine if the plot of this type should be done. 
        '''
        raise NotImplementedError(OVERRIDE_METHOD_STR)
        
    @abstractmethod
    def plotNormalizedData(self):
        '''
        Logical to determine if the plot of this type should be done. 
        '''
        raise NotImplementedError(OVERRIDE_METHOD_STR)
        
    def selectedNodes(self):
        return self._selectedNodes
    
    def setSelectedNodes(self, selectedNodes):
        logger.debug(METHOD_ENTER_STR % self)
        self._selectedNodes = selectedNodes
        self.setupDisplayWithSelectedNodes()
        
    @abstractmethod
    def setupDisplayWithSelectedNodes(self):
        logger.debug(METHOD_ENTER_STR)
        raise NotImplementedError(OVERRIDE_METHOD_STR)

    @abstractmethod
    def setPositionersToDisplay(self, positioners):
        logger.debug(METHOD_ENTER_STR)
        raise NotImplementedError(OVERRIDE_METHOD_STR)
        
    @abstractmethod
    def setUserParamsToDisplay(self, userParams):
        logger.debug(METHOD_ENTER_STR)
        raise NotImplementedError(OVERRIDE_METHOD_STR)
    
    def validateRangeSelection(self):
        selectedScansRange = self.getSelectedScansRange()
        preEdgeRange = self.getPreEdgeRange()
        postEdgeRange = self.getPostEdgeRange()
        if (preEdgeRange[0] >= selectedScansRange[0]) and \
            (preEdgeRange [0] <= preEdgeRange[1]) and \
            (postEdgeRange[0] > preEdgeRange[1]) and \
            (postEdgeRange[0] <= postEdgeRange[1]) and \
            (postEdgeRange[1] <= selectedScansRange[1]):
            return True
        else:
            return False
            

class XMCDNoScanSelected(XMCDException):
    
    def __init__(self, msg):
        super(XMCDNoScanSelected, self).__init__(msg)