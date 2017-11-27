'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
from xcirculardichro.data.intermediatescannode import IntermediateScanNode
import PyQt5.QtWidgets as qtWidgets
from xcirculardichro.data.filedatanode import FileDataNode
from enum import Enum
from xcirculardichro import METHOD_ENTER_STR

import logging
logger = logging.getLogger(__name__)

SELECTED_NODES = 'selectedNodes'
DATA_SELECTION = 'dataSelection' 
class DataSelectionTypes(Enum):
    RAW, AVERAGED, STEP_NORMALIZED = range(3) 

class IntermediateDataNode(FileDataNode):
    

    def __init__(self, dataInfo, parent=None, option=DataSelectionTypes.RAW):
#         plotAxisLabels = self._dataSelections.getPlotAxisLabels()
#         plotAxisLabelsIndex = self._dataSelections.getPlotAxisLabelsIndex()
        selectedNodes = dataInfo[SELECTED_NODES]
        dataSelection = dataInfo[DATA_SELECTION]
        logger.debug("selected nodes %s" % selectedNodes)
        logger.debug("data selection %s" % dataSelection)
        self.fileName  = \
            dataSelection.getNodeContainingScan(selectedNodes[0]).getFileName()
        
        newNodeName = ""
        for node in selectedNodes:
            newNodeName += node.shortName()
            newNodeName += (" - %s " % option.name)
            for scan in dataSelection.getSelectedScans():
                newNodeName += scan + ", "

        super(IntermediateDataNode, self).__init__(newNodeName, parent=parent)
        self._dataColumns = [[]]
        self._dataNames = []
#         scanNodes = node.getScanNodes()
#         scanNodeKeys = list(scanNodes.keys())
        logger.debug("selected nodes %s" % selectedNodes)
        if option == DataSelectionTypes.RAW:
            self.insertRawData(selectedNodes, dataSelection)
        elif option == DataSelectionTypes.AVERAGED:
            self.insertAveragedData(selectedNodes, dataSelection)
        elif option == DataSelectionTypes.STEP_NORMALIZED:
            self.insertStepNormalizedData(selectedNodes, dataSelection)
    

    def getAverageData(self, dataSelection):
        logger.debug(METHOD_ENTER_STR % dataSelection)
        counters, counterNames = dataSelection.getSelectedCounterInfo()
        currentSelectedScans = dataSelection.getSelectedScans()
        logger.debug("SelectedScans: %s" % currentSelectedScans)
        data = {}
        scans = {}
        dataOut = {}
        dataSum = {}
        dataAverage = []
        indices = []
        
        for selectedScan in currentSelectedScans:
            data[selectedScan] = []
            dataOut[selectedScan] = {}
        
        for selectedScan in currentSelectedScans:
            logger.debug("Adding scan %s type %s" % (selectedScan, type(selectedScan)))
            node = dataSelection.getNodeContainingScan(selectedScan)
            scans[selectedScan] = node.scans[selectedScan]
            for counter in counterNames:
                try:
                    data[selectedScan].append(scans[selectedScan].data[counter][:])
                except KeyError as ie:
                    logger.exception("Tried to read data which does not have " + "counter %s. scan: %s Exception %s ", (counter, scans[selectedScan], ie))
            
            try:
                dataOut[selectedScan] = dataSelection.calcPlotData(data[selectedScan])
            except IndexError:
                logger.warning("No data warning", "No data Was selected")
            countIndex = range(1, len(dataOut[selectedScan]))
            logger.debug("dataOut %s" % dataOut)
            indices = range(len(dataOut[selectedScan]))
            logger.debug("Indices: %s " % indices)
            for index in indices:
                logger.debug("dataOut[%s]: %s, index: %s" % (selectedScan, dataOut[selectedScan], index))
                if index == 0:
                    dataSum[index] = dataOut[selectedScan][index][:]
                else:
                    try:
                        if selectedScan == currentSelectedScans[0]:
                            logger.debug("Adding index %s for scan %s" % (index, selectedScan))
                            dataSum[index] = dataOut[selectedScan][index][:]
                        else:
                            logger.debug("Summing index %s for scan %s" % (index, selectedScan))
                            dataSum[index] += dataOut[selectedScan][index][:]
                    except ValueError as ve:
                        logger.warning("Data Error", "Trouble mixing data " + "from differnet scans" + "Common Cause is scans " + "have different number " + "of data points\n %s, " + " data[%] %s\n dataSum %s" % (str(ve), selectedScan, dataOut[selectedScan], dataSum))
                    except KeyError as ke:
                        logger.warning("KeyError %s, data[%s] %s\n dataSum %s" % (str(ke), selectedScan, dataOut[selectedScan], dataSum))
        
        for index in indices:
            if index == 0: #X Axis
                dataAverage.append(dataSum[index])
            else:
                dataAverage.append(dataSum[index][:] / len(currentSelectedScans)) # Average the y axes
        
        return dataAverage

    def getFileName(self):
        return self.fileName

    def insertAveragedData(self, selectedNodes, dataSelection):    
        logger.debug(METHOD_ENTER_STR % selectedNodes)
        
