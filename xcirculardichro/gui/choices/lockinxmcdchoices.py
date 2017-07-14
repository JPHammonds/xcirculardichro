'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import PyQt4.QtGui as qtGui
import PyQt4.QtCore as qtCore
from xcirculardichro.gui.choices.abstractchoices import AbstractChoices
import logging
logger = logging.getLogger(__name__)

PLOT_CHOICES = ["XAS/XMCD", ]
DEFAULT_SELECTIONS = [["Energy", "Lock DC", "LockACfix"],]

class LockinXMCDChoices(AbstractChoices):
    COUNTER_OPTS = ["Energy","XAS", "XMCD"]

    def __init__(self, parent=None):
        super(LockinXMCDChoices, self).__init__(parent)
        layout = self.layout()        

        plotLayout = qtGui.QHBoxLayout()

        label = qtGui.QLabel("Plot Type: ")
        self.plotSelector = qtGui.QComboBox()
        self.plotSelector.insertItems(0, PLOT_CHOICES)
        plotLayout.addWidget(label)
        plotLayout.addWidget(self.plotSelector)

        layout.addLayout(plotLayout)

        self.plotSelector.currentIndexChanged[int].connect(self.plotSelectorChanged)
        self.setLayout(layout)
        self.plotSelections = DEFAULT_SELECTIONS

    def calcPlotData(self, data):
        energy = data[0]
        xas = data[1]
        xmcd = data[2]
        
        retData = None
        if str(self.plotSelector.currentText()) == PLOT_CHOICES[0]:
            retData = [energy, xas, xmcd] 
        return retData
        
    def getPlotAxisLabels(self):
        labels = ["Energy",]
        labels.extend(str(self.plotSelector.currentText()).split('/'))
        return labels
    
    def getPlotSelections(self):
        selections = self.plotSelections[0]
        logger.debug("selections %s " % selections )
        return selections
        
    def setPlotSelections(self, selections):
        self.plotSelections[0] = selections
        
    @qtCore.pyqtSlot(int)
    def plotSelectorChanged(self, newType):
        self.plotTypeChanged[int].emit(newType)
        
