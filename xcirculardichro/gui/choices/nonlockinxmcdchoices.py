'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import numpy as np
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro.gui.choices.abstractchoices import AbstractChoices
import logging
from xcirculardichro import METHOD_ENTER_STR, METHOD_EXIT_STR
logger = logging.getLogger(__name__)

CHOICES = ['Flourescence', 'Transmission']
DEFAULT_SELECTIONS = [["Energy", "SCAtot2(+)", "SCAtot2(-)", "IC3(+)", "IC3(-)"], 
                      ["Energy", "IC5(+)", "IC5(-)", "IC4(+)", "IC5(-)"] ]
PLOT_CHOICES = ["XAS/XMCD", "XAS+/XAS-/XAS/XMCD", "XAS+/XAS-", "D+/D-", "M+/M-"]
ZERO = 0.00000000
ONE = 1.0000000

class NonLockinXMCDChoices(AbstractChoices):
    COUNTER_OPTS = ["Energy", "D+", "D-", "M+", "M-"]

    def __init__(self, parent=None):
        super(NonLockinXMCDChoices, self).__init__(parent)
        logger.debug (METHOD_ENTER_STR)
        layout = self.layout()     

        choiceLayout = qtWidgets.QHBoxLayout()
        label = qtWidgets.QLabel("Data Type: ")
        self.choiceSelector = qtWidgets.QComboBox()
        self.choiceSelector.insertItems(0, CHOICES)
        choiceLayout.addWidget(label)
        choiceLayout.addWidget(self.choiceSelector)
        
        plotLayout = qtWidgets.QHBoxLayout()
        label = qtWidgets.QLabel("Plot Type: ")
        self.plotSelector = qtWidgets.QComboBox()
        self.plotSelector.insertItems(0, PLOT_CHOICES)
        self.plotSelector.setCurrentIndex(0)
        plotLayout.addWidget(label)
        plotLayout.addWidget(self.plotSelector)
        
        layout.addLayout(choiceLayout)
        layout.addLayout(plotLayout)
        
        self.choiceSelector.currentIndexChanged[int].connect(self.choiceSelectorChanged)
        self.plotSelector.currentIndexChanged[int].connect(self.plotSelectorChanged)
        self.setLayout(layout)
        self.plotSelections = DEFAULT_SELECTIONS
#         self.show()
        
    def calcPlotData(self, data):
        logger.debug(METHOD_ENTER_STR % data)
        xasPlus = None
        xasMinus = None
        xas = None
        xmcd = None
        energy = np.array(data[0])
        dPlus = np.array(data[1])
        dMinus = np.array(data[2])
        mPlus = np.array(data[3])
        mMinus = np.array(data[4])
        if str(self.choiceSelector.currentText()) == CHOICES[0]:     # Transmision
            xasPlus = dPlus/mPlus
            xasMinus = dMinus/mMinus
            xas = (xasPlus + xasMinus)/2
            xmcd = xasPlus - xasMinus
        elif str(self.choiceSelector.currentText()) == CHOICES[1]:     # Transmision
            xasPlus = np.log(mPlus/dPlus)
            xasMinus = np.log(mMinus/dPlus)
            xas = (xasPlus + xasMinus)/2
            xmcd = xasPlus - xasMinus

        retData = None
        if str(self.plotSelector.currentText()) == PLOT_CHOICES[0]:
            retData = [energy, xas, xmcd]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[1]:
            retData = [energy, xasPlus, xasMinus, xas, xmcd]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[2]:
            retData = [energy, xasPlus, xasMinus]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[3]:
            retData = [energy, dPlus, dMinus]
        elif str(self.plotSelector.currentText()) == PLOT_CHOICES[4]:
            retData = [energy, mPlus, mMinus]
        logger.debug(METHOD_EXIT_STR % retData)
        return retData

    def calcCorrectedData(self, data, preEdge=None, postEdge=None):
        logger.debug(METHOD_ENTER_STR, ((data,preEdge, postEdge),))
        correctedData = []
        xas = data[0]
        xmcd = data[1]
        correctedData.append((xas-preEdge)/(postEdge-preEdge))
        correctedData.append((xmcd)/(postEdge-preEdge))
#        correctedData = [xasCor, xmcdCor]
        logger.debug(METHOD_EXIT_STR % correctedData)
        return correctedData
        
        
    def getPlotSelections(self):
        retSelections = self.plotSelections[self.choiceSelector.currentIndex()]
        logger.debug(METHOD_ENTER_STR % retSelections)
        return retSelections

    def getPlotAxisLabels(self):
        labels = ["Energy",]
        labels.extend(str(self.plotSelector.currentText()).split('/'))
        return labels
    
    def setDefaultSelectionsFromCounterNames(self, names):
        '''
        Override the default choices.  Should have been more like this in the 
        begunning so may need to look at a way to get this up front.
        For Sector 4-ID their non-lockin data usually has 3 columns labeled 
        [sum, diff, flip].  If you find these at the bottom of the file than 
        the two prior columns are D+/D- and the two before that are M
        '''
        logger.debug(METHOD_ENTER_STR % names)
        END_NAMES = ['sum', 'diff', 'flip']
        logger.debug("Names at end of list: %s"% names[-3:])
        if names[-3:] == END_NAMES:
            self.plotSelections=[[DEFAULT_SELECTIONS[0][0], names[-5], names[-4], names[-7], names[-6]],
                                 [DEFAULT_SELECTIONS[1][0], names[-5], names[-4], names[-7], names[-6]]]
            logger.debug("New plotSelections %s" % self.plotSelections )
    
    @qtCore.pyqtSlot(int)
    def choiceSelectorChanged(self, newType):
        self.plotSelections = DEFAULT_SELECTIONS[newType]
        self.subTypeChanged[int].emit(newType)
        
    @qtCore.pyqtSlot()
    def plotCorrectedData(self):
        return True
        
    @qtCore.pyqtSlot(int)
    def plotSelectorChanged(self, newType):
        self.plotTypeChanged[int].emit(newType)
        
    def setPlotSelections(self, selections):
        if str(self.choiceSelector.currentText()) == CHOICES[0]:
            self.plotSelections[0] = selections
        elif str(self.choiceSelector.currentText()) == CHOICES[1]:
            self.plotSelections[1] = selections

    #Assign an output to Y-axis 1 or 2 to 
    def getPlotAxisLabelsIndex(self):
        plotTypes = self.plotSelector.currentText().split("/")
        axisIndex = []
        axisIndex.append(0)    #x axis, kQTExifUserDataFlashEnergy
        for pType in plotTypes:
            if pType.startswith("XAS"):
                axisIndex.append(1)
            elif pType.startswith("XMCD"):
                axisIndex.append(2)
            elif pType.startswith('D+') or pType.startswith('w-'):
                axisIndex.append(1)
            elif pType.startswith('M+') or pType.startswith('w-'):
                axisIndex.append(2)
            else:
                axisIndex.append(1)
        logger.debug("axisIndexes %s" % axisIndex)
        return axisIndex
        
    def setDefaultSelectionsXName(self, xName):
        DEFAULT_SELECTIONS[0][0] = xName
        DEFAULT_SELECTIONS[1][0] = xName
        