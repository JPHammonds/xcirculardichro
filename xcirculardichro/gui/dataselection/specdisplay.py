'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging

import numpy as np
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
from PyQt5.QtWidgets import QAbstractItemView
from specguiutils.scantypeselector import ScanTypeSelector, SCAN_TYPES
from specguiutils.scanbrowser import ScanBrowser
from specguiutils.counterselector import CounterSelector

from xcirculardichro import METHOD_ENTER_STR,\
    METHOD_EXIT_STR
from xcirculardichro.gui.dataselection import RangeSelectionInfo
from xcirculardichro.gui.dataselection import SelectionTypeNames
from xcirculardichro.gui.dataselection import AbstractSelectionDisplay
from xcirculardichro.gui.choices import ChoiceHolder
    

logger = logging.getLogger(__name__)

class SpecDisplay(AbstractSelectionDisplay):
    
    def __init__(self, parent=None):
        super(SpecDisplay, self).__init__(parent)
        
        self.selectionType = SelectionTypeNames.SPEC_SELECTION
        self.currentSelections = {}
        self.typeSelector = ScanTypeSelector()
        self.scanBrowser = ScanBrowser()
        self.subChoices = ChoiceHolder()
        self.typeSelector.setCurrentType(0)
        self.counterSelector = CounterSelector(
            counterOpts = self.subChoices.choiceWidget.COUNTER_OPTS)
        self.scanBrowser.scanList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.rangeSelectionInfo = RangeSelectionInfo()
        
        self.addWidget(self.typeSelector)
        self.addWidget(self.scanBrowser)
        self.addWidget(self.subChoices)
        self.addWidget(self.counterSelector)
        self.addWidget(self.rangeSelectionInfo)
        
        
        self.scanBrowser.scanSelected[list].connect(self.handleScanSelection)
        self.scanBrowser.scanLoaded[bool].connect(self.handleScanLoaded)
        self.counterSelector.counterOptChanged[str, int, bool] \
            .connect(self.handleCounterOptChanged)
        self.counterSelector.counterView.counterDataChanged[list] \
            .connect(self.handleCounterDataChanged)
        self.typeSelector.scanTypeChanged[int].connect(self.scanTypeSelected)
        self.subChoices.subTypeChanged[int].connect(self.handleSubTypeChanged)
        self.subChoices.plotTypeChanged[int].connect(self.handlePlotTypeChanged)
        self.subChoices.plotOptionChanged.connect(self.handlePlotOptionChanged)
        self.rangeSelectionInfo.selectorTypeChanged[int].connect(self.handleSelectorTypeChanged)
        self.rangeSelectionInfo.selectorAxisChanged[int].connect(self.handleSelectorAxisChanged)
        self.rangeSelectionInfo.grabRangeFromSelection.connect(self.setDefSelectedScansRange)
        self.rangeSelectionInfo.dataRangeChanged.connect(self.handleEdgeRangeChanged)
        self.show()
        
    
    def calcPlotData(self, data):
        return self.subChoices.choiceWidget.calcPlotData(data)
        
    def copyPickedPointsToData(self):
        leftIndices = self.rangeSelectionInfo.pointSelections[RangeSelectionInfo.POINT_SELECTIONS[0]].getIndices()
        rightIndices = self.rangeSelectionInfo.pointSelections[RangeSelectionInfo.POINT_SELECTIONS[1]].getIndices()
        logger.debug("Points to copy to another Left: %s Right: %s" % (leftIndices, rightIndices) )
        self.pointSelectionReloadPicks.emit(leftIndices, rightIndices)

    def getAverageFromRange(self, x, y, range):
        logger.debug(METHOD_ENTER_STR)
        logger.debug(x)
        logger.debug(y)
        logger.debug(range)
        valsInRange = np.where((x >= range[0]) & (x <= range[1]))
        logger.debug("valsInRange %s" % valsInRange)
        logger.debug("y[valuesInRange] %s" % y[0][valsInRange])
        avgInRange = np.sum(y[0][valsInRange])/len(valsInRange[0])
        logger.debug(METHOD_EXIT_STR % avgInRange)
        return avgInRange

    def getCorrectedData(self, x, y):
        logger.debug(METHOD_ENTER_STR % ((x,y),))
        preEdgeRange = self.rangeSelectionInfo.getPreEdgeRange()
        logger.debug("preEdge: %s" % preEdgeRange)
        postEdgeRange = self.rangeSelectionInfo.getPostEdgeRange()
        logger.debug("postEdge: %s" % postEdgeRange)
        preEdgeAvg = self.getAverageFromRange(x, y,  preEdgeRange)
        postEdgeAvg = self.getAverageFromRange(x, y, postEdgeRange)
        return self.subChoices.calcCorrectedData(y, \
                                                 preEdge=preEdgeAvg, \
                                                 postEdge=postEdgeAvg)
        
    def getPlotAxisLabels(self):
        return self.subChoices.choiceWidget.getPlotAxisLabels()
        
