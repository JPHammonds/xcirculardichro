'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
from abc import ABC, abstractmethod, ABCMeta
from PyQt5 import QtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro import METHOD_ENTER_STR, METHOD_EXIT_STR
from specguiutils import XMCDException
from enum import Enum
logger = logging.getLogger(__name__)

class SelectionTypeNames(Enum):
    DUMMY_SELECTION, SPEC_SELECTION, INTERMEDIATE_SELECTION = range(3)

OVERRIDE_METHOD_STR ="Must subclass this and override this method"

class AbstractSelectionDisplay(QtWidgets.QSplitter):

    dataSelectionsChanged = qtCore.pyqtSignal(name="dataSelectionsChanged")
    plotOptionChanged = qtCore.pyqtSignal(name="plotOptionChanged")    
    pointSelectionTypeChanged = qtCore.pyqtSignal(int, name="pointSelectionTypeChanged")
    pointSelectionAxisChanged = qtCore.pyqtSignal(int, name="pointSelectionAxisChanged")
    pointSelectionReloadPicks = qtCore.pyqtSignal(list, list, name="pointSelectReloadPicks")

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
    
    def hasPointSelectionWidget(self):
        return False
    
    def hasValidPointSelectionData(self):
        return False
    
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
    def getPlotAxisLabelsIndex(self):
        raise NotImplementedError(OVERRIDE_METHOD_STR)

    @abstractmethod
    def getSelectedCounterInfo(self):
        raise NotImplementedError(OVERRIDE_METHOD_STR)

    @abstractmethod
    def getSelectedScans(self):
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
    
    @abstractmethod
    def setLeftDataSelection(self, label, selection, average):
        raise NotImplementedError(OVERRIDE_METHOD_STR)
    
    @abstractmethod
    def setRightDataSelection(self, label, selection, average):
        raise NotImplementedError(OVERRIDE_METHOD_STR)
    
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

class XMCDNoScanSelected(XMCDException):
    
    def __init__(self, msg):
        super(XMCDNoScanSelected, self).__init__(msg)