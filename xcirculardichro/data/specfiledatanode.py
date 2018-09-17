'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
from xcirculardichro import METHOD_ENTER_STR
import os
from xcirculardichro.data import FileDataNode
from xcirculardichro.data import SpecScanNode
from spec2nexus.spec import SpecDataFile
import gc

logger = logging.getLogger(__name__)

class SpecFileDataNode(FileDataNode):
    
    def __init__(self, specDataFile, parent=None):
        super(SpecFileDataNode, self).__init__(specDataFile.fileName, 
                                               parent=parent)
        self._specDataFile = specDataFile
        self.loadScans()
        
    def getSpecDataFile(self):
        logger.debug(METHOD_ENTER_STR % self._specDataFile.fileName)
        return self._specDataFile
    
    def loadScans(self):
        scanKeys = sorted(self._specDataFile.scans, key=int)
        for scan in scanKeys:
            self.scans[scan] = self._specDataFile.scans[scan]
            logger.debug("Scan %s %s" % (scan, type(scan)))
            self.addChild(SpecScanNode(self._specDataFile.scans[scan]))
        
        
    def setChecked(self, checked):
        if checked == True:
            siblings = self._parent._children
            for sibling in siblings:
                #Avoid Recursion
                if sibling is not self:
                    sibling.setChecked(False)
        self._isChecked = checked
        
    def shortName(self):
        return os.path.split(self._specDataFile.fileName)[1]
    
    def getFileName(self):
        return self.getSpecDataFile().fileName
    
    def reload(self):
        logger.debug(METHOD_ENTER_STR)
        scanKeys = sorted(self._specDataFile.scans, key=int)
        logger.debug("Unload the old data")
        
        filename = self._specDataFile.fileName
        for scan in scanKeys:
            logger.debug("scan to remove %s" % self.scans[scan].__class__)
            self.removeSpecScan(scan)
        for scan in self._specDataFile.scans:
            scan = None
        self._specDataFile = None
        gc.collect
        logger.debug("Load current data in the file")
        self._specDataFile = SpecDataFile(filename)
        self.loadScans()
        gc.collect()

    def removeSpecScan(self, scan):
        logger.debug("scan children %s" % self._children)
        for child in self._children:
            if child._specScan == self.scans[scan]:
                logger.debug("child._specScan %s,scan %s" % (child._specScan, self.scans[scan].__class__))
                logger.debug("scan to remove %s" % self.scans[scan].scanNum)
                child.removeData()
                self.removeChild(child)
        self.scans[scan] = None
        #gc.collect()