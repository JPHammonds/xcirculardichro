'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
import numpy as np
from enum import Enum
from xcirculardichro.gui.choices.abstractchoices import AbstractChoices
from xcirculardichro import METHOD_ENTER_STR
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
from PyQt5.Qt import QHBoxLayout

logger = logging.getLogger(__name__)

TEY_STR = "TEY"
TFY_STR = "TFY"
REF_STR = "REF"
I0_STR = 'i0'
APPEND_A = "_A"
APPEND_B = "_B"
RCP_STR = "RCP"
LCP_STR = "LCP"
SPACE_STR = " "
UNDERSCORE_STR ="_"
XAS_STR = "XAS"
XMCD_STR = "XMCD"

DEFAULT_SELECTIONS = [["SGM1:ENERGY", \
                       TEY_STR + APPEND_A, \
                       TEY_STR + APPEND_B, \
                       TFY_STR + APPEND_A, \
                       TFY_STR + APPEND_B, \
                       REF_STR + APPEND_A, \
                       REF_STR + APPEND_B, \
                       I0_STR + APPEND_A, \
                       I0_STR + APPEND_B, ],]
class PlotChoiceId(Enum):
    xasXmcd = 0
    xasRcpLcpXasXmcd = 1
    xasRcpLcp = 2
    teyRcpLcp = 3
    tfyRcpLcp = 4
    refRcpLcp = 5
    i0RcpLcp = 6
    
PLOT_CHOICES = ["XAS/XMCD", "XAS_RCP/XAS_LCP/XAS/XMCD", "XAS_RCP/XAS_LCP", 
                "TEY_RCP/TEY_LCP", "TFY_RCP/TFY_LCP", "REF_RCP/REF_LCP", 
                "i0_RCP/i0_LCP"]


class MultiNonLockinXMCDChoices(AbstractChoices):
    '''
    Setup display options for NonLockin type data with multiple detectors 
    which feed out XAS data for different forms
    '''
    COUNTER_OPTS = ["Energy", \
                    TEY_STR + UNDERSCORE_STR + RCP_STR, \
                    TEY_STR + UNDERSCORE_STR + LCP_STR, 
                    TFY_STR + UNDERSCORE_STR + RCP_STR, \
                    TFY_STR + UNDERSCORE_STR + LCP_STR, 
                    REF_STR + UNDERSCORE_STR + RCP_STR, \
                    REF_STR + UNDERSCORE_STR + LCP_STR, 
                    I0_STR + UNDERSCORE_STR + RCP_STR, \
                    I0_STR + UNDERSCORE_STR + LCP_STR]
        
    def __init__(self, parent=None):
        super(MultiNonLockinXMCDChoices, self).__init__(parent)
        logger.debug(METHOD_ENTER_STR)
        layout = self.layout()
        
