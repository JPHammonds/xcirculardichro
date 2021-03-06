'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
from xcirculardichro import METHOD_ENTER_STR
from xcirculardichro.data import ScanDataNode
import gc
logger = logging.getLogger(__name__)

class SpecScanNode(ScanDataNode):
    
    def __init__(self, specScan, parent=None):
        logger.debug("Scan %s" % specScan)
        super(SpecScanNode, self).__init__(specScan.scanCmd, parent=parent)
        self._specScan = specScan
        dataKeys = list(self._specScan.data.keys())
        for key in dataKeys:
            self.data[key] = self._specScan.data[key][:]
        
        
    def getScan(self):
        logger.debug(METHOD_ENTER_STR)
        
        
    def shortName(self):
        return "S %s" % self._specScan.scanNum
    
    def removeData(self):
        logger.debug(METHOD_ENTER_STR % dir(self._specScan))
        dataKeys = list(self._specScan.data.keys())
        for key in dataKeys:
            logger.debug("self.data[%s] %s" % (key, self.data[key]))
            self.data[key] = None
        #gc.collect()
        self.data = {}
        self._specScan = None
        #gc.collect()
