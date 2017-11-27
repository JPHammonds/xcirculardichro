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
        
    def setLeftDataSelection(self, label, selection, average):
        '''
        Dummy override that does nothing
        '''
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)
    
    def setPositionersToDisplay(self):
        '''
        Dummy override that does nothing
        '''
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)

    def setRightDataSelection(self, label, selection, average):
        '''
        Dummy override that does nothing
        '''
        logger.debug(METHOD_ENTER_STR % DUMMY_STR)
    
    