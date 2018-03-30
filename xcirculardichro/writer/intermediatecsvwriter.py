'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import xcirculardichro.data.intermediatedatanode
#from xcirculardichro.data.intermediatedatanode import DataSelectionTypes
from xcirculardichro.writer import Writer
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
                if not isinstance(node, xcirculardichro.data.intermediatedatanode.IntermediateDataNode):
                    raise TypeError("all elements of dataNodes argument must " +
                                    "be IntermediateScanNode objects was %s" % 
                                    type(node))
        else:
            raise TypeError("Argument dataNodes must be an iterable")
        logger.debug("Writing to file %s" % self.outFileName)
        with open(self.outFileName, 'w') as outFile:
            if self._dataSelections.plotIndividualData():
                logger.debug("Saving PlotIndividualData")
                outFile.write("FileNames: \n")
                for node in selectedNodes:
                    outFile.write("%s\n" % node.fileName)
                    for scan in scansForNode[node]:
                        outFile.write("%s\n" % scan)
                        self.writeScanData(node, scan, outFile)
                    outFile.write("\n")
            if self._dataSelections.plotNormalizedData():
                logger.debug("Saving PlotNormalizedNode")
                self.writePlotNormalizedNode(selectedNodes, scansForNode, \
                                            outFile)
            if self._dataSelections.plotAverageData():
                logger.debug("Saving PlotAverage")
                self.writePlotAveragedNode(selectedNodes, scansForNode, \
                                            outFile)
            
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

    def writePlotNormalizedNode(self, nodes, scansForNode,outFile):
        logger.debug(METHOD_ENTER_STR % ((nodes, scansForNode, outFile),))
            
        scanType = []
        logger.debug("nodes %s" % nodes)
        logger.debug("nodes[0] %s" % nodes[0])
        logger.debug("nodes[0].name() %s" % nodes[0].name())
        logger.debug("nodes[0].name().split('-') === %s ===" % nodes[0].name().split('-'))
        scanType.append((nodes[0].name().split('-'))[1].strip())
        scanType.append("")
        if len(nodes) > 1:
            scanType[1] = (nodes[1].name()).split('-')[1].strip()
        logger.debug("scanType %s" % (scanType))   
        if scanType[0] == xcirculardichro.data.intermediatedatanode.DataSelectionTypes.STEP_NORMALIZED.name and \
            (len(nodes) == 2 and 
             scanType[1] == xcirculardichro.data.intermediatedatanode.DataSelectionTypes.STEP_NORMALIZED.name): 
            self.writeNormalizedNodeFromTwoStepNormalized(nodes, \
                                                      scansForNode, \
                                                      outFile)
        elif scanType[0] == xcirculardichro.data.intermediatedatanode.DataSelectionTypes.FULL_NORMALIZED.name:
            self.writeNormalizedNodeFromOneNormaializeNode(nodes, \
                                                        scansForNode, \
                                                        outFile)

    def writeNormalizedNodeFromTwoStepNormalized(self, nodes, \
                                                 scansForNode,outFile):
        logger.debug(METHOD_ENTER_STR% ((nodes, scansForNode, \
                                         outFile),))
        scan1 = nodes[0].getScanNodes()[scansForNode[nodes[0]][0]]
        scan2 = nodes[1].getScanNodes()[scansForNode[nodes[1]][0]]
        logger.debug("scan1 %s, scan2 %s" % (scan1, scan2))
        logger.debug("scan1.getData() %s, scan2.getData() %s" % \
                     (scan1.getData(), scan2.getData()))
        scanColumns = scan1.getAxisLabels()
        logger.debug("scanColumns %s" % scanColumns)
        data = {}
        data[scanColumns[0]] = scan1.getData()[scanColumns[0]]
        xas = (scan1.getData()[scanColumns[1]] + \
               scan2.getData()[scanColumns[1]])/2
        data[scanColumns[1]] = xas
        xmcd = scan1.getData()[scanColumns[2]] - \
            scan2.getData()[scanColumns[2]]
        data[scanColumns[2]] = xmcd
        logger.debug("Data %s" % data)
        outFile.write("FileNames: \n")
        outFile.write("%s\n" % nodes[0].fileName)
        outFile.write("%s\n" % nodes[1].fileName)
        outFile.write("Normalized Data\n")
        #outFile.write("--- %s\n" % data)
        writer = csv.writer(outFile, delimiter=',', lineterminator='\n')
        writer.writerow(scanColumns)
        for index in range(len(data[scanColumns[0]])):
            thisPoint = [list(data[j])[index] for j in scanColumns]
            writer.writerow(thisPoint)
        outFile.write("\n")
        
    def writeNormalizedNodeFromOneNormaializeNode(self, nodes, \
                                                  scansForNode,outFile):
        logger.debug(METHOD_ENTER_STR% ((nodes, scansForNode, \
                                         outFile),))
        scan1 = nodes[0].getScanNodes()[scansForNode[nodes[0]][0]]
        scanColumns = scan1.getAxisLabels()
        logger.debug("scanColumns %s" % scanColumns)
        data = {}
        data[scanColumns[0]] = scan1.getData()[scanColumns[0]]
        xas = scan1.getData()[scanColumns[1]]
        data[scanColumns[1]] = xas
        xmcd = scan1.getData()[scanColumns[2]]
        data[scanColumns[2]] = xmcd
        logger.debug("Data %s" % data)
        outFile.write("FileNames: \n")
        outFile.write("%s\n" % nodes[0].fileName)
        outFile.write("Normalized Data\n")
        #outFile.write("--- %s\n" % data)
        writer = csv.writer(outFile, delimiter=',', lineterminator='\n')
        writer.writerow(scanColumns)
        for index in range(len(data[scanColumns[0]])):
            thisPoint = [list(data[j])[index] for j in scanColumns]
            writer.writerow(thisPoint)
        outFile.write("\n")

        
    def writePlotAveragedNode(self,nodes, scansForNode, outFile):
        logger.debug(METHOD_ENTER_STR % ((nodes, scansForNode, outFile),))
        scansForNode = {}
        for node in nodes:
            scansForNode[node]= node.getScanNodes()
            logger.debug("node  %s" % node  )
            logger.debug("Scans for node %s: " % node)
            logger.debug("       %s" % scansForNode[node])
