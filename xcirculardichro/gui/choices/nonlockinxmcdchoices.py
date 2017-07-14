'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import numpy as np
import PyQt4.QtGui as qtGui
import PyQt4.QtCore as qtCore
from xcirculardichro.gui.choices.abstractchoices import AbstractChoices
import logging
logger = logging.getLogger(__name__)

CHOICES = ['Flourescence', 'Transmission']
DEFAULT_SELECTIONS = [["Energy", "SCAtot2(+)", "SCAtot2(-)", "IC3(+)", "IC3(-)"], 
                      ["Energy", "IC5(+)", "IC5(-)", "IC4(+)", "IC5(-)"] ]
PLOT_CHOICES = ["XAS/XMCD", "XAS+/XAS-/XAS/XMCD", "XAS+/XAS-", "D+/D-", "M+/M-"]
    

class NonLockinXMCDChoices(AbstractChoices):
    COUNTER_OPTS = ["Energy", "D+", "D-", "M+", "M-"]

    def __init__(self, parent=None):
        super(NonLockinXMCDChoices, self).__init__(parent)
        logger.debug ("Entering")
        layout = self.layout()     

        choiceLayout = qtGui.QHBoxLayout()
        label = qtGui.QLabel("Data Type: ")
        self.choiceSelector = qtGui.QComboBox()
        self.choiceSelector.insertItems(0, CHOICES)
        choiceLayout.addWidget(label)
        choiceLayout.addWidget(self.choiceSelector)
        
        plotLayout = qtGui.QHBoxLayout()
        label = qtGui.QLabel("Plot Type: ")
        self.plotSelector = qtGui.QComboBox()
        self.plotSelector.insertItems(0, PLOT_CHOICES)
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
        return retData
        
    def getPlotSelections(self):
        retSelections = None
#         if str(self.choiceSelector.itemText()) == CHOICES[0]:
        retSelections = self.plotSelections[self.choiceSelector.currentIndex()]
#         elif str(self.choiceSelector.itemText()) == CHOICES[1]:
#             retSelections = self.plotSelections[1]
        return retSelections

    def getPlotAxisLabels(self):
        labels = ["Energy",]
        labels.extend(str(self.plotSelector.currentText()).split('/'))
        return labels
    
    @qtCore.pyqtSlot(int)
    def choiceSelectorChanged(self, newType):
        self.plotSelections = DEFAULT_SELECTIONS[newType]
        self.subTypeChanged[int].emit(newType)
        
    @qtCore.pyqtSlot(int)
    def plotSelectorChanged(self, newType):
        self.plotTypeChanged[int].emit(newType)
        
    def setPlotSelections(self, selections):
        if str(self.choiceSelector.currentText()) == CHOICES[0]:
            self.plotSelections[0] = selections
        elif str(self.choiceSelector.currentText()) == CHOICES[1]:
            self.plotSelections[1] = selections
