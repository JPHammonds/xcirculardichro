'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
from xcirculardichro.data.datanode import DataNode

class FileDataNode(DataNode):
    
    def __init__(self, name, parent=None):
        super(FileDataNode, self).__init__(name, parent=parent)
        self.scans = {}
        
    def getScanNodes(self):
        return self.scans
    
    def getFileName(self):
        raise NotImplementedError("This method must be implemented in the " +
                                  "subclass")