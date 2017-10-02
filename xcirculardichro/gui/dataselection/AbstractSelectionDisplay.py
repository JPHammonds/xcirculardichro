'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
from abc import ABC, abstractmethod, ABCMeta
from PyQt5 import QtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR,\
    METHOD_EXIT_STR
from specguiutils import XMCDException
logger = logging.getLogger(__name__)

class AbstractSelectionDisplay(QtWidgets.QDialog):

    dataSelectionsChanged = qtCore.pyqtSignal(name="dataSelectionsChanged")
    plotOptionChanged = qtCore.pyqtSignal(name="plotOptionChanged")    
    pointSelectionTypeChanged = qtCore.pyqtSignal(int, name="pointSelectionTypeChanged")
    pointSelectionAxisChanged = qtCore.pyqtSignal(int, name="pointSelectionAxisChanged")
    def __init__(self, parent=None):
        super(AbstractSelectionDisplay, self).__init__(parent=parent)
        self._selectedNodes = []
        
    @qtCore.pyqtSlot(int)
    def handleSelectorTypeChanged(self, index):
        logger.debug(METHOD_ENTER_STR % index)
        self.pointSelectionTypeChanged[int].emit(index)
        
    @qtCore.pyqtSlot(int)
    def handleSelectorAxisChanged(self, index):
        logger.debug(METHOD_ENTER_STR % index)
        self.pointSelectionAxisChanged[int].emit(index)
    
    @abstractmethod
    def isMultipleScansSelected(self):
        logger.debug(METHOD_ENTER_STR)
        raise NotImplementedError("Must subclass this and override this method")
        
    @abstractmethod
    def calcPlotData(self, data):
        raise NotImplementedError("Must subclass this and override this method")
        
    @abstractmethod
    def getPlotAxisLabels(self):
        raise NotImplementedError("Must subclass this and override this method")
        
#     @abstractmethod
#     def getDataLabels(self):
#         raise NotImplementedError("Must subclass this and override this method")

    def getNodeContainingScan(self, scan):
        nodeContainingScan = self._selectedNodes[0]
        for node in self._selectedNodes:
            for scanInNode in node.scans:
                if scanInNode == scan:
                    nodeContainingScan = node
        logging.debug(METHOD_EXIT_STR % nodeContainingScan)
        return nodeContainingScan
        
    @abstractmethod
    def getPlotAxisLabelsIndex(self):
        raise NotImplementedError("Must subclass this and override this method")

    @abstractmethod
    def getSelectedScans(self):
        raise NotImplementedError("Must subclass this and override this method")
        
    @abstractmethod
    def plotIndividualData(self):
        raise NotImplementedError("Must subclass this and override this method")
        
    @abstractmethod
    def plotAverageData(self):
        raise NotImplementedError("Must subclass this and override this method")
            
    def selectedNodes(self):
        return self._selectedNodes
    
    @abstractmethod
    def setLeftDataSelection(self, label, selection, average):
        raise NotImplementedError("Must subclass this and override this method")
    
    @abstractmethod
    def setRightDataSelection(self, label, selection, average):
        raise NotImplementedError("Must subclass this and override this method")
    
    def setSelectedNodes(self, selectedNodes):
        logger.debug(METHOD_ENTER_STR % self)
        self._selectedNodes = selectedNodes
        self.setupDisplayWithSelectedNodes()
        
    @abstractmethod
    def setupDisplayWithSelectedNodes(self):
        logger.debug(METHOD_ENTER_STR)
        raise NotImplementedError("Must subclass this and override this method")
        
class XMCDNoScanSelected(XMCDException):
    
    def __init__(self, msg):
        super(XMCDNoScanSelected, self).__init__(msg)