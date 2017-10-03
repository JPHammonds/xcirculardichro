'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
from xcirculardichro.gui.dataselection.AbstractSelectionDisplay import AbstractSelectionDisplay
import PyQt5.QtWidgets as qtWidget
logger = logging.getLogger(__name__)

class DummySelectionDisplay(AbstractSelectionDisplay):
    
    def __init__(self,parent=None):
        super(DummySelectionDisplay, self).__init__(parent=parent)

        label = qtWidget.QLabel("No data is selected")
        
        self.addWidget(label)
        self.show()
        
    def setLeftDataSelection(self, label, selection, average):
        pass
    
    def setRightDataSelection(self, label, selection, average):
        pass
    