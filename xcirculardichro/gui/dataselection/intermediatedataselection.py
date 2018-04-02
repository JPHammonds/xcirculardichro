'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import numpy as np
import logging
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtGui as qtGui
import PyQt5.QtCore as qtCore

from xcirculardichro.gui.dataselection import SelectionTypeNames,\
    AbstractSelectionDisplay
from xcirculardichro import METHOD_ENTER_STR
from xcirculardichro.gui.choices import IntermediateChoices
from xcirculardichro.gui.dataselection import RangeSelectionInfo

SCAN_COL = 0
CMD_COL = 1
INVERT_COL = 2
logger = logging.getLogger(__name__)

class IntermediateDataSelection(AbstractSelectionDisplay):
    
    def __init__(self, parent=None):
        super(IntermediateDataSelection, self).__init__(parent=parent)
        self.selectionType = SelectionTypeNames.INTERMEDIATE_SELECTION
        self.scanBrowser = ScanBrowser()
        self.subChoices = IntermediateChoices()
        self.rangeSelectionInfo = RangeSelectionInfo()
        
        self.addWidget(self.scanBrowser)
        self.addWidget(self.subChoices)
        self.addWidget(self.rangeSelectionInfo)
        
        self.show()
        
        self.scanBrowser.scanSelected[list].connect(self.handleScanSelection)
        self.subChoices.plotOptionChanged.connect(self.plotOptionChanged)
        self.rangeSelectionInfo.selectorTypeChanged[int].connect(self.handleSelectorTypeChanged)
        self.rangeSelectionInfo.selectorAxisChanged[int].connect(self.handleSelectorAxisChanged)
        self.rangeSelectionInfo.grabRangeFromSelection.connect(self.setDefSelectedScansRange)
        self.rangeSelectionInfo.dataRangeChanged.connect(self.handleEdgeRangeChanged)
        
    def isMultipleScansSelected(self):
        if len(self.selectedScans) > 1:
            return True
        else: 
            return False
        
    def calcPlotData(self, data):
        retData = []
        for index in range(len(data)):
            retData.append(np.array(data[index][:]))
        return retData
        
        
    def getCorrectedData(self, x, y):
        logger.debug(METHOD_ENTER_STR)
        preEdgeRange = self.rangeSelectionInfo.getPreEdgeRange()
        logger.debug("preEdge: %s" % preEdgeRange)
        postEdgeRange = self.rangeSelectionInfo.getPostEdgeRange()
        logger.debug("postEdge: %s" % postEdgeRange)
        return self.subChoices.calcStepCorrectedData(y, \
                                                 preEdge=preEdgeRange, \
                                                 postEdge=postEdgeRange)
        
    def getPlotAxisLabels(self):
        logger.debug(METHOD_ENTER_STR)
        logger.debug("selectedScans" % self.selectedScans)
        try:
            node = self.getNodeContainingScan(self.selectedScans[0])
        except IndexError as ex:
            logger.exception(ex)
            raise(ex)
        return node.scans[self.selectedScans[0]].axisLabels
        
    def getPlotAxisLabelsIndex(self):
        if (len(self.selectedScans) > 0):
            node = self.getNodeContainingScan(self.selectedScans[0])
            return node.scans[self.selectedScans[0]].axisLabelIndex
        else:
            return "Unknown"
        
    def getPostEdgeRange(self):
        return self.rangeSelectionInfo.getPostEdgeRange()
        
    def getPreEdgeRange(self):
        return self.rangeSelectionInfo.getPreEdgeRange()
        
    def getSelectedCounterInfo(self):
        logger.debug(METHOD_ENTER_STR % self.selectedScans)
        counters = []
        counterNames = []
        if len(self.selectedScans) > 0:
            nodeContainingScan = self.getNodeContainingScan(self.selectedScans[0])
            counters = []
            counterNames = nodeContainingScan.scans[self.selectedScans[0]].axisLabels
        return counters, counterNames

    def getSelectedEdgeRangeData(self):
        return (self.rangeSelectionInfo.getPreEdgeRange(),
                self.rangeSelectionInfo.getPostEdgeRange())
        
    def getSelectedScans(self):
        return self.selectedScans
        
    def handleEdgeRangeChanged(self, preEdgeRange, postEdgeRange):
        logger.debug(METHOD_ENTER_STR, ((preEdgeRange, postEdgeRange),))
        self.rangeValuesChanged.emit(preEdgeRange, postEdgeRange)
        

    def handleScanSelection(self, selectedScans):
        logger.debug(METHOD_ENTER_STR % selectedScans)
        self.selectedScans = selectedScans
        self.dataSelectionsChanged.emit()
        self.pointSelectionTypeChanged.emit(self.rangeSelectionInfo.getPointSetType())
        self.pointSelectionAxisChanged.emit(self.rangeSelectionInfo.getAxisSelection())
        
    def hasRangeSelectionWidget(self):
        return self.rangeSelectionInfo.hasValidRangeSelectionData()
    
    def hasValidRangeSelectionData(self):
        return self.rangeSelectionInfo.hasValidRangeSelectionData()
    
    def plotIndividualData(self):
        return self.subChoices.plotIndividualData()
        
    def plotAverageData(self):
        return self.subChoices.plotAverageData()

    def plotCorrectedData(self):
        return False
        
    def plotNormalizedData(self):
        if self.subChoices.plotNormalizedData():
            return self.subChoices.plotNormalizedData()
        
        else:
            return False
    
    def setDefSelectedScansRange(self):
        logger.debug(METHOD_ENTER_STR)
        scans = self.selectedScans
        minScan = None
        maxScan = None
        percentFromEdge = 0.05
        
        counters, counterNames = self.getSelectedCounterInfo()
        
        if len(scans) > 0:
            for scan in scans:
                node = self.getNodeContainingScan(scan)
                thisScan = node.scans[scan]
                logger.debug("thisScan %s" % thisScan)
                logger.debug("thisScan.data %s" % thisScan.data)
                axisCounter = counterNames[0]
                logger.debug(axisCounter)
                try:
                    dataThisScan = thisScan.data[axisCounter][:]
                    logger.debug("dataThisScan %s" % dataThisScan)
                    if dataThisScan is not None and len(dataThisScan) > 1:
                        
                        if self.isDataIncreasingX(dataThisScan):
                            if minScan is None:
                                minScan = dataThisScan[0]
                            else:
                                minScan = minScan if minScan < dataThisScan[0] \
                                    else dataThisScan[0]
                            if maxScan is None:
                                maxScan = dataThisScan[-1]
                            else:
                                maxScan = maxScan if maxScan > dataThisScan[-1] \
                                    else dataThisScan[-1]
                        else:
                            if minScan is None:
                                minScan = dataThisScan[-1]
                            else:
                                minScan = minScan if minScan < dataThisScan[-1] \
                                    else dataThisScan[-1]
                            if maxScan is None:
                                maxScan = dataThisScan[0]
                            else:
                                maxScan = maxScan if maxScan > dataThisScan[0] \
                                    else dataThisScan[0]
                    else: 
                        return
                        
                except KeyError:
                    logger.exception("Tried to load data that does "  +\
                                     "not have counters selected.")
                
                minPlus = minScan + (maxScan - minScan) * percentFromEdge
                maxMinus = maxScan - (maxScan - minScan) * percentFromEdge
                logger.debug("minScan, minPlus: %s" % ((minScan, minPlus),) )
                logger.debug("maxMinus, minScan: %s" % ((maxMinus, minScan),) )
                self.rangeSelectionInfo.setOverallRange([minScan, maxScan])
                self.rangeSelectionInfo.setPreEdgeRange([minScan, minPlus])
                self.rangeSelectionInfo.setPostEdgeRange([maxMinus, maxScan])
        self.rangeValuesChanged.emit(self.getPreEdgeRange(), 
                                     self.getPostEdgeRange())
        
    def setPositionersToDisplay(self, positioners):
        logger.debug(METHOD_ENTER_STR)
        self.scanBrowser.setPositionersToDisplay(positioners)
        
        
    def setupDisplayWithSelectedNodes(self):
        self.scanBrowser.clearBrowser()
        for node in self._selectedNodes:
            self.scanBrowser.appendNode(node)
        self.scanBrowser.scanList.selectRow(0)
    

