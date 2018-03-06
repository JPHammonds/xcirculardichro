'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
import PyQt5.QtGui as qtGui
from xcirculardichro import METHOD_ENTER_STR, METHOD_EXIT_STR
logger = logging.getLogger(__name__)
DUMMY_MINIMUM = 999999.9
DUMMY_MAXIMUM = -999999.9

class RangeSelectionInfo(qtWidgets.QDialog):
    POINT_SELECTIONS = ["Pre-Edge", "Post-Edge"]
    AXIS_SELECTIONS = ["Left", "Right"]
    selectorTypeChanged = qtCore.pyqtSignal(int)
    selectorAxisChanged = qtCore.pyqtSignal(int)
    grabRangeFromSelection = qtCore.pyqtSignal()
    dataRangeChanged = qtCore.pyqtSignal(list, list)     
       
    def __init__(self, parent=None):
        super(RangeSelectionInfo, self).__init__(parent=parent)
        layout = qtWidgets.QVBoxLayout()
        layout.setSpacing(5)
        hLayout1 = qtWidgets.QHBoxLayout()
        label = qtWidgets.QLabel("PointSet to Select: ")
        hLayout1.addWidget(label)
        self.pointSetSelector = qtWidgets.QComboBox()
        self.pointSetSelector.insertItems(0, self.POINT_SELECTIONS)
        
        hLayout1.addWidget(self.pointSetSelector)
        layout.addLayout(hLayout1)
        
        hLayout2 = qtWidgets.QHBoxLayout()
        label = qtWidgets.QLabel("PointSelect Axis: ")
        hLayout2.addWidget(label)
        self.axisSelector = qtWidgets.QComboBox()
        self.axisSelector.insertItems(0, self.AXIS_SELECTIONS)
        hLayout2.addWidget(self.axisSelector)
        layout.addLayout(hLayout2)
        self.pointSelections = {}
        for selection in self.POINT_SELECTIONS:
            self.pointSelections[selection] = PointSetInfo(selection)
            layout.addWidget(self.pointSelections[selection])
            self.pointSelections[selection].dataRangeChanged.connect(self.handleRangeChanged)
        self.grabRangeButton = qtWidgets.QPushButton("Grab Range From Data")
        layout.addWidget(self.grabRangeButton)
        
        self.setLayout(layout)
        self.pointSetSelector.currentIndexChanged[int].connect(self.handlePointSetSelectorTypeChanged)
        self.axisSelector.currentIndexChanged[int].connect(self.handleAxisSelectionChanged)
        self.grabRangeButton.clicked.connect(self.grabRange)

    def edgeRangesAtDummyValues(self):
        logger.debug(METHOD_ENTER_STR)
        retValue = False
        if self.pointSelections[self.POINT_SELECTIONS[0]].rangeAtDummyValues() and \
            self.pointSelections[self.POINT_SELECTIONS[1]].rangeAtDummyValues():
            retValue = True
        logger.debug(METHOD_EXIT_STR % retValue)
        return retValue
        
    def getAxisSelection(self):
        return self.axisSelector.currentIndex()
    
    def getPointSetType(self):
        return self.pointSetSelector.currentIndex()
    
    def getPointSetAverageLeft(self):
        return self.pointSelections[self.POINT_SELECTIONS[0]].getAverage()
    
    def getPointSetAverageRight(self):
        return self.pointSelections[self.POINT_SELECTIONS[1]].getAverage()
    
    def getPointSetLeftPoints(self):
        infoSet = self.pointSelections[self.POINT_SELECTIONS[0]].getIndices()
        return infoSet
        
    def getPointSetRightPoints(self):
        infoSet = self.pointSelections[self.POINT_SELECTIONS[1]].getIndices()
        return infoSet
    
    def getPostEdgeRange(self):
        logger.debug(METHOD_ENTER_STR)
        return self.pointSelections[self.POINT_SELECTIONS[1]].getRange()

    def getPreEdgeRange(self):
        logger.debug(METHOD_ENTER_STR)
        return self.pointSelections[self.POINT_SELECTIONS[0]].getRange()

    @qtCore.pyqtSlot()
    def grabRange(self):
        self.grabRangeFromSelection.emit()
                
    def hasValidPointSelectionData(self):
        logger.debug(METHOD_ENTER_STR, 
                     ((self.getPointSetLeftPoints(),
                       self.getPointSetRightPoints()),))
        retValue = False
        if (len(self.getPointSetLeftPoints()) == 0) or \
            (len(self.getPointSetRightPoints()) == 0):
            logger
            retValue = False
        else:
            retValue = True
        logger.debug(METHOD_EXIT_STR % retValue)
        return retValue
        
    @qtCore.pyqtSlot(int)
    def handleAxisSelectionChanged(self, index):
        self.selectorAxisChanged[int].emit(index)
        
    @qtCore.pyqtSlot(int)
    def handlePointSetSelectorTypeChanged(self, index):
        self.selectorTypeChanged[int].emit(index)
        
    def handleRangeChanged(self, newRange):
        logging.debug(METHOD_ENTER_STR, newRange)
        self.dataRangeChanged.emit(self.getPreEdgeRange(), \
                                   self.getPostEdgeRange())
        
    @qtCore.pyqtSlot(int)
    def setAxisSelection(self, axis):
        self.axisSelector.setCurrentIndex(axis)
    
    @qtCore.pyqtSlot(int)
    def setPointSetType(self, setNum):
        self.pointSetSelector.setCurrentIndex(setNum)
    
    def setSelectionIndices(self, selectionType, indices):
        logger.debug(METHOD_ENTER_STR % ((selectionType,indices),))
        self.pointSelections[selectionType].setIndices(indices)
        
    def setSelectionAverage(self, selectionType, average):
        logger.debug(METHOD_ENTER_STR % ((selectionType,average),))
        self.pointSelections[selectionType].setAverage(average)
 
    def setPreEdgeRange(self, dataRange):
        self.pointSelections[self.POINT_SELECTIONS[0]].setRange(dataRange)

    def setPostEdgeRange(self, dataRange):
        self.pointSelections[self.POINT_SELECTIONS[1]].setRange(dataRange)
        
