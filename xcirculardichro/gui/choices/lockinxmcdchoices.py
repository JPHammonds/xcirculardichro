'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import numpy as np
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro.gui.choices.abstractchoices import AbstractChoices
import logging
from xcirculardichro import METHOD_ENTER_STR
logger = logging.getLogger(__name__)

PLOT_CHOICES = ["XAS/XMCD", ]
DEFAULT_SELECTIONS = [["Energy", "Lock DC", "LockACfix"],]

class LockinXMCDChoices(AbstractChoices):
    '''
    Provide options and calculations for "Lockin" XMCD data.  This type 
    of data XAS and XMCD are collected directly.  This is for data 
    collected as is done for 4-id-d.  The data is in the last couple 
    columns of data with a scan type of qxscan and typically the last
    couple columns are "Lock DC" and "LockACFix"
    '''
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
        '''
        Not much calculation done here.  This returns 3 selected columns
        for E, XAS and XMCD
        '''
        logger.debug(METHOD_ENTER_STR % data)
        energy = np.array(data[0])
        xas = np.array(data[1])
        xmcd = np.array(data[2])
        
        retData = None
        if str(self.plotSelector.currentText()) == PLOT_CHOICES[0]:
            retData = [energy, xas, xmcd] 
        return retData

    def calcCorrectedData(self, data, preEdge=None, postEdge=None):
        '''
        Perform edge correction of the data.  For XAS subtract pre-edge
        plateau value.  After shifting XAS, divide XAS and XMCD by the 
        difference in post-edge and pre-edge plateau values.
        '''
        xas = data[0]
        xmcd = data[1]
        xasCor = (xas-preEdge)/(postEdge-preEdge)
        xmcdCor = (xmcd)/(postEdge-preEdge)
        return [xasCor, xmcdCor]

    def getPlotAxisLabels(self):
        '''
        Return plot axis labels
        '''
        labels = ["Energy",]
        labels.extend(str(self.plotSelector.currentText()).split('/'))
        return labels
    
    def getPlotSelections(self):
        '''
        Return a list of plot types
        '''
        selections = self.plotSelections[0]
        logger.debug("selections %s " % selections )
        return selections
        
    @qtCore.pyqtSlot(int)
    def plotCorrectedData(self):
        '''
        Return whether or not to plot corrected data/
        '''
        return True
    

    def setPlotSelections(self, selections):
        '''
        Set the list of plot selections
        '''
        self.plotSelections[0] = selections
        
    @qtCore.pyqtSlot(int)
    def plotSelectorChanged(self, newType):
        '''
        Emit a signal when plot type changes
        '''
        self.plotTypeChanged[int].emit(newType)
        
    def getPlotAxisLabelsIndex(self):
        '''
        Return indexes to which axis the data should be plotted.  This
        allows plotting data (XAS vs XMCD, etc) on different axis scales.
        '''
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

    def setDefaultSelectionsFromCounterNames(self, names):
        '''
        Override the default choices.  Should have been more like this in the 
        begunning so may need to look at a way to get this up front.
        For Sector 4-ID their lockin (scan type qxscan) data usually has the 
        last column begin with [Lock].  If this is the case, then the last two 
        columns are XAS and XMCD measured more directly.
        '''
        logger.debug(METHOD_ENTER_STR % names)
        if names[-1].startswith('Lock'):
            self.plotSelections=[['Energy', names[-2], names[-1]],]
            logger.debug("New plotSelections %s" % self.plotSelections )
    