#     def getDataLabels(self):
#         return self.subChoices.choiceWidget.getDataLabels()

    def getPlotAxisLabelsIndex(self):
        return self.subChoices.choiceWidget.getPlotAxisLabelsIndex()

    def getPostEdgeRange(self):
        return self.rangeSelectionInfo.getPostEdgeRange()
        
    def getPreEdgeRange(self):
        return self.rangeSelectionInfo.getPreEdgeRange()
        
    def getScanTypes(self, specFile):
        scanTypes = set()
        for scan in specFile.scans:
            scanTypes.add(specFile.scans[scan].scanCmd.split()[0])
        scanTypes = list(scanTypes)
        scanTypes.sort()
        return scanTypes
        
    def getSelectedCounterInfo(self):
        counters = self.counterSelector.getSelectedCounters()
        counterNames = self.counterSelector.getSelectedCounterNames(counters)
        return counters, counterNames
 
    def getSelectedEdgeRangeData(self):
        return (self.rangeSelectionInfo.getPreEdgeRange(),
                self.rangeSelectionInfo.getPostEdgeRange())
        
    def getSelectedScans(self):
        return self.selectedScans
    

    def getSelectedScansRange(self):
        scans = self.selectedScans
        minScan = None
        maxScan = None
        
        counters, counterNames = self.getSelectedCounterInfo()
        for scan in scans:
            node = self.getNodeContainingScan(scan)
            thisScan = node.scans[scan]
            axisCounter = counterNames[0]
            try:
                dataThisScan = thisScan.data[axisCounter][:]
                if dataThisScan is not None and len(dataThisScan) > 1:
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
            except KeyError:
                logger.exception("Tried to load data that does "  +\
                                 "not have counters selected.")
                
        if minScan is None:
            minScan = 999999.
        if maxScan is None:
            maxScan = -999999.9
        return [minScan, maxScan]
        
    '''
    Triggered when a user selects a new option for which counter to use in a 
    particular roll in calculations/plotting
    '''
    @qtCore.pyqtSlot(list)
    def handleCounterDataChanged(self, data):
        logger.debug (" %s" % data)
        counters = self.counterSelector.getSelectedCounters()
        names = self.counterSelector.getSelectedCounterNames(counters)
        currentScan = self.scanBrowser.getCurrentScan()
        currentType = self._selectedNodes[0].getSpecDataFile(). \
            scans[str(currentScan)].scanCmd.split()[0]
        
        self.storePlotSelections(currentType)
        
        self.subChoices.choiceWidget.setPlotSelections(names)
        self.currentSelections[currentType] = names
        self.dataSelectionsChanged.emit()

    '''
    Triggered when a new set of options are loaded typically by selecting a
    new scan type
    '''
    @qtCore.pyqtSlot(str, int, bool)
    def handleCounterOptChanged(self, counterName, optIndex, value):
        logger.debug(METHOD_ENTER_STR)
        typeNames = self.typeSelector.getTypeNames()
        specFile = self._selectedNodes[0].getSpecDataFile()
        if (optIndex == 1 and value ==True):
            energyData = specFile.getSpecDataFile(). \
                scans[self.selectedScans[0]].data['Energy']
            data = specFile.scans[self.selectedScans[0]].data[str(counterName)]
            #TODO: plot widget is external to this.   Need to raise signal to main window
            self.plotWidget.plot(energyData, data)
        
    def handleEdgeRangeChanged(self, preEdgeRange, postEdgeRange):
        logger.debug(METHOD_ENTER_STR, ((preEdgeRange, postEdgeRange),))
        self.rangeValuesChanged.emit(preEdgeRange, postEdgeRange)
        
    @qtCore.pyqtSlot()
    def handlePlotOptionChanged(self):
        logger.debug(METHOD_ENTER_STR)
        self.plotOptionChanged.emit()
        
    @qtCore.pyqtSlot(int)
    def handlePlotTypeChanged(self, newType, suppressFilter=False):
        logger.debug(METHOD_ENTER_STR)
        
    '''
    Called when a user actually selects a new scan from the list in the 
    ScanBrowser.  When a new scan is selected, it's type needs to be determined, 
    a correct Choice widget should load to the Choice Holder, the counter table 
    should be loaded with the list of choices for the selected scan and options
    presented that make sense for that type of scan.  If the type is not known,
    then the UndefinedChoice presents some basic X/Y options for plotting.
    If the scan type selector is set for all, the user should only be able to 
    select one scan.  If the user has selected a scan type then selecting 
    multiple scans should be possible.  If multiple scans are selected the 
    scan data is averaged and displayed.  If selected in the Choice field, the 
    individual scans will also be plotted.  The sum will be bolder than the 
    individual scans.
    '''
    def handleScanSelection(self, selectedScans):
        logger.debug(METHOD_ENTER_STR % selectedScans)
        self.selectedScans = selectedScans
        logger.debug("selectedScans %s", selectedScans)
        
        newScan = self.selectedScans[0]
        logger.debug("newScan %s" % newScan)
        specFile = self._selectedNodes[0].getSpecDataFile()
        newScanType = specFile.scans[str(newScan)].scanCmd.split()[0]
        firstNumPts = None
        for scan in selectedScans:
            numPtsInScan = len(specFile.scans[scan].data_lines)
            if firstNumPts is None:
                firstNumPts = numPtsInScan
            else:
                if numPtsInScan != firstNumPts:
                    qtWidgets.QMessageBox.warning(self, "Num pts dont match", 
                                  "All selected scans must have the same " +
                                  "number of points in the scan")
                    return
                    
        
        logger.debug("newScanType %s" % newScanType)
        
        self.subChoices.setChoiceWidgetByScanType(newScanType)
        self.subChoices.setDefaultSelectionsFromCounterNames(
            specFile.scans[str(newScan)].L)
        self.counterSelector.counterModel. \
            initializeDataRows(self.subChoices.choiceWidget.COUNTER_OPTS,
                               specFile.scans[str(newScan)].L)
        self.counterSelector.counterModel \
            .setCounterOptions(self.subChoices.choiceWidget.COUNTER_OPTS)

        typeIndex = self.typeSelector.getTypeIndexFromName(newScanType)
        logger.debug("currentselection %s" % self.currentSelections.keys())
        self.counterSelector.counterModel \
            .setCounterOptions(self.subChoices.choiceWidget.COUNTER_OPTS)
        #TODO: may need to move out
        self.storePlotSelections(newScanType)
        
        self.counterSelector.setSelectedCounters(
            self.currentSelections[newScanType])
        self.dataSelectionsChanged.emit()
        self.validateRangeSelection()
        
        
    '''
    Handle a sequence of operations when the contents of the scan browser 
    changes.  This can happen when a new scan is loaded or when the user 
    selects a scan type in the scan browser.
    ''' 
    @qtCore.pyqtSlot(bool)
    def handleScanLoaded(self, newFile):
        logger.debug(METHOD_ENTER_STR)
        scanTypes = self.getScanTypes(self._selectedNodes[0].getSpecDataFile())
        logger.debug("scanTypes: %s" % scanTypes)
        if newFile:
            self.typeSelector.loadScans(scanTypes)
        self.scanBrowser.setCurrentScan(0)
        self.counterSelector.setCurrentCounter(0)
        self.dataSelectionsChanged.emit()
        
    @qtCore.pyqtSlot(int)
    def handleSubTypeChanged(self, newType):
        logger.debug(METHOD_ENTER_STR % newType)

    def hasRangeSelectionWidget(self):
        return True
    
    def hasValidRangeSelectionData(self):
        return self.rangeSelectionInfo.hasValidRangeSelectionData()

    def isDataIncreasingX(self, dataSet):
        logger.debug(METHOD_ENTER_STR % dataSet)
        retValue = False
        if dataSet[0] <= dataSet[-1]:
            retValue = True
        logger.debug(METHOD_EXIT_STR % retValue)
        return retValue
        
    def isMultipleScansSelected(self):
        logger.debug(METHOD_ENTER_STR % self.selectedNodes)
        if len(self.selectedScans) > 1:
            return True
        else:
            return False

    def setupDisplayWithSelectedNodes(self):
        logger.debug(METHOD_ENTER_STR)
        if len(self._selectedNodes) == 1:
            logger.debug(type(self._selectedNodes[0]))
            specFile = self._selectedNodes[0].getSpecDataFile()
            self.scanBrowser.setPositionersToDisplay(self.scanBrowser.positionersToDisplay)
            self.scanBrowser.loadScans(specFile.scans, newFile=True)
            self.typeSelector.loadScans(self.getScanTypes(specFile))
            
    def plotIndividualData(self):
        return self.subChoices.plotIndividualData()
        
    def plotAverageData(self):
        return self.subChoices.plotAverageData()
   
    def plotCorrectedData(self):
        logger.debug(METHOD_ENTER_STR)
        preEdgeRange = self.rangeSelectionInfo.getPreEdgeRange()
        postEdgeRange = self.rangeSelectionInfo.getPostEdgeRange()
        decision = (self.selectedScansOverlapRange(preEdgeRange)) and \
            (self.selectedScansOverlapRange(postEdgeRange)) and \
            self.subChoices.plotCorrectedData()
        logger.debug(METHOD_EXIT_STR % decision)
        return decision 
        
    def plotNormalizedData(self):
        return False

    @qtCore.pyqtSlot(int)
    def scanTypeSelected(self, newType, suppressFilter=False):
        '''
        Called when the user selects a scan type from the ScanTypeSelector
        This should should modify the list shown in the ScanBrowser so that 
        only that type of scan is shown in the browser.  This user should be 
        able to change between specific types or all types.  This should also
        switch the browser in/out of multi selection mode.
        '''
        names = self.typeSelector.getTypeNames()
        logger.debug(METHOD_ENTER_STR % names[newType])
        specFile = self._selectedNodes[0].getSpecDataFile()
        logger.debug ("filter for type %d from scan types %s" % \
                      (newType, str(names)))
        if names[newType] == SCAN_TYPES[0]:  # all types
            types = names[1:]
            self.scanBrowser.scanList. \
                setSelectionMode(qtWidgets.QAbstractItemView.SingleSelection)
        else:
            types = (names[newType],)
            self.scanBrowser.scanList. \
                setSelectionMode(qtWidgets.QAbstractItemView.ExtendedSelection)
        logger.debug ("filter for type %d from scan types %s" % \
                      (newType, str(types)))
        if not suppressFilter:
            self.scanBrowser.filterByScanTypes(specFile.scans, types)
        currentScan = self.scanBrowser.getCurrentScan()
        logger.debug("current scan %s" %currentScan)
        self.scanBrowser.scanList.setCurrentCell(0, 0)
        self.scanBrowser.scanList.selectRow(0)
        #force this since we have changed the underlying data
        if names[newType] == 'XMCDvsE':
            self.counterSelector.setVisible(False)
        else:
            self.counterSelector.setVisible(True)
        self.scanBrowser.scanList.itemSelectionChanged.emit()
        self.dataSelectionsChanged.emit()            
        
    def selectedScansOverlapRange(self, range):
        logger.debug(METHOD_ENTER_STR % range)
        scansOverlap = False
        scans = self.selectedScans
        counters, counterNames = self.getSelectedCounterInfo()
        for scan in scans:
            node = self.getNodeContainingScan(scan)
            thisScan = node.scans[scan]
            axisCounter = counterNames[0]
            try:
                dataThisScan = thisScan.data[axisCounter][:]
                logger.debug("dataThisScan %s" % dataThisScan)
                if dataThisScan is not None and len(dataThisScan) > 1:
                    if self.isDataIncreasingX(dataThisScan):
                        logger.debug("Evaluate for increasing X %s, %s, %s" \
                                     % (range, dataThisScan[0], \
                                      dataThisScan[-1]))
                        if ((range[0] >= dataThisScan[0]) and \
                            (range[0] <= dataThisScan[-1])) \
                            or \
                            ((range[1] >= dataThisScan[0]) and \
                              (range[1] <= dataThisScan[-1])):
                            scansOverlap = True
                    else:
                        logger.debug("Evalueate for Decreasing X %s, %s, %s" \
                                     % (range, dataThisScan[0], \
                                      dataThisScan[-1]))
                        if ((range[0] >= dataThisScan[-1]) and \
                            (range[0] <= dataThisScan[0])) \
                            or \
                            ((range[1] >= dataThisScan[-1]) and \
                              (range[1] <= dataThisScan[0])):
                            scansOverlap = True
                        
            except KeyError:
                logger.exception("Tried to load data that does "  +\
                                 "not have counters selected.")
        logger.debug("scansOverlap %s" % scansOverlap)
        return scansOverlap
        
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
        logger.debug(METHOD_ENTER_STR, positioners)
        self.scanBrowser.setPositionersToDisplay(positioners)
        
    def setUserParamsToDisplay(self, userParams):
        logger.debug(METHOD_ENTER_STR, userParams)
        self.scanBrowser.setUserParamsToDisplay(userParams)
        
    def setTemperatureParamsToDisplay(self, temperatureParams):
        logger.debug(METHOD_ENTER_STR, temperatureParams)
        self.scanBrowser.setTemperatureParamsToDisplay(temperatureParams)
        
    def storePlotSelections(self, typeName):
        if not (typeName in self.currentSelections.keys()):
            logger.debug("dealing with new scan type %s" %typeName)
            logger.debug("subChoices.choiceWidget %s" % 
                         self.subChoices.choiceWidget)
            self.currentSelections[typeName] = \
                self.subChoices.getPlotSelections()
        logger.debug("currentSelections %s" % self.currentSelections[typeName]) 
        
    def updateEdgeRanges(self):
        logger.debug(METHOD_ENTER_STR)
        if (self.rangeSelectionInfo.edgeRangesAtDummyValues()):
            logging.debug("Current edges at dummy values")
            self.setDefSelectedScansRange()
        else:
            currentPreEdgeRange, currentPostEdgeRange = \
                self.getSelectedEdgeRangeData()
            currentSelectedScanRange = self.getSelectedScansRange()
            if (currentPreEdgeRange[0] < currentSelectedScanRange[0]) or \
                (currentPostEdgeRange[1] > currentSelectedScanRange[1]):
                logging.debug("Current edge values %s outside range of current selection %s" % \
                              ((currentPreEdgeRange, currentPostEdgeRange), currentSelectedScanRange))
                self.setDefSelectedScansRange()
 