#         choiceLayout = qtWidgets.QHBoxLayout()
#         label = qtWidgets.QLabel("DataType: ")
#         self.choiceSelector = qtWidgets.QComboBox()
#         self.choiceSelector.insertItems(0, CHOICES)

        plotLayout = QHBoxLayout()
        label = qtWidgets.QLabel("Plot Type: ")
        self.plotSelector = qtWidgets.QComboBox()
        self.plotSelector.insertItems(0, PLOT_CHOICES)
        self.plotSelector.setCurrentIndex(0)
        plotLayout.addWidget(label)
        plotLayout.addWidget(self.plotSelector)
        layout.addLayout(plotLayout)
        
        self.plotSelector.currentIndexChanged[int]. \
            connect(self.plotSelectorChanged)

        self.setLayout(layout)
        self.plotSelections = DEFAULT_SELECTIONS
                
    def calcPlotData(self, data):
        '''
        From the raw data for the selected detectors calculate the 
        output values for XAS and XMCD 
        '''
        logger.debug(METHOD_ENTER_STR % data)
        #Grab stuff from the incoming array
        energy = np.array(data[0])
        teyRCP = np.array(data[1])
        teyLCP = np.array(data[2])
        tfyRCP = np.array(data[3])
        tfyLCP = np.array(data[4])
        refRCP = np.array(data[5])
        refLCP = np.array(data[6])
        i0RCP = np.array(data[7])
        i0LCP = np.array(data[8])
        
        xasTeyRCP = teyRCP/i0RCP
        xasTeyLCP = teyLCP/i0LCP
        xasTfyRCP = tfyRCP/i0RCP
        xasTfyLCP = tfyLCP/i0LCP
        xasRefRCP = refRCP/i0RCP
        xasRefLCP = refLCP/i0LCP

        xasTey = (xasTeyRCP + xasTeyLCP)/2.0
        xmcdTey = xasTeyRCP - xasTeyLCP
        xasTfy = (xasTfyRCP + xasTfyLCP)/2.0
        xmcdTfy = xasTfyRCP - xasTfyLCP
        xasRef = (xasRefRCP + xasRefLCP)/2.0
        xmcdRef = xasRefRCP - xasRefLCP
        
        retData = None
        logger.debug("PlotSelector " + self.plotSelector.currentText())
        logger.debug(PLOT_CHOICES[PlotChoiceId.xasXmcd.value])
        
        if str(self.plotSelector.currentText()) == str(PLOT_CHOICES[PlotChoiceId.xasXmcd.value]) :
            retData = [energy, xasTey, xasTfy, xasRef,
                       xmcdTey, xmcdTfy, xmcdRef]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.xasRcpLcpXasXmcd.value]:
            retData = [energy, xasTeyRCP,xasTeyLCP, xasTfyRCP,xasTfyLCP, \
                    xasRefRCP,xasRefLCP, xasTey, xasTfy, xasRef, \
                    xmcdTey, xmcdTfy, xmcdRef]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.xasRcpLcp.value ]:
            retData = [energy, xasTeyRCP,xasTeyLCP, xasTfyRCP,xasTfyLCP, \
                    xasRefRCP,xasRefLCP]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.teyRcpLcp.value] :
            retData = [energy, teyRCP, teyLCP]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.tfyRcpLcp.value] :
            retData = [energy, tfyRCP, tfyLCP]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.refRcpLcp.value] :
            retData = [energy, refRCP, refLCP]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.i0RcpLcp.value]:
            retData = [energy, i0RCP, i0LCP]
        else:
            raise LookupError(" No data selection for " + \
                              str(self.plotSelector.currentText()))
        return retData
        
    def calcCorrectedData(self, data, preEdge=None, postEdge=None):
        '''
        calculate corrected data that is scaled by step normalization
        '''
        logger.debug(METHOD_ENTER_STR, ((data, preEdge, postEdge),))
        
    def getPlotAxisLabels(self):
        labels = ["Energy",]
