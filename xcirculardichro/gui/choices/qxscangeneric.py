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

class QXScanGenericChoices(AbstractChoices):
    '''
    This class is set to handle the case where the scan type is "qxscan"
    but that the last two coloumns of scan data are NOT "Lock DC" and
    LockACfix
    '''
    COUNTER_OPTS = ["X", "Y1", "Y2"]
    
    def __init__(self, parent=None):
        super(QXScanGenericChoices, self).__init__(parent)
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
        '''
        Override the abstract default method.  Either plot y1/y2 or
        plot log(y1/y2)
        '''
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
        '''
        Override the abstract default method.  Plot selections here
        are for y1/y2 or log(y1/y2)
        '''
        selections = self.plotSelections[0]
        logger.debug("selections %s " % selections )
        return selections
        
    @qtCore.pyqtSlot(int)
    def plotSelectorChanged(self, newType):
        '''
        Emit a signal when the tbe selected plot type changes
        '''
        self.plotTypeChanged[int].emit(newType)
        
    def setPlotSelections(self, selections):
        '''
        Set the plot selections.
        '''
        self.plotSelections[0] = selections
        
    def getPlotAxisLabels(self):
        '''
        Return a list of axis labels for 
        '''
        labels = ["X",]
        labels.extend(str(self.plotSelector.currentText()).split('/'))
        logging.debug(labels)
        return labels

    def getPlotAxisLabelsIndex(self):
        '''
        Define an axis index against which to plot data
        '''
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
        '''
        Define whether an axis should plot corrected data.  For this 
        type of data, no type of corrected data has been defined.
        '''
        return False

