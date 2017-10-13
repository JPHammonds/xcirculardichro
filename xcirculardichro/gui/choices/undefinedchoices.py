'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro.gui.choices.abstractchoices import AbstractChoices
import logging
logger = logging.getLogger(__name__)

DEFAULT_SELECTIONS = [["", "", ""],]
PLOT_CHOICES = ["Y1/Y2",]

class UndefinedChoices(AbstractChoices):
    COUNTER_OPTS = ["X", "Y1", "Y2"]
    
    def __init__(self, parent=None):
        super(UndefinedChoices, self).__init__(parent)
        layout = self.layout()        
        
        plotLayout = qtWidgets.QHBoxLayout()
        label = qtWidgets.QLabel("Plot Type: ")
        self.plotSelector = qtWidgets.QComboBox()
        self.plotSelector.insertItems(0, PLOT_CHOICES)
        plotLayout.addWidget(label)
        plotLayout.addWidget(self.plotSelector)
        
        layout.addLayout(plotLayout)
        self.plotSelector.currentIndexChanged[int].connect(self.plotSelectorChanged)
        self.setLayout(layout)
        self.plotSelections = DEFAULT_SELECTIONS

    def calcPlotData(self, data):
        return data
        
    def getPlotSelections(self):
        selections = self.plotSelections[0]
        logger.debug("selections %s " % selections )
        return selections
        
    @qtCore.pyqtSlot(int)
    def plotSelectorChanged(self, newType):
        self.plotTypeChanged[int].emit(newType)
        
    def setPlotSelections(self, selections):
        self.plotSelections[0] = selections
        
    def getPlotAxisLabels(self):
        labels = ["X",]
        labels.extend(str(self.plotSelector.currentText()).split('/'))
        return labels

    def getPlotAxisLabelsIndex(self):
        plotTypes = self.plotSelector.currentText().split("/")
        axisIndex = []
        axisIndex.append(0)    #x axis, kQTExifUserDataFlashEnergy
        for pType in plotTypes:
            if pType == "Y1":
                axisIndex.append(1)
            else: 
                axisIndex.append(2)
            
            
        return axisIndex

    def plotCorrectedData(self):
        return False