#            logger.debug("Adding Node %s" % node)
        dataAverage = self.getAverageData(dataSelection)
        counters, counterNames = dataSelection.getSelectedCounterInfo()
        currentSelectedScans = dataSelection.getSelectedScans()
        self.scans["Average %s" % str(currentSelectedScans)] = \
            IntermediateScanNode("Average %s" % str(currentSelectedScans), 
                                 parent=self)
        axisLabels = dataSelection.getPlotAxisLabels()
        axisLabelIndex = dataSelection.getPlotAxisLabelsIndex()
        logger.debug("AxisLabels %s" % axisLabels)
        logger.debug("axisLabelsIndex %s" % axisLabelIndex)
        logger.debug("counterNames %s" % counterNames )
        self.scans["Average %s" % str(currentSelectedScans)] \
            .addData("Average %s" % str(currentSelectedScans), 
                     "shared", 
                     axisLabels, 
                     axisLabelIndex, 
                     dataAverage, 
                     counterNames)
            
            
    def insertRawData(self, selectedNodes, dataSelection):
        logger.debug(METHOD_ENTER_STR % selectedNodes)
        for node in selectedNodes:
            logger.debug("Adding Node %s" % node)
    
            dataOut = []
            for selectedScan in dataSelection.getSelectedScans():
                data = []
                logger.debug("Adding Scan %s type %s" % (selectedScan, type(selectedScan)))
                scan = node.scans[selectedScan]
                self.scans[selectedScan] = IntermediateScanNode(str(scan.scanNum), parent=self)
                counters, counterNames = dataSelection.getSelectedCounterInfo()
                logger.debug("counters %s", counters)
                logger.debug("counterNames %s", counterNames)
                for counter in counterNames:
                    try:
                        data.append(node.scans[selectedScan].data[counter])
                    except KeyError as ie:
                        logger.exception("Tried to load data which does" + 
                                         " not have counters selected." + 
                                         "Multiple scans are selected and some" + 
                                         "may not have the selected counters " + 
                                         "Scan %s \n %s" % 
                                         (str(selectedScan), str(ie)))
                
                
                try:
                    logger.debug("scan %s data %s" % (selectedScan, data))
                    dataOut = dataSelection.calcPlotData(data)
                except IndexError:
                    qtWidgets.QMessageBox.warning(self, "No Data Warning", "No Data WasSelected")
                axisLabels = dataSelection.getPlotAxisLabels()
                axisLabelIndex = dataSelection.getPlotAxisLabelsIndex()
                self.scans[selectedScan].addData(scan.scanNum, scan.scanCmd, axisLabels, axisLabelIndex, dataOut, counterNames)

    def insertStepNormalizedData(self, selectedNodes, dataSelection):
        logger.debug(METHOD_ENTER_STR % selectedNodes)
        dataAverage = self.getAverageData(dataSelection)
        correctedData = dataSelection.getCorrectedData(dataAverage[0], dataAverage[1:])
        counters, counterNames = dataSelection.getSelectedCounterInfo()
        currentSelectedScans = dataSelection.getSelectedScans()
        logger.debug("Average Data %s" % dataAverage)
        logger.debug("CorrectedData %s" % correctedData) 
        self.scans["%s %s" % (DataSelectionTypes.STEP_NORMALIZED.name, str(currentSelectedScans))] = \
            IntermediateScanNode("%s %s" % (DataSelectionTypes.STEP_NORMALIZED.name, str(currentSelectedScans)), 
                                 parent=self)
        axisLabels = dataSelection.getPlotAxisLabels()
        axisLabelIndex = dataSelection.getPlotAxisLabelsIndex()
        logger.debug("AxisLabels %s" % axisLabels)
        logger.debug("axisLabelsIndex %s" % axisLabelIndex)
        logger.debug("counterNames %s" % counterNames )
        correctedData.insert(0, dataAverage[0])
        self.scans["%s %s" % (DataSelectionTypes.STEP_NORMALIZED.name, str(currentSelectedScans))] \
            .addData("%s %s" % (DataSelectionTypes.STEP_NORMALIZED.name, str(currentSelectedScans)), 
                     "shared", 
                     axisLabels, 
                     axisLabelIndex, 
                     correctedData, 
                     counterNames)
            
    def shortName(self):
        return self._name
    

