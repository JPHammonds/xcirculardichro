'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import numpy as np
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
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
        energy = np.array(data[0])
        xas = np.array(data[1])
        xmcd = np.array(data[2])
        
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
        
    def getPlotAxisLabelsIndex(self):
        plotTypes = self.plotSelector.currentText().split("/")
        axisIndex = []
        axisIndex.append(0)    #x axis, kQTExifUserDataFlashEnergy
        for pType in plotTypes:
            if pType.startswith("XAS"):
                axisIndex.append(1)
            elif pType.startswith("XMCD"):
                axisIndex.append(2)
            else:
                axisIndex.append(1)
        return axisIndex

    def getDataLabels(self):
        plotTypes = self.plotSelector.currentText().split("/")
        labels = ['E', ]
        labels.extend(plotTypes)
        logger.debug("labels %s" % labels)
        return labels        