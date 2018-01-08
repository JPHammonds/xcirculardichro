'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
from xcirculardichro.gui.dataselection.AbstractSelectionDisplay import AbstractSelectionDisplay,\
    SelectionTypeNames
import PyQt5.QtWidgets as qtWidget
from xcirculardichro import METHOD_ENTER_STR
logger = logging.getLogger(__name__)

DUMMY_STR = "No action taken here"
class DummySelectionDisplay(AbstractSelectionDisplay):
    
    def __init__(self,parent=None):
        super(DummySelectionDisplay, self).__init__(parent=parent)

        label = qtWidget.QLabel("No data is selected")
        
        self.addWidget(label)
        self.show()
        self.selectionType = SelectionTypeNames.DUMMY_SELECTION
        
    def calcPlotData(self, data):
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)

    def getCorrectedData(self, x, y):
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)
        return []
    
    def getPlotAxisLabels(self):
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)

    def getPlotAxisLabelsIndex(self):
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)

    
    def getSelectedCounterInfo(self):
        logger.debug(METHOD_ENTER_STR % self.selectedScans)
        counters = []
        counterNames = []
        return counters, counterNames

    def getSelectedScans(self):
        logger.debug(METHOD_ENTER_STR % self.selectedScans)
        return[]
        
    def isMultipleScansSelected(self):
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)

    def plotAverageData(self):
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)
        return False
    
    def plotCorrectedData(self):
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)
        return False

    def plotIndividualData(self):
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)
        return False

    def plotNormalizedData(self):
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)
        return False

    def setupDisplayWithSelectedNodes(self):
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)
        
    def setLeftDataSelection(self, label, selection, average):
        '''
        Dummy override that does nothing
        '''
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)
    
    def setPositionersToDisplay(self, positioners):
        '''
        Dummy override that does nothing
        '''
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)

    def setRightDataSelection(self, label, selection, average):
        '''
        Dummy override that does nothing
        '''
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)
    
    def setUserParamsToDisplay(self, userParams):
        '''
        Dummy override that does nothing
        '''
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)

    