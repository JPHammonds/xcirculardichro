'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
from abc import ABC, abstractmethod, ABCMeta
from PyQt5 import QtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR
logger = logging.getLogger(__name__)

class AbstractSelectionDisplay(QtWidgets.QDialog):

    dataSelectionsChanged = qtCore.pyqtSignal(name="dataSelectionsChanged")    
    def __init__(self, parent=None):
        super(AbstractSelectionDisplay, self).__init__(parent=parent)
        self._selectedNodes = []
        
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
        
    @abstractmethod
    def getDataLabels(self):
        raise NotImplementedError("Must subclass this and override this method")

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
    
    def setSelectedNodes(self, selectedNodes):
        logger.debug(METHOD_ENTER_STR % self)
        self._selectedNodes = selectedNodes
        self.setupDisplayWithSelectedNodes()
        
    @abstractmethod
    def setupDisplayWithSelectedNodes(self):
        logger.debug(METHOD_ENTER_STR)
        raise NotImplementedError("Must subclass this and override this method")
        
    