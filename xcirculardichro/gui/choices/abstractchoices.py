'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
import logging
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR
logger = logging.getLogger(__name__)

class AbstractChoices(qtWidgets.QDialog):
    
    subTypeChanged = qtCore.pyqtSignal(int, name='subTypeChanged')
    plotTypeChanged = qtCore.pyqtSignal(int, name='plotTypeChanged')
    plotOptionChanged = qtCore.pyqtSignal(name="plotOptionChanged")
    
    PLOT_OPTIONS = ["Individual & Average Scan Data",
                    "Individual Scan Data Only", 
                    "Average Scan Data Only"]
    
    def __init__(self, parent=None):
        super(AbstractChoices, self).__init__(parent)
        layout = qtWidgets.QVBoxLayout()        
        
        optionLayout = qtWidgets.QHBoxLayout()
        label = qtWidgets.QLabel("Plot Data")
        self.plotDataChoice = qtWidgets.QComboBox()
        self.plotDataChoice.insertItems(0,self.PLOT_OPTIONS)
        optionLayout.addWidget(label)
        optionLayout.addWidget(self.plotDataChoice)
        
        layout.addLayout(optionLayout)
        
        self.plotDataChoice.currentIndexChanged[int] \
            .connect(self.handlePlotChoiceChanged)
        self.setLayout(layout)

    def plotIndividualData(self):
        if (str(self.plotDataChoice.currentText()) == self.PLOT_OPTIONS[0]) or \
            (str(self.plotDataChoice.currentText()) == self.PLOT_OPTIONS[1]):
            return True
        else:
            return False
        
    def plotAverageData(self):
        if (str(self.plotDataChoice.currentText()) == self.PLOT_OPTIONS[0]) or \
            (str(self.plotDataChoice.currentText()) == self.PLOT_OPTIONS[2]):
            return True
        else:
            return False
        
    def plotCorrectedData(self):
        return False
        
    @qtCore.pyqtSlot(int)
    def handlePlotChoiceChanged(self, index):
        logger.debug("Enter")
        self.plotOptionChanged.emit()
        
        
    def getPlotAxisLabelsIndex(self):
        raise Exception("Abstract method called")
    
    def setDefaultSelectionsFromCounterNames(self, names):
        '''
        This method should be overridden by subclass
        '''
        logger.debug(METHOD_ENTER_STR % names)
    