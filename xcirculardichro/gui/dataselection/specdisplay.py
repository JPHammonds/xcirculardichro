'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging

import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
from specguiutils.scantypeselector import ScanTypeSelector, SCAN_TYPES
from specguiutils.scanbrowser import ScanBrowser
from specguiutils.counterselector import CounterSelector
from xcirculardichro.gui.choices.choiceholder import ChoiceHolder
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR
from xcirculardichro.gui.dataselection.AbstractSelectionDisplay import AbstractSelectionDisplay
from PyQt5.QtWidgets import QAbstractItemView

logger = logging.getLogger(__name__)

class SpecDisplay(AbstractSelectionDisplay):
    
    def __init__(self, parent=None):
        super(SpecDisplay, self).__init__(parent)
        layout = qtWidgets.QVBoxLayout()
        
        self.currentSelections = {}
        self.typeSelector = ScanTypeSelector()
        self.scanBrowser = ScanBrowser()
        self.subChoices = ChoiceHolder()
        self.typeSelector.setCurrentType(0)
        self.counterSelector = CounterSelector(
            counterOpts = self.subChoices.choiceWidget.COUNTER_OPTS)
        self.scanBrowser.scanList.setSelectionMode(QAbstractItemView.SingleSelection)
        
        layout.addWidget(self.typeSelector)
        layout.addWidget(self.scanBrowser)
        layout.addWidget(self.subChoices)
        layout.addWidget(self.counterSelector)
        
        self.setLayout(layout)
        
        self.scanBrowser.scanSelected[list].connect(self.handleScanSelection)
        self.scanBrowser.scanLoaded[bool].connect(self.handleScanLoaded)
        self.counterSelector.counterOptChanged[str, int, bool] \
            .connect(self.handleCounterOptChanged)
        self.counterSelector.counterView.counterDataChanged[list] \
            .connect(self.handleCounterDataChanged)
        self.typeSelector.scanTypeChanged[int].connect(self.scanTypeSelected)
        self.subChoices.subTypeChanged[int].connect(self.handleSubTypeChanged)
        self.subChoices.plotTypeChanged[int].connect(self.handlePlotTypeChanged)
        
        self.show()
        
    
    def calcPlotData(self, data):
        return self.subChoices.choiceWidget.calcPlotData(data)
        
    def getPlotAxisLabels(self):
        return self.subChoices.choiceWidget.getPlotAxisLabels()
        
    def getDataLabels(self):
        return self.subChoices.choiceWidget.getDataLabels()

    def getPlotAxisLabelsIndex(self):
        return self.subChoices.choiceWidget.getPlotAxisLabelsIndex()

    def getScanTypes(self, specFile):
        scanTypes = set()
        for scan in specFile.scans:
            scanTypes.add(specFile.scans[scan].scanCmd.split()[0])
        return list(scanTypes)
        
    def getSelectedScans(self):
        return self.selectedScans
    
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
        currentType = self._selectedNodes[0].getSpecDataFile().scans[str(currentScan)].scanCmd.split()[0]
        
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
            energyData = specFile.getSpecDataFile().scans[self.selectedScans[0]].data['Energy']
            data = specFile.scans[self.selectedScans[0]].data[str(counterName)]
            #TODO: plot widget is external to this.   Need to raise signal to main window
            self.plotWidget.plot(energyData, data)
        
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

    def isMultipleScansSelected(self):
        if len(self.selectedScans) == 1:
            return False
        elif len(self.selectedScans) > 1:
            return True

    def setupDisplayWithSelectedNodes(self):
        logger.debug(METHOD_ENTER_STR)
        if len(self._selectedNodes) == 1:
            logger.debug(type(self._selectedNodes[0]))
            specFile = self._selectedNodes[0].getSpecDataFile()
            self.scanBrowser.loadScans(specFile.scans, newFile=True)
            self.typeSelector.loadScans(self.getScanTypes(specFile))
            
        
    def plotIndividualData(self):
        return self.subChoices.choiceWidget.plotIndividualData()
        
    def plotAverageData(self):
        return self.subChoices.choiceWidget.plotAverageData()
            
    '''
    Called when the user selects a scan type from the ScanTypeSelector
    This should should modify the list shown in the ScanBrowser so that 
    only that type of scan is shown in the browser.  This user should be 
    able to change between specific types or all types.  This should also
    switch the browser in/out of multi selection mode.
    '''
    @qtCore.pyqtSlot(int)
    def scanTypeSelected(self, newType, suppressFilter=False):
        logger.debug(METHOD_ENTER_STR)
        names = self.typeSelector.getTypeNames()
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
        self.scanBrowser.scanList.itemSelectionChanged.emit()
        self.dataSelectionsChanged.emit()            
        
    def storePlotSelections(self, typeName):
        if not (typeName in self.currentSelections.keys()):
            logger.debug("dealing with new scan type %s" %typeName)
            logger.debug("subChoices.choiceWidget %s" % 
                         self.subChoices.choiceWidget)
            self.currentSelections[typeName] = \
                self.subChoices.getPlotSelections()
        logger.debug("currentSelections %s" % self.currentSelections[typeName]) 
        
