'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import PyQt4.QtGui as qtGui
import PyQt4.QtCore as qtCore
from xcirculardichro.gui.choices.undefinedchoices import UndefinedChoices
import logging
from xcirculardichro.gui.choices.nonlockinxmcdchoices import NonLockinXMCDChoices
from xcirculardichro.gui.choices.lockinxmcdchoices import LockinXMCDChoices
logger = logging.getLogger(__name__)
QXDICHRO = 'qxdichro'
QXSCAN = 'qxscan'

class ChoiceHolder(qtGui.QDialog):
    
    subTypeChanged = qtCore.pyqtSignal(int, name='subTypeChanged')
    plotTypeChanged = qtCore.pyqtSignal(int, name='plotTypeChanged')
    
    
    def __init__(self, parent=None):
        super(ChoiceHolder, self).__init__(parent)
        layout = qtGui.QHBoxLayout()
        self.choiceWidget = UndefinedChoices()
        self.lastChoiceType = "undefined"
        layout.addWidget(self.choiceWidget)
        self.choiceWidget.subTypeChanged[int].connect(self.choiceSelectionChanged)
        self.choiceWidget.plotTypeChanged[int].connect(self.plotSelectionChanged)
        self.setLayout(layout)
        self.show()
        
    def setChoiceWidget(self, choiceWidget):
        layout = self.layout()
        self.choiceWidget.subTypeChanged[int].disconnect(self.choiceSelectionChanged)
        self.choiceWidget.plotTypeChanged[int].disconnect(self.plotSelectionChanged)
        layout.removeWidget(self.choiceWidget)
        self.choiceWidget.deleteLater()
        self.choiceWidget = None
        self.choiceWidget = choiceWidget
        layout.addWidget(self.choiceWidget)
        self.choiceWidget.subTypeChanged[int].connect(self.choiceSelectionChanged)
        self.choiceWidget.plotTypeChanged[int].connect(self.plotSelectionChanged)
        self.choiceWidget.show()
        self.adjustSize()
        self.update()
        
    @qtCore.pyqtSlot(int)
    def choiceSelectionChanged(self, typeStr):
        self.subTypeChanged[int].emit(typeStr)

    def getPlotSelections(self):
        logger.debug("Entering")
        return self.choiceWidget.getPlotSelections()

    @qtCore.pyqtSlot(int)
    def plotSelectionChanged(self, typeStr):
        self.plotTypeChanged[int].emit(typeStr)
        
    def setChoiceWidgetByScanType(self, typeName):
        if self.lastChoiceType == typeName:        # done change anything
            return
        if typeName == QXDICHRO:
            logger.debug("setting choice to non-lockin")
            self.setChoiceWidget(NonLockinXMCDChoices())
        elif typeName == QXSCAN:
            logger.debug("setting choice to lockin")
            self.setChoiceWidget(LockinXMCDChoices())
        else:
            logger.debug("setting choice to other")
            self.setChoiceWidget(UndefinedChoices())
        self.lastChoiceType = typeName
        