class ScanBrowser(qtWidgets.QDialog):
    scanSelected = qtCore.pyqtSignal(list, name="scanSelected")
    
    def __init__(self, parent=None):
        super(ScanBrowser, self).__init__(parent=parent)
        self.positionersToShow = []
        self.userParamsToShow = []
        layout = qtWidgets.QHBoxLayout()
        #
        self.scanList = qtWidgets.QTableWidget()
        self.scanList.setColumnCount(3)
        self.scanList.setEditTriggers(qtWidgets.QAbstractItemView.NoEditTriggers)
        self.scanList.setSelectionBehavior(qtWidgets.QAbstractItemView.SelectRows)
        self.scanList.setHorizontalHeaderLabels(['S#', 'Command', 'Invert'])
        font = qtGui.QFont("Helvetica", pointSize=10)
        self.scanList.setFont(font)
 
        layout.addWidget(self.scanList)
        self.setMinimumWidth(400)
        self.setMinimumHeight(250)
        self.setMaximumWidth(600)
        
        self.setLayout(layout)
        self.show()
        
        self.scanList.itemSelectionChanged.connect(self.scanSelectionChanged)
        
    def appendNode(self, node):
        logger.debug(METHOD_ENTER_STR % type(node))
        scanKeys = list(node.scans.keys())
        for scanItem in scanKeys:
            row = self.scanList.rowCount()
            self.scanList.setRowCount(row + 1)
            logger.debug("scan, scanType %s, %s " %(node.scans[scanItem], type(node.scans[scanItem])))
            self.scanList.setItem(row, 
                                  SCAN_COL, 
                                  qtWidgets.QTableWidgetItem(str(node.scans[scanItem].scanNum)))
            self.scanList.setItem(row, 
                                  CMD_COL, 
                                  qtWidgets.QTableWidgetItem(str(node.scans[scanItem].scanCmd)))
            self.scanList.setCellWidget(row,
                                  INVERT_COL,
                                  qtWidgets.QCheckBox())
        
    def clearBrowser(self):
        for row in range(self.scanList.rowCount()):
            self.scanList.setItem(row, SCAN_COL, None)
        self.scanList.setRowCount(0)
        
    def scanSelectionChanged(self):
        logger.debug(METHOD_ENTER_STR)
        selectedItems = self.scanList.selectedIndexes()
        selectedScans = []
        for item in selectedItems:
            if item.column() == 0:
                scan = str(self.scanList.item(item.row(),0).text())
                selectedScans.append(scan)
        self.scanSelected[list].emit(selectedScans)
        
    def setPositionersToDisplay(self, positioners):
        self.positionersToShow = positioners
        
    def setTemperatureParamsToDisplay(self, temperatureParams):
        self.temperatureParamsToShow = temperatureParams        

    def setUserParamsToDisplay(self, userParams):
        self.userParamsToShow = userParams