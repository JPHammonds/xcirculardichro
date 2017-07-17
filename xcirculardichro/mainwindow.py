'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import os
import PyQt4.QtGui as qtGui
import PyQt4.QtCore as qtCore

from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import pyqtSlot as Slot

from PyQt4.QtGui import QAbstractItemView

import sys
import logging
import logging.config
from xcirculardichro.config.loggingConfig import LOGGER_NAME, LOGGER_DEFAULT,\
    METHOD_ENTER_STR, METHOD_EXIT_STR
from ConfigParser import NoSectionError
from spec2nexus.spec import SpecDataFile
#import specguiutils
#from xcirculardichro.gui.datatype import DataType
from specguiutils.scanbrowser import ScanBrowser
from specguiutils.counterselector import CounterSelector
from specguiutils.scantypeselector import ScanTypeSelector, SCAN_TYPES
from xcirculardichro.gui.plotwidget import PlotWidget
from xcirculardichro.gui.choices.choiceholder import ChoiceHolder
from xcirculardichro.gui.datanavigator import DataNavigator
from specguiutils.view.specdatafileitem import SpecDataFileItem


#configure message logging
userDir = os.path.expanduser('~')
logConfigFile = os.path.join(userDir, LOGGER_NAME + 'Log.config')
try:
    logging.config.fileConfig(logConfigFile)
except NoSectionError:
    logging.config.dictConfig(LOGGER_DEFAULT)
logger = logging.getLogger(LOGGER_NAME)
APP_NAME = "XCircularDichro"

