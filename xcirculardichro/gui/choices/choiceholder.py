'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro.gui.choices.undefinedchoices import UndefinedChoices
import logging
from xcirculardichro.gui.choices.nonlockinxmcdchoices import \
    NonLockinXMCDChoices
from xcirculardichro.gui.choices.lockinxmcdchoices import LockinXMCDChoices
from xcirculardichro import METHOD_ENTER_STR
from xcirculardichro.gui.choices.multinonlockinxmcdchoices import \
    MultiNonLockinXMCDChoices
logger = logging.getLogger(__name__)
QXDICHRO = 'qxdichro'
QXSCAN = 'qxscan'
TEMPDICHRO = 'tempdichro'
KEPDICHRO = 'kepdichro'
XMCDVSE = 'XMCDvsE'

class ChoiceHolder(qtWidgets.QDialog):
    
    subTypeChanged = qtCore.pyqtSignal(int, name='subTypeChanged')
    plotTypeChanged = qtCore.pyqtSignal(int, name='plotTypeChanged')
    plotOptionChanged = qtCore.pyqtSignal(name="plotOptionChanged")
    
    
    def __init__(self, parent=None):
        super(ChoiceHolder, self).__init__(parent)
        layout = qtWidgets.QHBoxLayout()
        self.choiceWidget = UndefinedChoices()
        self.lastChoiceType = "undefined"
        layout.addWidget(self.choiceWidget)
        self.choiceWidget.subTypeChanged[int].connect(self.choiceSelectionChanged)
        self.choiceWidget.plotTypeChanged[int].connect(self.plotSelectionChanged)
        self.choiceWidget.plotOptionChanged.connect(self.handlePlotOptionChanged)
        self.setLayout(layout)
        self.show()
    
    @qtCore.pyqtSlot()    
    def handlePlotOptionChanged(self):
        logger.debug(METHOD_ENTER_STR)
        self.plotOptionChanged.emit()
        
    def setChoiceWidget(self, choiceWidget):
        logger.debug(METHOD_ENTER_STR)
        layout = self.layout()
        self.choiceWidget.subTypeChanged[int].disconnect(self.choiceSelectionChanged)
        self.choiceWidget.plotTypeChanged[int].disconnect(self.plotSelectionChanged)
        self.choiceWidget.plotOptionChanged.disconnect(self.handlePlotOptionChanged)
        layout.removeWidget(self.choiceWidget)
        self.choiceWidget.deleteLater()
        self.choiceWidget = None
        self.choiceWidget = choiceWidget
        layout.addWidget(self.choiceWidget)
        self.choiceWidget.subTypeChanged[int].connect(self.choiceSelectionChanged)
        self.choiceWidget.plotTypeChanged[int].connect(self.plotSelectionChanged)
        self.choiceWidget.plotOptionChanged.connect(self.handlePlotOptionChanged)
        self.choiceWidget.show()
        self.adjustSize()
        self.update()
        
    @qtCore.pyqtSlot(int)
    def choiceSelectionChanged(self, typeStr):
        self.subTypeChanged[int].emit(typeStr)

    def calcCorrectedData(self, y, preEdge=None, postEdge=None):
        logger.debug(METHOD_ENTER_STR % ((y,preEdge, postEdge),))
        logger.debug("preEdge %s" % preEdge)
        logger.debug("postEdge %s" % postEdge)
        return self.choiceWidget.calcCorrectedData(y, preEdge = preEdge, postEdge = postEdge)
        
    def getPlotSelections(self):
        logger.debug(METHOD_ENTER_STR)
        return self.choiceWidget.getPlotSelections()

    def plotAverageData(self):
        return self.choiceWidget.plotAverageData()
    
    def plotCorrectedData(self):
        return self.choiceWidget.plotCorrectedData()
    
    def plotIndividualData(self):
        return self.choiceWidget.plotIndividualData()
    
    def plotNormalizedData(self):
        return self.choiceWidget.plotNormalizedData()
    
    @qtCore.pyqtSlot(int)
    def plotSelectionChanged(self, typeStr):
        self.plotTypeChanged[int].emit(typeStr)
        
    def setChoiceWidgetByScanType(self, typeName):
        logger.debug(METHOD_ENTER_STR % typeName)
        if self.lastChoiceType == typeName:        # done change anything
            return
        if typeName == QXDICHRO:
            logger.debug("setting choice to non-lockin")
            self.setChoiceWidget(NonLockinXMCDChoices())
        elif typeName == TEMPDICHRO:
            logger.debug("setting choice to non-lockin tempdichro")
            self.setChoiceWidget(NonLockinXMCDChoices())
            self.choiceWidget.setDefaultSelectionsXName("Temperature")
        elif typeName == KEPDICHRO:
            logger.debug("setting choice to non-lockin kepdichro")
            self.setChoiceWidget(NonLockinXMCDChoices())
            self.choiceWidget.setDefaultSelectionsXName("KCurrVAL")
        elif typeName == QXSCAN:
            logger.debug("setting choice to lockin")
            self.setChoiceWidget(LockinXMCDChoices())
        elif typeName == XMCDVSE:
            logger.debug("setting choice to lockin")
            self.setChoiceWidget(MultiNonLockinXMCDChoices())
        else:
            logger.debug("setting choice to other")
            self.setChoiceWidget(UndefinedChoices())
        self.lastChoiceType = typeName
        
    def setDefaultSelectionsFromCounterNames(self, names):
        '''
        Pass this call down to the choiceWidget
        '''
        logger.debug(METHOD_ENTER_STR % names)
        self.choiceWidget.setDefaultSelectionsFromCounterNames(names)

        