class PointSetInfo(qtWidgets.QDialog):

    dataRangeChanged = qtCore.pyqtSignal(list)

    def __init__(self, pointSetLabel, parent=None):
        super(PointSetInfo, self).__init__(parent=parent)
        layout = qtWidgets.QHBoxLayout()
        label = qtWidgets.QLabel(str(pointSetLabel))
        layout.addWidget(label)
        label = qtWidgets.QLabel("Minimum:")
        layout.addWidget(label)
        self.rangeMinimum = qtWidgets.QLineEdit(str(DUMMY_MINIMUM))
        self.rangeMinValidator = qtGui.QDoubleValidator()
        self.rangeMinimum.setValidator(self.rangeMinValidator)
        layout.addWidget(self.rangeMinimum)
        label = qtWidgets.QLabel("Maximum:")
        layout.addWidget(label)
        self.rangeMaximum = qtWidgets.QLineEdit(str(DUMMY_MAXIMUM))
        self.rangeMaxValidator = qtGui.QDoubleValidator()
        self.rangeMaximum.setValidator(self.rangeMaxValidator)
        layout.addWidget(self.rangeMaximum)
        
        self.rangeMinimum.editingFinished.connect(self.handleMinValueChanged)
        self.rangeMinimum.editingFinished.connect(self.handleMaxValueChanged)
        self.setLayout(layout)

    def getIndices(self):
        indices = []
#         indTxt = self.pointSetIndices.text()
#         logger.debug(METHOD_ENTER_STR % indTxt)
#         logger.debug("as a list of strings %s" % indTxt[1:-1])
#         indicesStr = indTxt[1:-1].split(',')
#         logger.debug("as a list of strings %s" % indicesStr)
#         indices = []
#         if len(indicesStr) > 0 and indicesStr[0] != '':
#             indices = list(map(int, indicesStr))
#             indices.sort()
#         logger.debug(METHOD_EXIT_STR %indices)
        return indices
    
    def getAverage(self):
        average = 0
        return float(average)
    
    def getRange(self):
        logger.debug(METHOD_ENTER_STR % ((str(self.rangeMinimum.text()),
                                         str(self.rangeMaximum.text())),))
        return [float(str(self.rangeMinimum.text())),
                float(str(self.rangeMaximum.text()))]
        
    @qtCore.pyqtSlot()
    def handleMinValueChanged(self):
        logger.debug(METHOD_ENTER_STR)
        self.dataRangeChanged.emit(self.getRange())
        
    @qtCore.pyqtSlot()
    def handleMaxValueChanged(self):
        logger.debug(METHOD_ENTER_STR)
        self.dataRangeChanged.emit(self.getRange())
        
    def rangeAtDummyValues(self):
        '''
        return True if both minimum and maximum are at their initial 
        dummy values
        '''
        logger.debug(METHOD_ENTER_STR)
        retValue = False
        if self.getRange() == [DUMMY_MINIMUM, DUMMY_MAXIMUM]:
            retValue = True
        logger.debug(METHOD_EXIT_STR % retValue)
        return retValue
        
    def setIndices(self, indices):
        logger.debug(METHOD_ENTER_STR % indices)
        #self.pointSetIndices.setText(str(indices))
        
    def setAverage(self, average):
        logger.debug(METHOD_ENTER_STR % average)
        #self.pointSetAverage.setText(str(average))
        
    def setRange(self, dataRange):
        self.rangeMinimum.setText(str(dataRange[0]))
        self.rangeMaximum.setText(str(dataRange[1]))
    

class PointSetSelector(qtWidgets.QDialog):
    
    def __init__(self, parent=None):
        super(PointSetSelector, self).__init__(parent=parent)
        