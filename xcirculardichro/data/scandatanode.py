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