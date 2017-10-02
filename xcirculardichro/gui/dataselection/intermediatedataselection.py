'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import numpy as np
import logging
from xcirculardichro.gui.dataselection.AbstractSelectionDisplay import AbstractSelectionDisplay
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtGui as qtGui
import PyQt5.QtCore as qtCore
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR
from xcirculardichro.gui.choices.intermediatechoices import IntermediateChoices
from xcirculardichro.gui.dataselection.PointSelectionInfo import PointSelectionInfo

SCAN_COL = 0
CMD_COL = 1
logger = logging.getLogger(__name__)

class IntermediateDataSelection(AbstractSelectionDisplay):
    
    def __init__(self, parent=None):
        super(IntermediateDataSelection, self).__init__(parent=parent)
        self.selectedScans = []
        layout = qtWidgets.QVBoxLayout()
        self.scanBrowser = ScanBrowser()
        self.subChoices = IntermediateChoices()
        self.pointSelectionInfo = PointSelectionInfo()
        
        layout.addWidget(self.scanBrowser)
        layout.addWidget(self.subChoices)
        layout.addWidget(self.pointSelectionInfo)
        
        self.setLayout(layout)
        self.show()
        
        self.scanBrowser.scanSelected[list].connect(self.handleScanSelection)
        self.subChoices.plotOptionChanged.connect(self.plotOptionChanged)
        
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
#         return self._selectedNodes[0].scans[self.selectedScans[0]].data
        
#     def getNodeContainingScan(self, scan):
#         nodeContainingScan = self._selectedNodes[0]
#         for node in self._selectedNodes:
#             for scan in node.scans:
#                 if self.selectedScans[0] == scan:
#                     nodeContainingScan = node
#         return nodeContainingScan
        
    def getPlotAxisLabels(self):
        logger.debug(METHOD_ENTER_STR)
        logger.debug("selectedScans" % self.selectedScans)
        try:
            node = self.getNodeContainingScan(self.selectedScans[0])
        except IndexError as ex:
            logger.exception(ex)
            raise(ex)
        return node.scans[self.selectedScans[0]].axisLabels
        
#     def getDataLabels(self):
#         AbstractSelectionDisplay.getDataLabels(self)
        
    def getPlotAxisLabelsIndex(self):
        if (len(self.selectedScans) > 0):
            node = self.getNodeContainingScan(self.selectedScans[0])
            return node.scans[self.selectedScans[0]].axisLabelIndex
        else:
            return "Unknown"
        
    def getSelectedCounterInfo(self):
        logger.debug(METHOD_ENTER_STR % self.selectedScans)
        counters = []
        counterNames = []
        if len(self.selectedScans) > 0:
            nodeContainingScan = self.getNodeContainingScan(self.selectedScans[0])
            counters = []
            counterNames = nodeContainingScan.scans[self.selectedScans[0]].axisLabels
        return counters, counterNames

    def setLeftDataSelection(self, label, selection, average):
        pass
    
    def setRightDataSelection(self, label, selection, average):
        pass

    def getSelectedScans(self):
        return self.selectedScans
        

    def handleScanSelection(self, selectedScans):
        logger.debug(METHOD_ENTER_STR % selectedScans)
        self.selectedScans = selectedScans
        self.dataSelectionsChanged.emit()
        
    def plotIndividualData(self):
        return self.subChoices.plotIndividualData()
        
    def plotAverageData(self):
        return self.subChoices.plotAverageData()

    def setLeftDataSelection(self, label, selection, average):
        logger.debug(METHOD_ENTER_STR % (+label, selection, average))
    
    def setRightDataSelection(self, label, selection, average):
        logger.debug(METHOD_ENTER_STR % (label, selection, average))
    
    def setupDisplayWithSelectedNodes(self):
        self.scanBrowser.clearBrowser()
        for node in self._selectedNodes:
            self.scanBrowser.appendNode(node)
    

class ScanBrowser(qtWidgets.QDialog):
    scanSelected = qtCore.pyqtSignal(list, name="scanSelected")
    
    def __init__(self, parent=None):
        super(ScanBrowser, self).__init__(parent=parent)
        layout = qtWidgets.QHBoxLayout()
        #
        self.scanList = qtWidgets.QTableWidget()
        self.scanList.setColumnCount(2)
        self.scanList.setSelectionBehavior(qtWidgets.QAbstractItemView.SelectRows)
        self.scanList.setHorizontalHeaderLabels(['S#', 'Command'])
        font = qtGui.QFont("Helvetica", pointSize=10)
        self.scanList.setFont(font)
 
        layout.addWidget(self.scanList)
        self.setMinimumWidth(400)
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