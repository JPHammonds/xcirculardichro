'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import os
import PyQt4.QtGui as qtGui
import PyQt4.QtCore as qtCore

from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtCore import pyqtSlot as Slot


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


#configure message logging
userDir = os.path.expanduser('~')
logConfigFile = os.path.join(userDir, LOGGER_NAME + 'Log.config')
try:
    logging.config.fileConfig(logConfigFile)
except NoSectionError:
    logging.config.dictConfig(LOGGER_DEFAULT)
logger = logging.getLogger(LOGGER_NAME)
APP_NAME = "XCircularDichro"
# DEF_COUNTER_OPTS = ["X", "Y", "Mon"]
# NON_LOCK_IN_COUNTER_OPTS = ["Energy", "D+", "D-", "M+", "M-"]
# LOCK_IN_COUNTER_OPTS = ["Energy","XAS", "XMCD"]
#SELECTION_TYPES = ['None', 'lockin', 'Flourecence', 'Transmission']
#SCAN_TYPES_FOR_SELECTION = [(), ('qxscan',), ('qxdichro',), ('qxdichro',)]
# QXDICHRO = 'qxdichro'
# QXSCAN = 'qxscan'
# COUNTER_OPTS_FOR_SELECTION= [DEF_COUNTER_OPTS, \
#                              LOCK_IN_COUNTER_OPTS, \
#                              NON_LOCK_IN_COUNTER_OPTS, \
#                              NON_LOCK_IN_COUNTER_OPTS]

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
        self.typeSelector = ScanTypeSelector()
        self.scanBrowser = ScanBrowser()
        self.subChoices = ChoiceHolder()
        self.typeSelector.setCurrentType(0)
        self.counterSelector = \
            CounterSelector(counterOpts=self.subChoices.choiceWidget.COUNTER_OPTS)
        specLayout.addWidget(self.typeSelector)
        specLayout.addWidget(self.scanBrowser)
        specLayout.addWidget(self.subChoices)
        specLayout.addWidget(self.counterSelector)
        self.scanBrowser.scanSelected[str].connect(self.handleScanSelection)
        self.scanBrowser.scanLoaded[bool].connect(self.handleScanLoaded)
        self.counterSelector.counterOptChanged[str, int, bool] \
            .connect(self.handleCounterOptChanged)
        self.counterSelector.counterView.counterDataChanged[list] \
            .connect(self.handleCounterDataChanged)
        self.typeSelector.scanTypeChanged[int].connect(self.scanTypeSelected)
        self.subChoices.subTypeChanged[int].connect(self.handleSubTypeChanged)
        self.subChoices.plotTypeChanged[int].connect(self.handlePlotTypeChanged)
        specWidget.setLayout(specLayout)
        #layout.addLayout(specLayout)
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
        
        openAction = qtGui.QAction("Open", self)
        openAction.triggered.connect(self.openFile)

        exitAction = qtGui.QAction("Exit", self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        
    def getScanTypes(self):
        scanTypes = set()
        for scan in self.specFile.scans:
            scanTypes.add(self.specFile.scans[scan].scanCmd.split()[0])
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
            energyData = self.specFile.scans[self.selectedScans].data['Energy']
            data = self.specFile.scans[self.selectedScans].data[str(counterName)]
            #logger.debug ("data %s" % data)
            self.plotWidget.plot(energyData, data)
        
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
        scanTypes = self.getScanTypes()
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
    @qtCore.pyqtSlot(str)
    def handleScanSelection(self, newScan):
        logger.debug ("handling selection of scan %s" %newScan)
        self.selectedScans = str(newScan)
        newScanType = self.specFile.scans[str(newScan)].scanCmd.split()[0]

        self.subChoices.setChoiceWidgetByScanType(newScanType)
        self.counterSelector.counterModel \
            .setCounterOptions(self.subChoices.choiceWidget.COUNTER_OPTS)

        self.counterSelector.counterModel.initializeDataRows(self.specFile.scans[str(newScan)].L)
        typeIndex = self.typeSelector.getTypeIndexFromName(newScanType)
        logger.debug("currentselection %s" % self.currentSelections.keys())
        self.counterSelector.counterModel \
            .setCounterOptions(self.subChoices.choiceWidget.COUNTER_OPTS)
        
        self.storePlotSelections(newScanType)
        
        self.counterSelector.setSelectedCounters(self.currentSelections[newScanType])
#        self.scanTypeSelected(typeIndex, suppressFilter=True)
        self.updatePlotData()

    
        
    @qtCore.pyqtSlot(int)
    def handleSubTypeChanged(self, newType):
        
        logger.debug("newType %s" % newType)
        
    def openFile(self):
        logger.debug(METHOD_ENTER_STR)
        fileName = qtGui.QFileDialog.getOpenFileName(None, "Open Spec File")
        if fileName != "":
            self.specFile = SpecDataFile(fileName)
            self.setWindowTitle(APP_NAME + " - " + str(fileName))
            self.scanBrowser.loadScans(self.specFile.scans, newFile=True)
            self.typeSelector.loadScans(self.getScanTypes())
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
        logger.debug ("filter for type %d from scan types %s" % (newType, str(names)))
        if names[newType] == SCAN_TYPES[0]:  # all types
            types = names[1:]
        else:
            types = (names[newType],)
        logger.debug ("filter for type %d from scan types %s" % (newType, str(types)))
        if not suppressFilter:
            self.scanBrowser.filterByScanTypes(self.specFile.scans, types)
#        self.subChoices.setChoiceWidgetByScanType(names[newType])
        currentScan = self.scanBrowser.getCurrentScan()
        logger.debug("current scan %s" %currentScan)
        #newScanType = self.specFile.scans[str(currentScan)].scanCmd.split()[0]
#        newScanType = names[newType]
        self.scanBrowser.scanList.setCurrentCell(0, 0)            

    def storePlotSelections(self, typeName):
        if not (typeName in self.currentSelections.keys()):
            logger.debug("dealing with new scan type %s" %typeName)
            logger.debug("subChoices.choiceWidget %s" % self.subChoices.choiceWidget)
            self.currentSelections[typeName] = self.subChoices.getPlotSelections()
        logger.debug("currentSelections %s"   % self.currentSelections[typeName]) 
        
        
    '''
    Performs all updates to the plots given real data.
    '''
    def updatePlotData(self):
        counters = self.counterSelector.getSelectedCounters()
        counterNames = self.counterSelector.getSelectedCounterNames(counters)
        logger.debug("Data selected for this plot %s" % counters)
        data = []
        dataOut = []
        scans = self.specFile.scans[self.selectedScans]
        
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
        logger.debug("plotAxesLabels %s", plotAxisLabels)
        for index in countIndex:
            logger.debug("index, counters %s %s" % (index, counters))
            logger.debug("index, len(counters)-1 %s, %s" % (index, len(counters)-1 ))
            self.plotWidget.switchPlot(index, len(counters)-1)
            self.plotWidget.plot(dataOut[0], dataOut[index])
            self.plotWidget.setXlabel(plotAxisLabels[0])
            self.plotWidget.setYlabel(plotAxisLabels[index])
            
        
if __name__ == '__main__':
    app = qtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
