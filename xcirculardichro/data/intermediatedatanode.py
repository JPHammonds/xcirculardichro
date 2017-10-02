'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
from xcirculardichro.data.datanode import DataNode
from xcirculardichro.data.intermediatescannode import IntermediateScanNode
import PyQt5.QtWidgets as qtWidgets
from xcirculardichro.data.filedatanode import FileDataNode

logger = logging.getLogger(__name__)

SELECTED_NODES = 'selectedNodes'
DATA_SELECTION = 'dataSelection' 

class IntermediateDataNode(FileDataNode):
    
    def __init__(self, dataInfo, parent=None):
#         plotAxisLabels = self._dataSelections.getPlotAxisLabels()
#         plotAxisLabelsIndex = self._dataSelections.getPlotAxisLabelsIndex()
        selectedNodes = dataInfo[SELECTED_NODES]
        dataSelection = dataInfo[DATA_SELECTION]
        logger.debug("selected nodes %s" % selectedNodes)
        logger.debug("data selection %s" % dataSelection)
        
        newNodeName = ""
        for node in selectedNodes:
            newNodeName += node.shortName()
            newNodeName += (" - ")
            for scan in dataSelection.getSelectedScans():
                newNodeName += scan + ", "

        super(IntermediateDataNode, self).__init__(newNodeName, parent=parent)
        self._dataColumns = [[]]
        self._dataNames = []
#         scanNodes = node.getScanNodes()
#         scanNodeKeys = list(scanNodes.keys())
        logger.debug("selected nodes %s" % selectedNodes)
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
                                     " not have counters selected."  +
                                     "Multiple scans are selected and some" +
                                     "may not have the selected counters " +
                                     "Scan %s \n %s" % (str(selectedScan), str(ie)))
                        
                try:
                    logger.debug("scan %s data %s" % (selectedScan, data))
                    dataOut = dataSelection.calcPlotData(data)
                except IndexError:
                    qtWidgets.QMessageBox.warning(self, "No Data Warning", 
                                                  "No Data WasSelected")
                axisLabels = dataSelection.getPlotAxisLabels()
                axisLabelIndex = dataSelection.getPlotAxisLabelsIndex()
                self.scans[selectedScan].addData(scan.scanNum,  scan.scanCmd, axisLabels, axisLabelIndex, dataOut, counterNames)
                
        
    def shortName(self):
        return self._name