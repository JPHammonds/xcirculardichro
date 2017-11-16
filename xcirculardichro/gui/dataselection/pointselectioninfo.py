'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
from xcirculardichro import METHOD_ENTER_STR, METHOD_EXIT_STR
logger = logging.getLogger(__name__)

class PointSelectionInfo(qtWidgets.QDialog):
    POINT_SELECTIONS = ["Pre-Edge", "Post-Edge"]
    AXIS_SELECTIONS = ["Left", "Right"]
    selectorTypeChanged = qtCore.pyqtSignal(int)
    selectorAxisChanged = qtCore.pyqtSignal(int)        
    def __init__(self, parent=None):
        super(PointSelectionInfo, self).__init__(parent=parent)
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
        
        self.setLayout(layout)
        self.pointSetSelector.currentIndexChanged[int].connect(self.handlePointSetSelectorTypeChanged)
        self.axisSelector.currentIndexChanged[int].connect(self.handleAxisSelectionChanged)

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
        
class PointSetInfo(qtWidgets.QDialog):

    def __init__(self, pointSetLabel, parent=None):
        super(PointSetInfo, self).__init__(parent=parent)
        layout = qtWidgets.QHBoxLayout()
        label = qtWidgets.QLabel(str(pointSetLabel))
        layout.addWidget(label)
        label = qtWidgets.QLabel("Indices:")
        layout.addWidget(label)
        self.pointSetIndices = qtWidgets.QLabel("[]")
        layout.addWidget(self.pointSetIndices)
        label = qtWidgets.QLabel("Average:")
        layout.addWidget(label)
        self.pointSetAverage = qtWidgets.QLabel("None")
        layout.addWidget(self.pointSetAverage)
        
        self.setLayout(layout)

    def getIndices(self):
        indTxt = self.pointSetIndices.text()
        logger.debug(METHOD_ENTER_STR % indTxt)
        logger.debug("as a list of strings %s" % indTxt[1:-1])
        indicesStr = indTxt[1:-1].split(',')
        logger.debug("as a list of strings %s" % indicesStr)
        indices = []
        if len(indicesStr) > 0 and indicesStr[0] != '':
            indices = list(map(int, indicesStr))
            indices.sort()
        logger.debug(METHOD_EXIT_STR %indices)
        return indices
    
    def getAverage(self):
        return float(str(self.pointSetAverage.text()))
        
        
    def setIndices(self, indices):
        logger.debug(METHOD_ENTER_STR % indices)
        self.pointSetIndices.setText(str(indices))
        
    def setAverage(self, average):
        logger.debug(METHOD_ENTER_STR % average)
        self.pointSetAverage.setText(str(average))

class PointSetSelector(qtWidgets.QDialog):
    
    def __init__(self, parent=None):
        super(PointSetSelector, self).__init__(parent=parent)
        