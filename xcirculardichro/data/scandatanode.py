'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
from xcirculardichro.data.datanode import DataNode


class ScanDataNode(DataNode):
    
    def __init__(self, name, parent=None):
        super(ScanDataNode, self).__init__(name, parent=parent)
        self.scanNum = -1
        self.data = {}
        self.axisLabels = []
        self.axisLabelIndex = []
        self.counterNames = []
        self.scanCmd = None
        
    def getAxisLabels(self):
        return self.axisLabels
    
    def getAxisLabelIndex(self):
        return self.axisLabelIndex
    
    def getCounterNames(self):
        return self.counterNames
    
    def getScanCommand(self):
        return self.scanCmd
    
    def getScanNumber(self):
        return self.scanNum
    
    def getData(self):
        return self.data