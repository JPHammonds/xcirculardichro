'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging

import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore

from spec2nexus.spec import SpecDataFile
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR,\
    METHOD_EXIT_STR
from xcirculardichro.gui.xmcddatanavigator import XMCDDataNavigator
from xcirculardichro.gui.plotwidget import PlotWidget
from xcirculardichro.gui.dataselection.selectionholder import SelectionHolder

logger = logging.getLogger(__name__)

APP_NAME = 'XMCD'

class XMCDMainWindow(qtWidgets.QMainWindow):
    '''
    Main Window for X-Ray Magnetic Circular Dichroism Application
    '''
    
    def __init__(self, parent=None):
        super(XMCDMainWindow, self).__init__(parent)
        logger.debug(METHOD_ENTER_STR)
        self.setAttribute(qtCore.Qt.WA_DeleteOnClose)
        self._createMenuBar()
        splitter = qtWidgets.QSplitter()
        
        self._dataNavigator = XMCDDataNavigator()
        self._dataSelections = SelectionHolder()
        self._plotWidget = PlotWidget()
        
        splitter.addWidget(self._dataNavigator)
        splitter.addWidget(self._dataSelections)
        splitter.addWidget(self._plotWidget)
        
        self.setCentralWidget(splitter)
        self.setWindowTitle(APP_NAME)
        self.show()
        
        self._dataNavigator.model().dataChanged.connect(self.handleNavigatorDataChanged)
        self._dataSelections.dataSelectionsChanged.connect(self.handleDataSelectionsChanged)
        logger.debug(METHOD_EXIT_STR)
        
    def _createMenuBar(self):
        '''
        internal method to setup the menu bar for this application
        '''
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu('File')
        dataMenu = menuBar.addMenu('Data')
        
        openAction = qtWidgets.QAction("Open", self)
        openAction.triggered.connect(self.openFile)
        
        saveAction = qtWidgets.QAction("Save", self)
        saveAction.triggered.connect(self.saveFile)

        saveAsAction = qtWidgets.QAction("Save As", self)
        saveAsAction.triggered.connect(self.saveAsFile)
        
        exportAction = qtWidgets.QAction("Export", self)
        exportAction.triggered.connect(self.export)
        
        closeAction = qtWidgets.QAction("Close", self)
        closeAction.triggered.connect(self.closeFile)

        captureCurrentAction = qtWidgets.QAction("CaptureCurrent", self)
        captureCurrentAction.triggered.connect(self.captureCurrent)
        
        exitAction = qtWidgets.QAction("Exit", self)
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

        dataMenu.addAction(captureCurrentAction)
        
    @qtCore.pyqtSlot() 
    def captureCurrent(self):
        logger.debug(METHOD_ENTER_STR)
    
    @qtCore.pyqtSlot()
    def closeFile(self):
        logger.debug(METHOD_ENTER_STR)
        
    @qtCore.pyqtSlot()
    def export(self):
        logger.debug(METHOD_ENTER_STR)

    @qtCore.pyqtSlot()
    def handleDataSelectionsChanged(self):
        logger.debug(METHOD_ENTER_STR)
        self.updatePlotData()
        
    @qtCore.pyqtSlot(qtCore.QModelIndex, qtCore.QModelIndex)
    def handleNavigatorDataChanged(self, beginIndex, endIndex):
        logger.debug("begin Index %s, endIndex %s" % (beginIndex, endIndex))
        checkedNodes = self._dataNavigator.model().getTopDataSelectedNodes()
        self._dataSelections.setSelectedNodes(checkedNodes)
                
        
    @qtCore.pyqtSlot()
    def openFile(self):
        '''
        Open a file, populate the navigator window as appropriate
        '''
        logger.debug(METHOD_ENTER_STR)
        fileName = qtWidgets.QFileDialog.getOpenFileName(None, "Open Spec File")[0]
        specFile = None
        if fileName != "":
            try:
                specFile = SpecDataFile(fileName)
            except NotASpecDataFile as ex:
                qtWidgets.QMessageBox.warning(self, "Not a Spec File", 
                              "The file %s does not seem to be a spec file" %
                              fileName)
                return
        else:
            return
        self._dataNavigator.addSpecDataFileNode(specFile)
        
        
    @qtCore.pyqtSlot()
    def saveFile(self):
        logger.debug(METHOD_ENTER_STR)
        
    @qtCore.pyqtSlot()
    def saveAsFile(self):
        logger.debug(METHOD_ENTER_STR)
        
    '''
    Performs all updates to the plots given real data.
    '''
    def updatePlotData(self):
        counters, counterNames = self._dataSelections.getSelectedCounterInfo()
        logger.debug("Data selected for this plot %s" % counters)
        if not self._dataSelections.isMultipleScansSelected():
            self.updatePlotDataSingle(counters, counterNames)
        else:
            self.updatePlotDataMultiple(counters, counterNames)
            
    '''
    Handle updating the plot window when multiple scans are selected
    '''
    def updatePlotDataMultiple(self, counters, counterNames, 
                               displayAverage=True, displayEach=True):
        logger.debug("Enter")
        data = {}
        dataOut = {}
        self._plotWidget.clear()
        
        dataSum = []
        dataAverage = []
        selectedScans = self._dataSelections.getSelectedScans()

        for scan in selectedScans:
            data[scan] = []
            dataOut[scan] = []
            thisScan = self._dataNavigator.model().getTopDataSelectedNodes()[0]._specDataFile.scans[scan]
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
                dataOut[scan] = self._dataSelections.calcPlotData(data[scan])
                 
            except IndexError:
                qtWidgets.QMessageBox.warning(self, "No Data Warning", 
                                          "No Data Was Selected")
            countIndex = range(1, len(dataOut[scan]))   #start at 1 since 0 is x axis
            plotAxisLabels = self._dataSelections.getPlotAxisLabels()
            plotDataLabel = self._dataSelections.getDataLabels()
            axisLabelIndex = self._dataSelections.getPlotAxisLabelsIndex()
            if self._dataSelections.plotIndividualData():
                for index in countIndex:
                    dataLabel = "%s - Scan %s" % (plotDataLabel[index], scan) 
                    if axisLabelIndex[index] == 1:
                        self._plotWidget.plotAx1(dataOut[scan][0], 
                                                dataOut[scan][index], 
                                                dataLabel)
                        self._plotWidget.setXLabel(plotAxisLabels[0])
                        self._plotWidget.setYLabel(plotAxisLabels[index])
                    elif axisLabelIndex[index] == 2:
                        self._plotWidget.plotAx2(dataOut[scan][0], 
                                                dataOut[scan][index], 
                                                dataLabel)
                        self._plotWidget.setXLabel(plotAxisLabels[0])
                        self._plotWidget.setY2Label(plotAxisLabels[index])
                        
            if scan == selectedScans[0]:
                dataSum = dataOut[scan] 
            else:
                for index in countIndex:
                    logger.debug("dataSum[%d] %s" % (index,dataSum[index]))
