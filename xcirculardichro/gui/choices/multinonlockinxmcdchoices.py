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

        dataSelectorLayout = qtWidgets.QHBoxLayout()
        self.dataSelector = {}
        label = qtWidgets.QLabel("Data Selection")
        self.dataSelector[TEY_STR] = qtWidgets.QCheckBox("TEY_STR")
        self.dataSelector[TFY_STR] = qtWidgets.QCheckBox("TFY_STR")
        self.dataSelector[REF_STR] = qtWidgets.QCheckBox("REF_STR")
        dataSelectorLayout.addWidget(label)
        dataSelectorLayout.addWidget(self.dataSelector[TEY_STR])
        dataSelectorLayout.addWidget(self.dataSelector[TFY_STR])
        dataSelectorLayout.addWidget(self.dataSelector[REF_STR])
        self.dataSelector[TEY_STR].stateChanged.connect(self.handleDataSelector)
        self.dataSelector[TFY_STR].stateChanged.connect(self.handleDataSelector)
        self.dataSelector[REF_STR].stateChanged.connect(self.handleDataSelector)
        
        layout.addLayout(dataSelectorLayout)

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

        xas = []
        xmcd = []
        xasChiral = []
        if self.useTEY():
            xas.append(xasTey)
            xmcd.append(xmcdTey)
            xasChiral.extend([xasTeyRCP, xasTeyLCP])
        if self.useTFY():
            xas.append(xasTfy)
            xmcd.append(xmcdTfy)
            xasChiral.extend([xasTfyRCP, xasTfyLCP])
        if self.useREF():
            xas.append(xasRef)
            xmcd.append(xmcdRef)
            xasChiral.extend([xasRefRCP, xasRefLCP])
        
        if str(self.plotSelector.currentText()) == str(PLOT_CHOICES[PlotChoiceId.xasXmcd.value]) :
            retData = [energy,]
            retData.extend(xas)
            retData.extend(xmcd)
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.xasRcpLcpXasXmcd.value]:
            retData = [energy, xasTeyRCP,xasTeyLCP, xasTfyRCP,xasTfyLCP, \
                    xasRefRCP,xasRefLCP, xasTey, xasTfy, xasRef, \
                    xmcdTey, xmcdTfy, xmcdRef]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.xasRcpLcp.value ]:
            retData = [energy, ]
            retData.extend(xasChiral)
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
        

    def getI0ChiralLabels(self):
        I0RCPStr = "".join([I0_STR, UNDERSCORE_STR, RCP_STR])
        I0LCPStr = "".join([I0_STR, UNDERSCORE_STR, LCP_STR])
        return I0RCPStr, I0LCPStr

    def getTeyChiralLabels(self):
        xasTeyRCPStr = "".join([XAS_STR, UNDERSCORE_STR, TEY_STR, \
                                UNDERSCORE_STR, RCP_STR])
        xasTeyLCPStr = "".join([XAS_STR, UNDERSCORE_STR, TEY_STR, \
                                UNDERSCORE_STR, LCP_STR])
        return xasTeyRCPStr, xasTeyLCPStr


    def getTfyChiralLabels(self):
        xasTfyRCPStr = "".join([XAS_STR, UNDERSCORE_STR, TFY_STR, \
                                UNDERSCORE_STR, RCP_STR])
        xasTfyLCPStr = "".join([XAS_STR, UNDERSCORE_STR, TFY_STR, \
                                UNDERSCORE_STR, LCP_STR])
        return xasTfyRCPStr, xasTfyLCPStr


    def getRefChiralLabels(self):
        xasRefRCPStr = "".join([XAS_STR, UNDERSCORE_STR, TFY_STR, \
                                UNDERSCORE_STR, RCP_STR])
        xasRefLCPStr = "".join([XAS_STR, UNDERSCORE_STR, TFY_STR, \
                                UNDERSCORE_STR, LCP_STR])
        return xasRefRCPStr, xasRefLCPStr

    def getFunctionLabels(self):
        xasTeyStr = "".join([XAS_STR, UNDERSCORE_STR, TEY_STR])
        xasTfyStr = "".join([XAS_STR, UNDERSCORE_STR, TFY_STR])
        xasRefStr = "".join([XAS_STR, UNDERSCORE_STR, REF_STR])
        xmcdTeyStr = "".join([XMCD_STR, UNDERSCORE_STR, TEY_STR])
        xmcdTfyStr = "".join([XMCD_STR, UNDERSCORE_STR, TFY_STR])
        xmcdRefStr = "".join([XMCD_STR, UNDERSCORE_STR, REF_STR])
        xasTeyRCPStr, xasTeyLCPStr = self.getTeyChiralLabels()
        xasTfyRCPStr, xasTfyLCPStr = self.getTfyChiralLabels()
        xasRefRCPStr, xasRefLCPStr = self.getRefChiralLabels()
        xasLabels = []
        xmcdLabels = []
        xasChiral = []
        if self.useTEY():
            xasLabels.append(xasTeyStr)
            xmcdLabels.append(xmcdTeyStr)
            xasChiral.extend([xasTeyRCPStr, xasTeyLCPStr])
        if self.useTFY():
            xasLabels.append(xasTfyStr)
            xmcdLabels.append(xmcdTfyStr)
            xasChiral.extend([xasTfyRCPStr, xasTfyLCPStr])
        if self.useREF():
            xasLabels.append(xasRefStr)
            xmcdLabels.append(xmcdRefStr)
            xasChiral.extend([xasRefRCPStr, xasRefLCPStr])
        return xasLabels, xmcdLabels, xasChiral

    def getPlotAxisLabels(self):
        labels = ["Energy",]

        xasLabels, xmcdLabels, xasChiral = self.getFunctionLabels()
        yLabels = []    
        if str(self.plotSelector.currentText()) == str(PLOT_CHOICES[PlotChoiceId.xasXmcd.value]) :
            yLabels.extend(xasLabels)
            yLabels.extend(xmcdLabels)
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.xasRcpLcpXasXmcd.value]:
            yLabels.extend(xasChiral)
            yLabels.extend(xasLabels)
            yLabels.extend(xmcdLabels)
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.xasRcpLcp.value ]:
            yLabels.extend(xasChiral)
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.teyRcpLcp.value] :
            xasTeyRCPStr, xasTeyLCPStr = self.getTeyChiralLabels()
            yLabels.append(xasTeyRCPStr)
            yLabels.append(xasTeyLCPStr)
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.tfyRcpLcp.value] :
            xasTfyRCPStr, xasTfyLCPStr = self.getTfyChiralLabels()
            yLabels.append(xasTfyRCPStr)
            yLabels.append(xasTfyLCPStr)
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.refRcpLcp.value] :
            xasRefRCPStr, xasRefLCPStr = self.getRefChiralLabels()
            yLabels.append(xasRefRCPStr)
            yLabels.append(xasRefLCPStr)
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[PlotChoiceId.i0RcpLcp.value]:
            i0RCPStr, i0LCPStr = self.getI0ChiralLabels()
            yLabels.append(i0RCPStr)
            yLabels.append(i0LCPStr)
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
        addLabels = []

        if str(self.plotSelector.currentText()) == \
                                    PLOT_CHOICES[PlotChoiceId.xasXmcd]:
            xasLabels, xmcdLabels, xasChiral = self.getFunctionLabels()
            addLabels.extend(xasLabels)
            addLabels.extend(xmcdLabels)
        elif str(self.plotSelector.currentText()) == \
                                PLOT_CHOICES[PlotChoiceId.xasRcpLcpXasXmcd]:
            xasLabels, xmcdLabels, xasChiral = self.getFunctionLabels()
            addLabels.extend(xasChiral)
            addLabels.extend(xasLabels)
            addLabels.extend(xmcdLabels)
        elif str(self.plotSelector.currentText()) == \
                                        PLOT_CHOICES[PlotChoiceId.xasRcpLcp]:
            xasLabels, xmcdLabels, xasChiral = self.getFunctionLabels()
            addLabels.extend(xasChiral)
        elif str(self.plotSelector.currentText()) == \
                                        PLOT_CHOICES[PlotChoiceId.teyRcpLcp]:
        
            xasTeyRCPStr, xasTeyLCPStr = self.getTeyChiralLabels()
            addLabels.append(xasTeyRCPStr)
            addLabels.append(xasTeyLCPStr)
        elif str(self.plotSelector.currentText()) == \
                                        PLOT_CHOICES[PlotChoiceId.tfyRcpLcp]:
            xasTfyRCPStr, xasTfyLCPStr = self.getTfyChiralLabels()
            addLabels.append(xasTfyRCPStr)
            addLabels.append(xasTfyLCPStr)
        elif str(self.plotSelector.currentText()) == \
                                        PLOT_CHOICES[PlotChoiceId.refRcpLcp]:
            xasRefRCPStr, xasRefLCPStr = self.getRefChiralLabels()
            addLabels.append(xasRefRCPStr)
            addLabels.append(xasRefLCPStr)
        elif str(self.plotSelector.currentText()) == \
                                        PLOT_CHOICES[PlotChoiceId.i0RcpLcp]:
            i0RCPStr, i0LCPStr = self.getI0ChiralLabels()
            addLabels.append(i0RCPStr)
            addLabels.append(i0LCPStr)
        labels.extend(addLabels)
        return labels
        
    def handleDataSelector(self, state):
        logger.debug(METHOD_ENTER_STR % state)
        self.plotOptionChanged.emit()
        
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
    
        
    def useTEY(self):
        '''
        Use TEY in plots and calculations
        '''
        return self.dataSelector[TEY_STR].isChecked()
        
    def useTFY(self):
        '''
        Use TFY in plots and calculations
        '''
        return self.dataSelector[TFY_STR].isChecked()
        
    def useREF(self):
        '''
        Use REF in plots and calculations
        '''
        return self.dataSelector[REF_STR].isChecked()
        
        