class MainWindow(qtGui.QMainWindow):
    '''
    Create a main dialog for the application
    '''

    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        logger.debug(METHOD_ENTER_STR)
        self._createMenuBar()
        mainWidget = qtGui.QWidget()
        layout = qtGui.QHBoxLayout()
        self.currentSelections = {}
        self.splitter = qtGui.QSplitter()
        specWidget = qtGui.QWidget()
        specLayout = qtGui.QVBoxLayout()
        self.dataNavigator = DataNavigator()
        self.typeSelector = ScanTypeSelector()
        self.scanBrowser = ScanBrowser()
        self.scanBrowser.scanList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.subChoices = ChoiceHolder()
        self.typeSelector.setCurrentType(0)
        self.counterSelector = CounterSelector(
            counterOpts=self.subChoices.choiceWidget.COUNTER_OPTS)
        specLayout.addWidget(self.typeSelector)
        specLayout.addWidget(self.scanBrowser)
        specLayout.addWidget(self.subChoices)
        specLayout.addWidget(self.counterSelector)
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
        self.dataNavigator.specDataSelectionChanged[SpecDataFileItem].connect( \
            self.handleSpecDataSelectionChanged)
        specWidget.setLayout(specLayout)
        self.splitter.addWidget(self.dataNavigator)
        self.splitter.addWidget(specWidget)
        self.plotWidget = PlotWidget()
        self.splitter.addWidget(self.plotWidget)
        layout.addWidget(self.splitter)
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)
        self.setGeometry(300,300, 1000, 600)
        self.setWindowTitle('XCircularDichro')
        self.show()
        logger.debug(METHOD_EXIT_STR)
        
    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu('File')
        dataMenu = menuBar.addMenu('Data')
        
        openAction = qtGui.QAction("Open", self)
        openAction.triggered.connect(self.openFile)
        
        saveAction = qtGui.QAction("Save", self)
        saveAction.triggered.connect(self.saveFile)

        saveAsAction = qtGui.QAction("Save As", self)
        saveAsAction.triggered.connect(self.saveAsFile)
        
        exportAction = qtGui.QAction("Export", self)
        exportAction.triggered.connect(self.export)
        
        closeAction = qtGui.QAction("Close", self)
        closeAction.triggered.connect(self.closeFile)

        
        exitAction = qtGui.QAction("Exit", self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(closeAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exportAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
    
    def closeFile(self):
        logger.debug(METHOD_ENTER_STR)
        index = self.dataNavigator.dataNavigatorView.currentIndex()
        logger.debug("Index %s " % index) 
        self.dataNavigator.dataNavigatorModel.removeRows(index.row(), 1)
        #self.dataNavigator.dataNavigatorView.setCurrentSelection()
    def export(self):
        logger.debug(METHOD_ENTER_STR)    

    def getScanTypes(self, specFile):
        scanTypes = set()
        for scan in specFile.scans:
            scanTypes.add(specFile.scans[scan].scanCmd.split()[0])
        return list(scanTypes)
        
    
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
        currentType = self.specFile.scans[str(currentScan)].scanCmd.split()[0]
        
        self.storePlotSelections(currentType)
        
        self.subChoices.choiceWidget.setPlotSelections(names)
        self.currentSelections[currentType] = names
        self.updatePlotData()
        
    '''
    Triggered when a new set of options are loaded typically by selecting a
    new scan type
    '''
    @qtCore.pyqtSlot(str, int, bool)
    def handleCounterOptChanged(self, counterName, optIndex, value):
        typeNames = self.typeSelector.getTypeNames()
#         logger.debug ("handling a counter option changing for counter %s %s %s " % \
#                 (counterName, LOCK_IN_COUNTER_OPTS[optIndex], value))
        
        if (optIndex == 1 and value ==True):
            energyData = self.specFile.scans[self.selectedScans[0]].data['Energy']
            data = self.specFile.scans[self.selectedScans[0]].data[str(counterName)]
            #logger.debug ("data %s" % data)
            self.plotWidget.plot(energyData, data)
        
    @qtCore.pyqtSlot()
    def handlePlotOptionChanged(self):
        logger.debug("METHOD_ENTER_STR")
        self.updatePlotData()

    '''
    Update the scan plots when the plot type has changed in the Choice Holder/
    ChoiceWidget
    '''
    @qtCore.pyqtSlot(int)
    def handlePlotTypeChanged(self, newType):
        logger.debug("newType %s" % newType)
        self.updatePlotData()
        
    '''
    Handle a sequence of operations when the contents of the scan browser 
    changes.  This can happen when a new scan is loaded or when the user 
    selects a scan type in the scan browser.
    ''' 
    @qtCore.pyqtSlot(bool)
    def handleScanLoaded(self, newFile):
        scanTypes = self.getScanTypes(self.specFile)
        logger.debug("scanTypes: %s" % scanTypes)
        if newFile:
            self.typeSelector.loadScans(scanTypes)
        self.scanBrowser.setCurrentScan(0)
        self.counterSelector.setCurrentCounter(0)
        
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
#    @qtCore.pyqtSlot(str)
    def handleScanSelection(self, selectedScans):
        logger.debug ("handling selection of scans %s" %selectedScans)
        self.selectedScans = selectedScans
        newScan = self.selectedScans[0]
        logger.debug("newScan %s" % newScan)
        newScanType = self.specFile.scans[str(newScan)].scanCmd.split()[0]
        logger.debug("newScanType %s" % newScanType)
        
        self.subChoices.setChoiceWidgetByScanType(newScanType)
        self.counterSelector.counterModel \
            .setCounterOptions(self.subChoices.choiceWidget.COUNTER_OPTS)

        self.counterSelector.counterModel. \
            initializeDataRows(self.specFile.scans[str(newScan)].L)
        typeIndex = self.typeSelector.getTypeIndexFromName(newScanType)
        logger.debug("currentselection %s" % self.currentSelections.keys())
        self.counterSelector.counterModel \
            .setCounterOptions(self.subChoices.choiceWidget.COUNTER_OPTS)
        
        self.storePlotSelections(newScanType)
        
        self.counterSelector.setSelectedCounters(
            self.currentSelections[newScanType])
        self.updatePlotData()

    
    @qtCore.pyqtSlot(SpecDataFileItem)
    def handleSpecDataSelectionChanged(self, dataItem):
        selectedSpecFile = dataItem.getSpecDataFile()
        self.specFile = selectedSpecFile
        logger.debug("Selected File Name %s" % selectedSpecFile.fileName)
        self.setWindowTitle(APP_NAME + " - " + selectedSpecFile.fileName)
        self.scanBrowser.loadScans(selectedSpecFile.scans, newFile=True)
        self.typeSelector.loadScans(self.getScanTypes(selectedSpecFile))

    @qtCore.pyqtSlot(int)
    def handleSubTypeChanged(self, newType):
        logger.debug("newType %s" % newType)
        
    def saveFile(self):
        logger.debug(METHOD_ENTER_STR)
        
    def saveAsFile(self):
        logger.debug(METHOD_ENTER_STR)
        
    def openFile(self):
        logger.debug(METHOD_ENTER_STR)
        fileName = qtGui.QFileDialog.getOpenFileName(None, "Open Spec File")
        if fileName != "":
            self.specFile = SpecDataFile(fileName)
            self.setWindowTitle(APP_NAME + " - " + str(fileName))
            self.scanBrowser.loadScans(self.specFile.scans, newFile=True)
            self.typeSelector.loadScans(self.getScanTypes(self.specFile))
            dataItem = SpecDataFileItem(self.specFile.fileName, self.specFile)
            self.dataNavigator.dataNavigatorModel.appendRow(dataItem)
            
        logger.debug(METHOD_EXIT_STR)
        
    '''
    Called when the user selects a scan type from the ScanTypeSelector
    This should should modify the list shown in the ScanBrowser so that 
    only that type of scan is shown in the browser.  This user should be 
    able to change between specific types or all types.  This should also
    switch the browser in/out of multi selection mode.
    '''
    @qtCore.pyqtSlot(int)
    def scanTypeSelected(self, newType, suppressFilter=False):
        names = self.typeSelector.getTypeNames()
        logger.debug ("filter for type %d from scan types %s" % \
                      (newType, str(names)))
        if names[newType] == SCAN_TYPES[0]:  # all types
            types = names[1:]
            self.scanBrowser.scanList. \
                setSelectionMode(qtGui.QAbstractItemView.SingleSelection)
        else:
            types = (names[newType],)
            self.scanBrowser.scanList. \
                setSelectionMode(qtGui.QAbstractItemView.ExtendedSelection)
        logger.debug ("filter for type %d from scan types %s" % \
                      (newType, str(types)))
        if not suppressFilter:
            self.scanBrowser.filterByScanTypes(self.specFile.scans, types)
        currentScan = self.scanBrowser.getCurrentScan()
        logger.debug("current scan %s" %currentScan)
        self.scanBrowser.scanList.setCurrentCell(0, 0)            

    def storePlotSelections(self, typeName):
        if not (typeName in self.currentSelections.keys()):
            logger.debug("dealing with new scan type %s" %typeName)
            logger.debug("subChoices.choiceWidget %s" % 
                         self.subChoices.choiceWidget)
            self.currentSelections[typeName] = \
                self.subChoices.getPlotSelections()
        logger.debug("currentSelections %s" % self.currentSelections[typeName]) 
        
        
    '''
    Performs all updates to the plots given real data.
    '''
    def updatePlotData(self):
        counters = self.counterSelector.getSelectedCounters()
        counterNames = self.counterSelector.getSelectedCounterNames(counters)
        logger.debug("Data selected for this plot %s" % counters)
        if len(self.selectedScans) == 1:
            self.updatePlotDataSingle(counters, counterNames)
        elif len(self.selectedScans) > 1:
            self.updatePlotDataMultiple(counters, counterNames)
            
    '''
    Handle updating the plot window when multiple scans are selected
    '''
    def updatePlotDataMultiple(self, counters, counterNames, 
                               displayAverage=True, displayEach=True):
        logger.debug("Enter")
        data = {}
        dataOut = {}
        self.plotWidget.clear()
        
        dataSum = []
        dataAverage = []
        for scan in self.selectedScans:
            data[scan] = []
            dataOut[scan] = []
            thisScan = self.specFile.scans[scan]
            for counter in counterNames:
                try:
                    
                    data[scan].append(thisScan.data[counter])
                except KeyError as ie:
                    logger.exception("Tried to load data which does" +
                                     " not have counters selected."  +
                                     "Multiple scans are selected and some" +
                                     "may not have the selected counters " +
                                     "Scan %s \n %s" % (str(scan), str(ie)))
            try:
                dataOut[scan] = self.subChoices.choiceWidget.calcPlotData(data[scan])
                 
            except IndexError:
                qtGui.QMessageBox.warning(self, "No Data Warning", 
                                          "No Data Was Selected")
            countIndex = range(1, len(dataOut[scan]))   #start at 1 since 0 is x axis
            plotAxisLabels = self.subChoices.choiceWidget.getPlotAxisLabels()
            plotDataLabel = self.subChoices.choiceWidget.getDataLabels()
            axisLabelIndex = self.subChoices.choiceWidget.getPlotAxisLabelsIndex()
            if self.subChoices.choiceWidget.plotIndividualData():
                for index in countIndex:
                    dataLabel = "%s - Scan %s" % (plotDataLabel[index], scan) 
                    if axisLabelIndex[index] == 1:
                        self.plotWidget.plotAx1(dataOut[scan][0], dataOut[scan][index], dataLabel)
                        self.plotWidget.setXLabel(plotAxisLabels[0])
                        self.plotWidget.setYLabel(plotAxisLabels[index])
                    elif axisLabelIndex[index] == 2:
                        self.plotWidget.plotAx2(dataOut[scan][0], dataOut[scan][index], dataLabel)
                        self.plotWidget.setXLabel(plotAxisLabels[0])
                        self.plotWidget.setY2Label(plotAxisLabels[index])
                        
            if scan == self.selectedScans[0]:
                dataSum = dataOut[scan] 
            else:
                for index in countIndex:
                    logger.debug("dataSum[index].shape %s" % dataSum[index].shape)
                    logger.debug("dataOut[scan][index].shape %s" % dataOut[scan][index].shape)
                    dataSum[index] += dataOut[scan][index]
        if self.subChoices.choiceWidget.plotAverageData():
            for index in countIndex:
                dataAverage = dataSum[index]/len(self.selectedScans)
                plotDataLabel = self.subChoices.choiceWidget.getDataLabels()
                dataLabel = "%s - Avg" % plotDataLabel[index] 
                if axisLabelIndex[index] == 1:
                    self.plotWidget.plotAx1Average(dataOut[scan][0], dataAverage, dataLabel)
                if axisLabelIndex[index] == 2:
                    self.plotWidget.plotAx2Average(dataOut[scan][0], dataAverage, dataLabel)
        self.plotWidget.plotDraw()                            
    '''
    Handle updating the plot window when only one scan is selected
    '''        
    def updatePlotDataSingle(self, counters, counterNames):
        logger.debug("Enter")
        data = []
        dataOut = []
        scans = self.specFile.scans[self.selectedScans[0]]
        
        for counter in counterNames:
            try:
                data.append(scans.data[counter])
            except KeyError as ie:
                logger.exception("Tried to load data which does not have " +
                                 "counters selected. Please make a selection " +
                                 "for this type of data: Scan --%s--\n%s" % 
                                 (str(scans), str(ie)))
        try:
            dataOut = self.subChoices.choiceWidget.calcPlotData(data)
        except IndexError:
            qtGui.QMessageBox.warning(self, "No Data Warning", "NoData was selected")
        countIndex = range(1, len(dataOut))
        self.plotWidget.clear()
        plotAxisLabels = self.subChoices.choiceWidget.getPlotAxisLabels()
        plotDataLabel = self.subChoices.choiceWidget.getDataLabels()
        axisLabelIndex = self.subChoices.choiceWidget.getPlotAxisLabelsIndex()
        logger.debug("plotAxesLabels %s", plotAxisLabels)
        for index in countIndex:
            logger.debug("index, counters %s %s" % (index, counters))
            logger.debug("index, len(counters)-1 %s, %s" % (index, len(counters)-1 ))
            if axisLabelIndex[index] == 1:
                self.plotWidget.plotAx1(dataOut[0], dataOut[index], plotDataLabel[index])
                logger.debug("plotAxisLabels: %s" % plotAxisLabels)
                self.plotWidget.setXLabel(plotAxisLabels[0])
                self.plotWidget.setYLabel(plotAxisLabels[index])
            if axisLabelIndex[index] == 2:
                self.plotWidget.plotAx2(dataOut[0], dataOut[index], plotDataLabel[index])
                logger.debug("plotAxisLabels: %s" % plotAxisLabels)
                self.plotWidget.setXLabel(plotAxisLabels[0])
                self.plotWidget.setY2Label(plotAxisLabels[index])
        
        self.plotWidget.plotDraw()
        
if __name__ == '__main__':
    app = qtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
