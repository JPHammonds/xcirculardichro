#-*- coding: UTF-8 -*-
'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro.gui.choices.abstractchoices import AbstractChoices
import numpy as np
import logging
from xcirculardichro import METHOD_ENTER_STR
logger = logging.getLogger(__name__)

DEFAULT_SELECTIONS = [["", "", ""],]
PLOT_CHOICES = ["Y1%sY2"%chr(247),"ln(Y1%sY2)"%chr(247)]

class EScanChoices(AbstractChoices):
    COUNTER_OPTS = ["X", "Y1", "Y2"]
    
    def __init__(self, parent=None):
        super(EScanChoices, self).__init__(parent)
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
        logger.debug(METHOD_ENTER_STR % data)
        energy = np.array(data[0])
        y1 = np.array(data[1])
        y2 = np.array(data[2])
        
        logger.debug("Energy %s" % energy)
        logger.debug("y1 %s" %y1)
        logger.debug("y2 %s" % y2)
        retData = None
        if str(self.plotSelector.currentText()) == PLOT_CHOICES[0]:
            retData = [energy, y1/y2]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[1]:
            retData = [energy, np.log(y1/y2)]
        return retData
        
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
        logging.debug(labels)
        return labels

    def getPlotAxisLabelsIndex(self):
        plotTypes = self.plotSelector.currentText().split("/")
        axisIndex = []
        axisIndex.append(0)    #x axis, kQTExifUserDataFlashEnergy
        logger.debug("plotTypes %s" % plotTypes)
        for pType in plotTypes:
            if pType == PLOT_CHOICES[0]:
                axisIndex.append(1)
            elif pType == PLOT_CHOICES[1]: 
                axisIndex.append(1)
            
            
        return axisIndex

    def plotCorrectedData(self):
        return False