#        labels.extend(str(self.plotSelector.currentText()).split('/'))

        if str(self.plotSelector.currentText()) == str(PLOT_CHOICES[PlotChoiceId.xasXmcd.value]) :
            yLabels = ["".join([XAS_STR, UNDERSCORE_STR, TEY_STR]), 
                       "".join([XAS_STR, UNDERSCORE_STR, TFY_STR]),
                       "".join([XAS_STR, UNDERSCORE_STR, REF_STR]),
                       "".join([XMCD_STR, UNDERSCORE_STR, TEY_STR]),
                       "".join([XMCD_STR, UNDERSCORE_STR, TFY_STR]),
                       "".join([XMCD_STR, UNDERSCORE_STR, REF_STR])]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.xasRcpLcpXasXmcd.value]:
            yLabels = ["".join([XAS_STR, UNDERSCORE_STR, TEY_STR, \
                                UNDERSCORE_STR, RCP_STR]), \
                       "".join([XAS_STR, UNDERSCORE_STR, TEY_STR, \
                                UNDERSCORE_STR, LCP_STR]), \
                       "".join([XAS_STR, UNDERSCORE_STR, TFY_STR, \
                                UNDERSCORE_STR, RCP_STR]), \
                       "".join([XAS_STR, UNDERSCORE_STR, TFY_STR, \
                                UNDERSCORE_STR, LCP_STR]), \
                       "".join([XAS_STR, UNDERSCORE_STR, REF_STR, \
                                UNDERSCORE_STR, RCP_STR]), \
                       "".join([XAS_STR, UNDERSCORE_STR, REF_STR, \
                                UNDERSCORE_STR, LCP_STR]), \
                       "".join([XAS_STR, UNDERSCORE_STR, TEY_STR]), 
                       "".join([XAS_STR, UNDERSCORE_STR, TFY_STR]),
                       "".join([XAS_STR, UNDERSCORE_STR, REF_STR]),
                       "".join([XMCD_STR, UNDERSCORE_STR, TEY_STR]),
                       "".join([XMCD_STR, UNDERSCORE_STR, TFY_STR]),
                       "".join([XMCD_STR, UNDERSCORE_STR, REF_STR])]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.xasRcpLcp.value ]:
            yLabels = ["".join([XAS_STR, UNDERSCORE_STR, TEY_STR, \
                                UNDERSCORE_STR, RCP_STR]), \
                       "".join([XAS_STR, UNDERSCORE_STR, TEY_STR, \
                                UNDERSCORE_STR, LCP_STR]), \
                       "".join([XAS_STR, UNDERSCORE_STR, TFY_STR, \
                                UNDERSCORE_STR, RCP_STR]), \
                       "".join([XAS_STR, UNDERSCORE_STR, TFY_STR, \
                                UNDERSCORE_STR, LCP_STR]), \
                       "".join([XAS_STR, UNDERSCORE_STR, REF_STR, \
                                UNDERSCORE_STR, RCP_STR]), \
                       "".join([XAS_STR, UNDERSCORE_STR, REF_STR, \
                                UNDERSCORE_STR, LCP_STR])]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.teyRcpLcp.value] :
            yLabels = ["".join([TEY_STR, UNDERSCORE_STR, RCP_STR]), \
                       "".join([TEY_STR, UNDERSCORE_STR, LCP_STR])]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.tfyRcpLcp.value] :
            yLabels = ["".join([TFY_STR, UNDERSCORE_STR, RCP_STR]), \
                       "".join([TFY_STR, UNDERSCORE_STR, LCP_STR])]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.refRcpLcp.value] :
            yLabels = ["".join([REF_STR, UNDERSCORE_STR, RCP_STR]), \
                       "".join([REF_STR, UNDERSCORE_STR, LCP_STR])]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.i0RcpLcp.value]:
            yLabels = ["".join([I0_STR, UNDERSCORE_STR, RCP_STR]), \
                       "".join([I0_STR, UNDERSCORE_STR, LCP_STR])]
        else:
            raise LookupError(" No data selection for " + \
                              str(self.plotSelector.currentText()))
        labels.extend(yLabels)
        return labels
    
    def getPlotSelections(self):
        retSelections = self.plotSelections[0]
        logger.debug(METHOD_ENTER_STR)
        return retSelections
        
    def getPlotLabels(self):
        labels = ["Energy",]
        addLabels = None
        if str(self.plotSelector.currentText()) == \
                                    PLOT_CHOICES[PlotChoiceId.xasXmcd]:
            addLabels = [XAS_STR + SPACE_STR + TEY_STR, \
                         XAS_STR + SPACE_STR + TFY_STR, \
                         XAS_STR + SPACE_STR + REF_STR, \
                         XMCD_STR + SPACE_STR + TEY_STR, \
                         XMCD_STR + SPACE_STR + TFY_STR, \
                         XMCD_STR + SPACE_STR + REF_STR]        
        elif str(self.plotSelector.currentText()) == \
                                PLOT_CHOICES[PlotChoiceId.xasRcpLcpXasXmcd]:
            addLabels = [XAS_STR + SPACE_STR + TEY_STR + SPACE_STR + RCP_STR,\
                         XAS_STR + SPACE_STR + TEY_STR + SPACE_STR + LCP_STR, \
                         XAS_STR + SPACE_STR + TFY_STR + SPACE_STR + RCP_STR,\
                         XAS_STR + SPACE_STR + TFY_STR + SPACE_STR + LCP_STR, \
                         XAS_STR + SPACE_STR + REF_STR + SPACE_STR + RCP_STR,\
                         XAS_STR + SPACE_STR + REF_STR + SPACE_STR + LCP_STR, \
                         XAS_STR + SPACE_STR + TEY_STR, \
                         XAS_STR + SPACE_STR + TFY_STR, \
                         XAS_STR + SPACE_STR + REF_STR, \
                         XMCD_STR + SPACE_STR + TEY_STR, \
                         XMCD_STR + SPACE_STR + TFY_STR, \
                         XMCD_STR + SPACE_STR + REF_STR]        
        elif str(self.plotSelector.currentText()) == \
                                        PLOT_CHOICES[PlotChoiceId.xasRcpLcp]:
            addLabels = [XAS_STR + SPACE_STR + TEY_STR + SPACE_STR + RCP_STR,\
                         XAS_STR + SPACE_STR + TEY_STR + SPACE_STR + LCP_STR, \
                         XAS_STR + SPACE_STR + TFY_STR + SPACE_STR + RCP_STR,\
                         XAS_STR + SPACE_STR + TFY_STR + SPACE_STR + LCP_STR, \
                         XAS_STR + SPACE_STR + REF_STR + SPACE_STR + RCP_STR,\
                         XAS_STR + SPACE_STR + REF_STR + SPACE_STR + LCP_STR]
        elif str(self.plotSelector.currentText()) == \
                                        PLOT_CHOICES[PlotChoiceId.teyRcpLcp]:
            addLabels = [TEY_STR + SPACE_STR + RCP_STR,\
                         TEY_STR + SPACE_STR + LCP_STR]
        elif str(self.plotSelector.currentText()) == \
                                        PLOT_CHOICES[PlotChoiceId.tfyRcpLcp]:
            addLabels = [TFY_STR + SPACE_STR + RCP_STR,\
                         TFY_STR + SPACE_STR + LCP_STR]
        elif str(self.plotSelector.currentText()) == \
                                        PLOT_CHOICES[PlotChoiceId.refRcpLcp]:
            addLabels = [REF_STR + SPACE_STR + RCP_STR,\
                         REF_STR + SPACE_STR + LCP_STR]
        elif str(self.plotSelector.currentText()) == \
                                        PLOT_CHOICES[PlotChoiceId.i0RcpLcp]:
            addLabels = [I0_STR + SPACE_STR + RCP_STR,\
                         I0_STR + SPACE_STR + LCP_STR]
        labels.extend(addLabels)
        return labels
        
    def setDefaultSelectionsFromCounterNames(self, names):
        logger.debug(METHOD_ENTER_STR, names)
        
    @qtCore.pyqtSlot(int)
    def choiceSelectorChanged(self, newType):
        logger.debug(newType)
        
    @qtCore.pyqtSlot(int)
    def plotCorrectedData(self):
        return False
    
    @qtCore.pyqtSlot(int)
    def plotSelectorChanged(self, newType):
        self.plotTypeChanged[int].emit(newType)
        
    def setPlotSelections(self, selections):
        pass
    
    def getPlotAxisLabelsIndex(self):
        plotTypes = self.getPlotAxisLabels()
        logger.debug("==== plot axis labels ")
        axisIndex = []
        axisIndex.append(0)    #x axis, kQTExifUserDataFlashEnergy
        for pType in plotTypes[1:]:
            if pType.startswith("XAS"):
                logger.debug("%s getting assigned label index %d" % (pType, 1) )
                axisIndex.append(1)
            elif pType.startswith("XMCD"):
                logger.debug("%s getting assigned label index %d" % (pType, 2) )
                axisIndex.append(2)
            else:
                axisIndex.append(1)
        logger.debug("axisIndexes %s" % axisIndex)
        return axisIndex
    
    def setDefaultSelectionXName(self, xName):
        DEFAULT_SELECTIONS[0][0] = xName
        DEFAULT_SELECTIONS[1][0] = xName
    
        
        