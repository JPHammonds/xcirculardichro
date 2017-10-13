'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
from xcirculardichro.data.scandatanode import ScanDataNode
from xcirculardichro import METHOD_ENTER_STR

logger = logging.getLogger(__name__)

NAME = 'name'
DATA = 'data'

class IntermediateScanNode(ScanDataNode):
    
    def __init__(self, name, parent=None):
        super(IntermediateScanNode, self).__init__(name, parent=parent)
        
    def addData(self, scanNum, scanCmd, axisLabels, axisLabelIndex, data, counterNames):
        logger.debug(METHOD_ENTER_STR)
        self.scanNum = scanNum  
        self.axisLabels = axisLabels
        self.axisLabelIndex = axisLabelIndex
        self.scanCmd = scanCmd
        self.counterNames = axisLabels
        logger.debug("Data %s" % data)
        for label in range(len(self.axisLabels)):
            self.data[axisLabels[label]] = data[label][:]
        
        
    