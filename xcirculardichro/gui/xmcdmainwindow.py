'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging

import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore

from spec2nexus.spec import SpecDataFile, NotASpecDataFile
from xcirculardichro import METHOD_ENTER_STR, METHOD_EXIT_STR
from xcirculardichro.gui.xmcddatanavigator import XMCDDataNavigator
from xcirculardichro.gui.plotwidget import PlotWidget
from xcirculardichro.gui.dataselection.selectionholder import SelectionHolder
from xcirculardichro.data.intermediatedatanode import SELECTED_NODES,\
    DataSelectionTypes
import os
from xcirculardichro.writer.intermediatecsvwriter import IntermediateCSVWriter
from xcirculardichro.gui.dataselection.AbstractSelectionDisplay import SelectionTypeNames
from specguiutils.positionerselector import PositionerSelector

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
        self.positionersToDisplay = []
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
        self._dataSelections.plotOptionChanged.connect(self.updatePlotData)
        self._plotWidget.leftSelectionChanged[str].connect(self.handleLeftDataSelectionChanged)
        self._plotWidget.rightSelectionChanged[str].connect(self.handleRightDataSelectionChanged)
        self._dataSelections.pointSelectionAxisChanged[int].connect(self._plotWidget.setPointSelectionAxis)
        self._dataSelections.pointSelectionTypeChanged[int].connect(self._plotWidget.setPointSelectionType)
        self._dataSelections.pointSelectionReloadPicks.connect(self.handlePointSelectionReloadPicks)
        logger.debug(METHOD_EXIT_STR)
        
    def _createMenuBar(self):
        '''
        internal method to setup the menu bar for this application
        '''
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu('File')
        viewMenu = menuBar.addMenu('View')
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

        self.selectPositionerParams = \
            qtWidgets.QAction("SelectPositionerParameters", self)
        self.selectUserParams = \
            qtWidgets.QAction("SelectUserParameters", self)
        self.selectPositionerParams.triggered.connect(self._selectPositionerParameters)
        self.selectUserParams.triggered.connect(self._selectUserParameters)

        self.captureCurrentAction = \
            qtWidgets.QAction("Capture Current", self)
        self.captureCurrentAction.triggered.connect(self.captureCurrent)
        
        self.captureCurrentAverageAction = \
            qtWidgets.QAction("Capture Current Average", self)
        self.captureCurrentAverageAction.triggered.connect(self.captureCurrentAverage)

        self.captureCurrentCorrectedAction = qtWidgets.QAction("Capture Current Corrected", self)
        self.captureCurrentCorrectedAction.triggered.connect(self.captureCurrentCorrected)
        
        exitAction = qtWidgets.QAction("Exit", self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
#        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(closeAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exportAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        viewMenu.addAction(self.selectPositionerParams)
        viewMenu.addAction(self.selectUserParams)
        
        dataMenu.addAction(self.captureCurrentAction)
        dataMenu.addAction(self.captureCurrentAverageAction)
        dataMenu.addAction(self.captureCurrentCorrectedAction)
        
        viewMenu.aboutToShow.connect(self._configureViewMenuEnable)
        dataMenu.aboutToShow.connect(self._configureDataMenuEnable)
        
    @qtCore.pyqtSlot()
    def _configureDataMenuEnable(self):
        logger.debug(METHOD_ENTER_STR)
        self.captureCurrentAction.setEnabled(True)
        self.captureCurrentAverageAction.setEnabled(True)
        self.captureCurrentCorrectedAction.setEnabled(True)
        try:
            if self._dataSelections.getSelectedScans() is None:
                self.captureCurrentAction.setEnabled(False)
                self.captureCurrentAverageAction.setEnabled(False)
                self.captureCurrentCorrectedAction.setEnabled(False)
            elif not self._dataSelections.isMultipleScansSelected():
                self.captureCurrentAverageAction.setEnabled(False)
            if not self._dataSelections.hasValidPointSelectionInfo():
                self.captureCurrentCorrectedAction.setEnabled(False)
        except NotImplementedError as ex:
            self.captureCurrentAction.setEnabled(False)
            self.captureCurrentAverageAction.setEnabled(False)
            self.captureCurrentCorrectedAction.setEnabled(False)
            
    @qtCore.pyqtSlot()
    def _configureViewMenuEnable(self):
        logger.debug(METHOD_ENTER_STR)
        if self._dataSelections.isSelectionType(SelectionTypeNames.SPEC_SELECTION):
            self.selectPositionerParams.setEnabled(True)
            self.selectUserParams.setEnabled(True)
        else:
            self.selectPositionerParams.setEnabled(False)
            self.selectUserParams.setEnabled(False)
        
    @qtCore.pyqtSlot() 
    def captureCurrent(self):
        logger.debug(METHOD_ENTER_STR)
        dataSelection = self._dataSelections._selectionWidget
        self._dataNavigator.addIntermediateDataNode(dataSelection, \
                                                    option=DataSelectionTypes.RAW)
        
    @qtCore.pyqtSlot() 
    def captureCurrentAverage(self):
        logger.debug(METHOD_ENTER_STR)
        dataSelection = self._dataSelections._selectionWidget
        self._dataNavigator.addIntermediateDataNode(dataSelection, \
                                                    option=DataSelectionTypes.AVERAGED)
        
    @qtCore.pyqtSlot() 
    def captureCurrentCorrected(self):
        logger.debug(METHOD_ENTER_STR)
        dataSelection = self._dataSelections._selectionWidget
        self._dataNavigator.addIntermediateDataNode(dataSelection, \
                                                    option=DataSelectionTypes.STEP_NORMALIZED)
        
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
        
    @qtCore.pyqtSlot(str)
    def handleLeftDataSelectionChanged(self, label):
        '''
        Handle selection on left side of the plot.  Feed selection information 
        to the choice widget and then handle any necessary plot changes
        '''
        logger.debug(METHOD_ENTER_STR % label)
        selection = self._plotWidget.getLeftSelectionIndexes(label)
        average = self._plotWidget.getLeftSelectionAverage(label)
        self._dataSelections.setLeftDataSelection(label, selection, average)
        #self.updatePlotData()
        
    @qtCore.pyqtSlot(str)
    def handleRightDataSelectionChanged(self, label):
        '''
        Handle selection on right side of the plot.  Feed selection information 
        to the choice widget and then handle any necessary plot changes
        '''
        logger.debug(METHOD_ENTER_STR % label)
        selection = self._plotWidget.getRightSelectionIndexes(label)
        average = self._plotWidget.getRightSelectionAverage(label)
        self._dataSelections.setRightDataSelection(label, selection, average)
        #self.updatePlotData()
        
        
    @qtCore.pyqtSlot(qtCore.QModelIndex, qtCore.QModelIndex)
    def handleNavigatorDataChanged(self, beginIndex, endIndex):
        logger.debug("begin Index %s, endIndex %s" % (beginIndex, endIndex))
        checkedNodes = self._dataNavigator.model().getTopDataSelectedNodes()
        self._dataSelections.setSelectedNodes(checkedNodes)
        self._dataSelections.setPostionersToDisplay(self.positionersToDisplay)
        self._dataSelections.handleDataSelectionsChanged()
              
    def handlePointSelectionReloadPicks(self, preEdgePoints, postEdgePoints):
        logger.debug(METHOD_ENTER_STR % ((preEdgePoints, postEdgePoints, "a"),))
        self._plotWidget.applyPickPoints(preEdgePoints, postEdgePoints)     
        logger.debug(METHOD_EXIT_STR)
        
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
        selectedScan = self._dataSelections.getSelectedScans()[0]
        logger.debug("First Selected Node %s" % selectedScan)
        selectedName = \
            self._dataSelections.getNodeContainingScan(selectedScan).getFileName()
        logger.debug("selectedName %s" % selectedName)
        folderOfSelected = os.path.dirname(str(selectedName))
        logger.debug("First Selected File %s" % folderOfSelected)
        
        fileName,junk = qtWidgets.QFileDialog.getSaveFileName(None, 
                                                'Save Selected Nodes', 
                                                folderOfSelected)
        
        writer = IntermediateCSVWriter(str(fileName), \
                                       selectionWidget=self._dataSelections)
        
        selectedScans = self._dataSelections.getSelectedScans()
        writer.writeNodes(selectedScans)
        
    @qtCore.pyqtSlot()
    def saveAsFile(self):
        logger.debug(METHOD_ENTER_STR)
        
    @qtCore.pyqtSlot()
    def _selectPositionerParameters(self):
        logger.debug(METHOD_ENTER_STR)
        selectedScans = self._dataSelections.getSelectedScans()
        firstNode = self._dataSelections.getNodeContainingScan(selectedScans[0])
        specScan = firstNode.scans[selectedScans[0]]
        parameters = specScan.positioner.keys()
        logger.debug("Parameters %s" % parameters)
        self.positionersToDisplay = PositionerSelector.getPositionSelectorModalDialog(specScan.positioner)
        logger.debug("Positioners %s" % self.positionersToDisplay)
        self._dataSelections.setPostionersToDisplay(self.positionersToDisplay)
        
    @qtCore.pyqtSlot()
    def _selectUserParameters(self):
        '''
        set up a dialog to allow the user to select parameters defined 
        in the #U fields in a scan.  From this selection, the selected 
        parameters will be added to the scanBrowser table to provide 
        the user with more information as selection criteria for which 
        scans to select for processing
        '''
        logger.debug(METHOD_ENTER_STR)
        selectedScans = self._dataSelections.getSelectedScans()
        firstNode = self._dataSelections.getNodeContainingScan(selectedScans[0])
        specScan = firstNode.scans[selectedScans[0]]
        parameters = specScan.U.keys()
        logger.debug("Parameters %s" % parameters)
        try:
            self.userParamsToDisplay = PositionerSelector.getPositionSelectorModalDialog(specScan.U)
        except :
            warningMessage = "No user parameters were found for the " \
                    + "selected scans.  Either no #U lines were found in "\
                    + "the spec file or no plugin was found to parse " \
                    + "the #U"
            qtWidgets.QMessageBox.warning(self, \
                                          "User Parameters Not Found", \
                                          warningMessage)
            return
        logger.debug("Positioners %s" % self.userParamsToDisplay)
        self._dataSelections.setUserParamsToDisplay(self.userParamsToDisplay)
        
    def updatePlotData(self):
        '''
        Performs all updates to the plots given real data.
        '''
        counters, counterNames = self._dataSelections.getSelectedCounterInfo()
        logger.debug("Data selected for this plot %s" % counters)
        if not self._dataSelections.isMultipleScansSelected():
            if (len(counters) == 0) and (len(counterNames)==0):
                self._plotWidget.clear()
                return
            self.updatePlotDataSingle(counters, counterNames)
        else:
            self.updatePlotDataMultiple(counters, counterNames)
            
    def updatePlotDataMultiple(self, counters, counterNames, 
                               displayAverage=True, displayEach=True):
        '''
        Handle updating the plot window when multiple scans are selected
        '''
        logger.debug(METHOD_ENTER_STR % ((counters, counterNames),))
        data = {}
        dataOut = {}
        self._plotWidget.clear()
        
        dataSum = []
        dataAverage = []
        selectedScans = self._dataSelections.getSelectedScans()
        logger.debug("SelectedScans %s" % selectedScans)
        
        normalizedData = []

        for scan in selectedScans:
            data[scan] = []
            dataOut[scan] = []
#             thisScan = self._dataNavigator.model().getTopDataSelectedNodes()[0]._specDataFile.scans[scan]
            node = self._dataSelections.getNodeContainingScan(scan)
            logger.debug("Scans in node %s: %s" % (node, node.scans))
            thisScan = node.scans[scan]
            for counter in counterNames:
                try:
                    logger.debug("Type of data %s" % type(thisScan.data[counter][:]))
                    data[scan].append(thisScan.data[counter][:])
                except KeyError as ie:
                    logger.exception("Tried to load data which does" +
                                     " not have counters selected."  +
                                     "Multiple scans are selected and some" +
                                     "may not have the selected counters " +
                                     "Scan %s \n %s" % (str(scan), str(ie)))
            try:
                dataOut[scan] = self._dataSelections.calcPlotData(data[scan])
                logger.debug("Type for data out %s" % type(dataOut[scan]))
            except IndexError:
                qtWidgets.QMessageBox.warning(self, "No Data Warning", 
                                          "No Data Was Selected")
            countIndex = range(1, len(dataOut[scan]))   #start at 1 since 0 is x axis
            plotAxisLabels = self._dataSelections.getPlotAxisLabels()
            axisLabelIndex = self._dataSelections.getPlotAxisLabelsIndex()
            if self._dataSelections.plotIndividualData():
                for index in countIndex:
                    dataLabel = "%s - Scan %s" % (plotAxisLabels[index], scan) 
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
                dataSum = dataOut[scan][:] 
            else:
                for index in countIndex:
                    logger.debug("dataSum[%d] %s" % (index,dataSum[index]))
                    try:
                        dataSum[index] += dataOut[scan][index][:]
                    except ValueError as ve:
                        qtWidgets.QMessageBox.warning(self, "Data Error", 
                                                   "Trouble mixing" +
                                                   "data from different scans." +
                                                   "Common cause is scans " +
                                                   "have different number of " +
                                                   "data points\n %s" %
                                                   str(ve))
                       
        dataAverage = None
        correctedData = None
        
        if self._dataSelections.plotAverageData():
            dataAverageArray = []
            for index in countIndex:
                dataAverage = dataSum[index][:]/len(selectedScans)
                plotDataLabel = self._dataSelections.getPlotAxisLabels()
                dataLabel = "%s - Avg" % plotDataLabel[index] 
                if axisLabelIndex[index] == 1:
                    self._plotWidget.plotAx1Average(dataOut[scan][0], 
                                                    dataAverage, 
                                                    dataLabel)
                    self._plotWidget.setXLabel(plotAxisLabels[0])
                    self._plotWidget.setYLabel(plotAxisLabels[index])
                if axisLabelIndex[index] == 2:
                    self._plotWidget.plotAx2Average(dataOut[scan][0], 
                                                    dataAverage, 
                                                    dataLabel)
                    self._plotWidget.setXLabel(plotAxisLabels[0])
                    self._plotWidget.setY2Label(plotAxisLabels[index])
                dataAverageArray.append(dataAverage)
            if self._dataSelections.plotCorrectedData():
                correctedData = \
                    self._dataSelections.getCorrectedData(dataOut[scan][0], \
                                                          dataAverageArray)
                logger.debug("Corrected Data: %s" % correctedData)
                for index in countIndex:
                    logger.debug("index %s " % index)
                    dataLabel = "%s - Corrected" % plotDataLabel[index]
                    
                    if axisLabelIndex[index] == 1:
                        self._plotWidget.plotAx3Corrected(dataOut[scan][0],
                                                          correctedData[index-1],
                                                          dataLabel)
                    elif axisLabelIndex[index] == 2:
                        self._plotWidget.plotAx4Corrected(dataOut[scan][0],
                                                          correctedData[index-1],
                                                          dataLabel)
        if self._dataSelections.plotNormalizedData():
            if len(selectedScans) == 2:
                normalizedData.append(dataSum[1]/2)
                normalizedData.append(data[selectedScans[0]][2] - data[selectedScans[1]][2])
                self._plotWidget.plotAx3Corrected(dataOut[scan][0],
                                         normalizedData[0],
                                         "Normalized XAS")
                self._plotWidget.plotAx4Corrected(dataOut[scan][0],
                                         normalizedData[1],
                                         "Normalized XMCD")
        
        self._plotWidget.plotDraw()                            

    def updatePlotDataSingle(self, counters, counterNames):
        '''
        Handle updating the plot window when only one scan is selected
        '''        
        logger.debug(METHOD_ENTER_STR % ((counters, counterNames), ))
        data = []
        dataOut = []
        logger.debug("SelectedScans %s" % self._dataSelections.getSelectedScans())
        node = self._dataSelections.getNodeContainingScan(self._dataSelections.getSelectedScans()[0])
        logger.debug("Scans in node %s: %s" % (node, node.scans))
        scans = node.scans[self._dataSelections.getSelectedScans()[0]]
#         scans = self._dataNavigator.model().getTopDataSelectedNodes()[0]._specDataFile.scans[self._dataSelections.getSelectedScans()[0]]
        logger.debug("counters %s", counters)
        logger.debug("counterNames %s", counterNames)
        
        for counter in counterNames:
            try:
                data.append(scans.data[counter])
            except KeyError as ie:
                logger.exception("Tried to load data which does not have " +
                                 "counters selected. Please make a selection " +
                                 "for this type of data: \nScan --%s--\nScans.data.keys -- %s\n%s" % 
                                 (str(scans), str(list(scans.data.keys())), str(ie)))
        try:
            dataOut = self._dataSelections.calcPlotData(data)
        except IndexError:
            qtWidgets.QMessageBox.warning(self, "No Data Warning", "NoData was selected")
        countIndex = range(1, len(dataOut))
        self._plotWidget.clear()
        plotAxisLabels = self._dataSelections.getPlotAxisLabels()
#         plotDataLabel = self._dataSelections.getPlotAxisLabels()
        axisLabelIndex = self._dataSelections.getPlotAxisLabelsIndex()
        logger.debug("plotAxesLabels %s", plotAxisLabels)
        logger.debug("axisLabelIndex %s", axisLabelIndex)
        logger.debug("countIndex " + str(countIndex))
        for index in countIndex:
            logger.debug("index, counters %s %s" % (index, counters))
            #logger.debug("index, len(counters)-1 %s, %s" % (index, len(counters)-1 ))
            if axisLabelIndex[index] == 1:
                logger.debug("dataOut %s" %dataOut)
                self._plotWidget.plotAx1(dataOut[0], 
                                         dataOut[index], 
                                         plotAxisLabels[index])
                logger.debug("plotAxisLabels: %s" % plotAxisLabels)
                self._plotWidget.setXLabel(plotAxisLabels[0])
                self._plotWidget.setYLabel(plotAxisLabels[index])
            if axisLabelIndex[index] == 2:
                self._plotWidget.plotAx2(dataOut[0], 
                                         dataOut[index], 
                                         plotAxisLabels[index])
                logger.debug("plotAxisLabels: %s" % plotAxisLabels)
                self._plotWidget.setXLabel(plotAxisLabels[0])
                self._plotWidget.setY2Label(plotAxisLabels[index])

        if self._dataSelections.plotCorrectedData():
            correctedData = \
                self._dataSelections.getCorrectedData(dataOut[0], \
                                                      dataOut[1:])
            plotDataLabel = self._dataSelections.getPlotAxisLabels()
            logger.debug("Corrected Data: %s" % correctedData)
            for index in countIndex:
                logger.debug("index %s " % index)
                dataLabel = "%s - Corrected" % plotDataLabel[index]
                
                if axisLabelIndex[index] == 1:
                    self._plotWidget.plotAx3Corrected(dataOut[0],
                                                      correctedData[index-1],
                                                      dataLabel)
                elif axisLabelIndex[index] == 2:
                    self._plotWidget.plotAx4Corrected(dataOut[0],
                                                      correctedData[index-1],
                                                      dataLabel)
                    
        self._plotWidget.plotDraw()
                   
        