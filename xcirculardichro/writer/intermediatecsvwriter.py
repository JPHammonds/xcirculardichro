'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
from xcirculardichro.data.intermediatedatanode import IntermediateDataNode
from xcirculardichro.writer.writer import Writer
import logging
import csv
from xcirculardichro import METHOD_ENTER_STR
logger = logging.getLogger(__name__)

class IntermediateCSVWriter(Writer):
    
    def __init__(self, outFileName, selectionWidget = None):
        self.outFileName = outFileName
        self._dataSelections = selectionWidget
        
              
    def writeNodes(self, dataNodes):
        logger.debug(METHOD_ENTER_STR % str(dataNodes))
        scansForNode = {}
        selectedNodes = set()
        for scan in dataNodes:
            logger.debug("getting Node for %s" % scan)
            nodeForScan = self._dataSelections.getNodeContainingScan(scan)
            selectedNodes.add(nodeForScan)
            if not (nodeForScan in scansForNode.keys()):
                scansForNode[nodeForScan] = []
            scansForNode[nodeForScan].append(scan)
            print ("SelectedNodes %s" %selectedNodes)
        selectedNodes = list(selectedNodes)
        if hasattr(selectedNodes, '__iter__'):
            for node in selectedNodes:
                if not isinstance(node, IntermediateDataNode):
                    raise TypeError("all elements of dataNodes argument must " +
                                    "be IntermediateScanNode objects was %s" % 
                                    type(node))
        else:
            raise TypeError("Argument dataNodes must be an iterable")
        logger.debug("Writing to file %s" % self.outFileName)
        with open(self.outFileName, 'w') as outFile:
            outFile.write("FileNames: \n")
            for node in selectedNodes:
                outFile.write("%s\n" % node.fileName)
                for scan in scansForNode[node]:
                    outFile.write("--- %s\n" % scan)
                    self.writeScanData(node, scan, outFile)
                outFile.write("\n")

    def writeScanData(self, node, scan,outFile):
        '''
        Handle writing out the scan data.
        '''
        scanColumns = node.getScanNodes()[scan].getAxisLabels()
        logger.debug(scanColumns)
        data = node.getScanNodes()[scan].getData()
        writer = csv.writer(outFile, delimiter=',', lineterminator='\n')
        writer.writerow(scanColumns)
        logger.debug("data %s" % data)
        
        for index in range(len(data[scanColumns[0]])):
            thisPoint = [list(data[j])[index] for j in scanColumns]
            writer.writerow(thisPoint) 
