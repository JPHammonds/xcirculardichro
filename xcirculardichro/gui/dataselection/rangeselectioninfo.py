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

class RangeSelectionInfo(qtWidgets.QWidget):
    POINT_SELECTIONS = ["Pre-Edge", "Post-Edge"]
    AXIS_SELECTIONS = ["Left", "Right"]
    selectorTypeChanged = qtCore.pyqtSignal(int)
    selectorAxisChanged = qtCore.pyqtSignal(int)
    grabRangeFromSelection = qtCore.pyqtSignal()
    dataRangeChanged = qtCore.pyqtSignal(list, list)     
       
    def __init__(self, parent=None):
        super(RangeSelectionInfo, self).__init__(parent=parent)
        self.overallRange = [DUMMY_MINIMUM, DUMMY_MAXIMUM]
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

        
        self.preEdgeRangeSelection = RangeSetInfo(self.POINT_SELECTIONS[0])
        layout.addWidget(self.preEdgeRangeSelection)
        self.preEdgeRangeSelection.dataRangeChanged.connect(self.handleRangeChanged)
        
        self.postEdgeRangeSelection = RangeSetInfo(self.POINT_SELECTIONS[1])
        layout.addWidget(self.postEdgeRangeSelection)
        self.postEdgeRangeSelection.dataRangeChanged.connect(self.handleRangeChanged)
        
        
        self.grabRangeButton = qtWidgets.QPushButton("Grab Range From Data")
        layout.addWidget(self.grabRangeButton)
        
        self.setLayout(layout)
        self.pointSetSelector.currentIndexChanged[int].connect(self.handlePointSetSelectorTypeChanged)
        self.axisSelector.currentIndexChanged[int].connect(self.handleAxisSelectionChanged)
        self.grabRangeButton.clicked.connect(self.grabRange)

    def edgeRangesAtDummyValues(self):
        logger.debug(METHOD_ENTER_STR)
        retValue = False
        if self.preEdgeRangeSelection.rangeAtDummyValues() and \
            self.postEdgeRangeSelection.rangeAtDummyValues():
            retValue = True
        logger.debug(METHOD_EXIT_STR % retValue)
        return retValue
        
    def getAxisSelection(self):
        return self.axisSelector.currentIndex()
    
    def getPointSetType(self):
        return self.pointSetSelector.currentIndex()
    
    def getPostEdgeRange(self):
        logger.debug(METHOD_ENTER_STR)
        return self.postEdgeRangeSelection.getRange()

    def getPreEdgeRange(self):
        logger.debug(METHOD_ENTER_STR)
        return self.preEdgeRangeSelection.getRange()

    @qtCore.pyqtSlot()
    def grabRange(self):
        self.grabRangeFromSelection.emit()
                
    def hasValidRangeSelectionData(self):
        logger.debug(METHOD_ENTER_STR, 
                     ((self.getPreEdgeRange(),
                       self.getPostEdgeRange()),))
        retValue = False
        preRange = self.getPreEdgeRange()
        postRange = self.getPostEdgeRange()
        # Ranges have been  defined
        if ((len(preRange) == 0) or \
            (len(postRange) == 0)):
            #logger
            retValue = False
        # maxes need to be more tha mins
        elif preRange[1] < preRange[0] or \
            postRange[1] < postRange[0]:
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
    
    def setOverallRange(self, range):
        self.overallRange = range
    
    def setPreEdgeRange(self, dataRange):
        self.preEdgeRangeSelection.setRange(dataRange,self.overallRange)

    def setPostEdgeRange(self, dataRange):
        self.postEdgeRangeSelection.setRange(dataRange, self.overallRange)
        
    
        
class RangeSetInfo(qtWidgets.QWidget):

    dataRangeChanged = qtCore.pyqtSignal(list)

    def __init__(self, pointSetLabel, parent=None):
        super(RangeSetInfo, self).__init__(parent=parent)
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
        self.setRangeStatusColors("red")
        
        self.rangeMinimum.editingFinished.connect(self.handleMinValueChanged)
        self.rangeMinimum.textChanged.connect(self.handleMinValueTextChanged)
        self.rangeMaximum.editingFinished.connect(self.handleMaxValueChanged)
        self.rangeMaximum.textChanged.connect(self.handleMaxValueTextChanged)
        
        self.setLayout(layout)
    
    def getRange(self):
        logger.debug(METHOD_ENTER_STR % ((str(self.rangeMinimum.text()),
                                         str(self.rangeMaximum.text())),))
        return [float(str(self.rangeMinimum.text())),
                float(str(self.rangeMaximum.text()))]
        
    @qtCore.pyqtSlot()
    def handleMinValueChanged(self):
        logger.debug(METHOD_ENTER_STR)
        dataRange = self.getRange()
        self.rangeMaxValidator.setBottom(dataRange[0])
        self.dataRangeChanged.emit(dataRange)
        
    @qtCore.pyqtSlot(str)
    def handleMinValueTextChanged(self, currentText):
        logger.debug(METHOD_ENTER_STR % currentText)
        if not self.rangeMinimum.hasAcceptableInput():
            qtWidgets.QToolTip.showText(self.rangeMinimum.mapToGlobal(qtCore.QPoint()), 'Invalid Input')
        else:
            qtWidgets.QToolTip.hideText()
        
    @qtCore.pyqtSlot()
    def handleMaxValueChanged(self):
        logger.debug(METHOD_ENTER_STR)
        dataRange = self.getRange()
        self.rangeMinValidator.setTop(dataRange[1])
        self.dataRangeChanged.emit(dataRange)
        
    @qtCore.pyqtSlot(str)
    def handleMaxValueTextChanged(self, currentText):
        logger.debug(METHOD_ENTER_STR % currentText)
        if not self.rangeMaximum.hasAcceptableInput():
            qtWidgets.QToolTip.showText(self.rangeMaximum.mapToGlobal(qtCore.QPoint()), 'Invalid Input')
        else:
            qtWidgets.QToolTip.hideText()
        range = self.getRange()
        if range[0] > range[1]:
            self.setRangeStatusColors("red")
        else:
            self.setRangeStatusColors("white")
            
    def setRangeStatusColors(self, color):
        self.rangeMinimum.setStyleSheet("QLineEdit {background-color: %s}" % color)
        self.rangeMaximum.setStyleSheet("QLineEdit {background-color: %s}" % color)
        
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
        
    def setRange(self, dataRange, overallRange):
        self.rangeMinValidator.setBottom(overallRange[0])
        self.rangeMinValidator.setTop(dataRange[1])
        self.rangeMaxValidator.setBottom(dataRange[0])
        self.rangeMaxValidator.setTop(overallRange[1])
        self.rangeMinimum.setText(str(dataRange[0]))
        self.rangeMaximum.setText(str(dataRange[1]))
    

class RangeSetSelector(qtWidgets.QDialog):
    
    def __init__(self, parent=None):
        super(RangeSetSelector, self).__init__(parent=parent)
        