#                     logger.debug("dataSum[index].shape %s" % 
#                                  dataSum[index].shape)
#                     logger.debug("dataOut[scan][index].shape %s" % 
#                                  dataOut[scan][index].shape)
                    try:
                        dataSum[index] += dataOut[scan][index]
                    except ValueError as ve:
                        qtWidgets.QMessageBox.warning(self, "Data Error", 
                                                   "Trouble mixing" +
                                                   "data from different scans." +
                                                   "Common cause is scans " +
                                                   "have different number of " +
                                                   "data points\n %s" %
                                                   str(ve))
                       
        if self._dataSelections.plotAverageData():
            for index in countIndex:
                dataAverage = dataSum[index]/len(selectedScans)
                plotDataLabel = self._dataSelections.getDataLabels()
                dataLabel = "%s - Avg" % plotDataLabel[index] 
                if axisLabelIndex[index] == 1:
                    self._plotWidget.plotAx1Average(dataOut[scan][0], dataAverage, dataLabel)
                if axisLabelIndex[index] == 2:
                    self._plotWidget.plotAx2Average(dataOut[scan][0], dataAverage, dataLabel)
        self._plotWidget.plotDraw()                            
    '''
    Handle updating the plot window when only one scan is selected
    '''        
    def updatePlotDataSingle(self, counters, counterNames):
        logger.debug("Enter")
        data = []
        dataOut = []
        scans = self._dataNavigator.model().getTopDataSelectedNodes()[0]._specDataFile.scans[self._dataSelections.getSelectedScans()[0]]
        
        for counter in counterNames:
            try:
                data.append(scans.data[counter])
            except KeyError as ie:
                logger.exception("Tried to load data which does not have " +
                                 "counters selected. Please make a selection " +
                                 "for this type of data: Scan --%s--\n%s" % 
                                 (str(scans), str(ie)))
        try:
            dataOut = self._dataSelections.calcPlotData(data)
        except IndexError:
            qtWidgets.QMessageBox.warning(self, "No Data Warning", "NoData was selected")
        countIndex = range(1, len(dataOut))
        self._plotWidget.clear()
        plotAxisLabels = self._dataSelections.getPlotAxisLabels()
        plotDataLabel = self._dataSelections.getDataLabels()
        axisLabelIndex = self._dataSelections.getPlotAxisLabelsIndex()
        logger.debug("plotAxesLabels %s", plotAxisLabels)
        for index in countIndex:
            logger.debug("index, counters %s %s" % (index, counters))
            logger.debug("index, len(counters)-1 %s, %s" % (index, len(counters)-1 ))
            if axisLabelIndex[index] == 1:
                self._plotWidget.plotAx1(dataOut[0], dataOut[index], plotDataLabel[index])
                logger.debug("plotAxisLabels: %s" % plotAxisLabels)
                self._plotWidget.setXLabel(plotAxisLabels[0])
                self._plotWidget.setYLabel(plotAxisLabels[index])
            if axisLabelIndex[index] == 2:
                self._plotWidget.plotAx2(dataOut[0], dataOut[index], plotDataLabel[index])
                logger.debug("plotAxisLabels: %s" % plotAxisLabels)
                self._plotWidget.setXLabel(plotAxisLabels[0])
                self._plotWidget.setY2Label(plotAxisLabels[index])
        
        self._plotWidget.plotDraw()
                   
        