#         scanColumns = scansForNode[nodes[0]][0].getAxisLabels()
        firstNodeScans = nodes[0].getScanNodes()
        logger.debug("firstNodeScans %s" % firstNodeScans)
        scanColumns = firstNodeScans[list(firstNodeScans.keys())[0]].getAxisLabels()
        logger.debug("scanColumns %s" % scanColumns)
        data = {}
        numberOfDataSets = 0
        outFile.write("FileNames:\n")
        for node in nodes:
            outFile.write("%s\n" % node.fileName)
            nodeScans = node.getScanNodes()
            for scan in nodeScans:
                logger.debug("scan %s" % scan)
                if len(data) == 0:
                    data[scanColumns[0]] = node.scans[scan].getData()[scanColumns[0]]
                    for col in range(1, len(scanColumns)):
                        data[scanColumns[col]] = node.scans[scan].getData()[scanColumns[col]]
                    numDataSets = 1
                else:
                    for col in range(1, len(scanColumns)):
                        data[scanColumns[col]] += node.scans[scan].getData()[scanColumns[col]]
                    numDataSets += 1
        outFile.write("Averaged Data\n")
        writer = csv.writer(outFile, delimiter=',', lineterminator='\n')
        writer.writerow(scanColumns)
        for index in range(len(data[scanColumns[0]])):
            thisPoint = [list(data[j])[index] for j in scanColumns]
            writer.writerow(thisPoint)
        outFile.write("\n")
        