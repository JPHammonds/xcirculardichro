'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
from xcirculardichro import METHOD_ENTER_STR
import os
from xcirculardichro.data.specscannode import SpecScanNode
from xcirculardichro.data.filedatanode import FileDataNode

logger = logging.getLogger(__name__)

class SpecFileDataNode(FileDataNode):
    
    def __init__(self, specDataFile, parent=None):
        super(SpecFileDataNode, self).__init__(specDataFile.fileName, 
                                               parent=parent)
        self._specDataFile = specDataFile
        scanKeys = sorted(self._specDataFile.scans, key=int)
        for scan in scanKeys:
            self.scans[scan] = self._specDataFile.scans[scan]
            logger.debug("Scan %s %s" % (scan, type(scan)))
            self.addChild(SpecScanNode(specDataFile.scans[scan]))
        
    def getSpecDataFile(self):
        logger.debug(METHOD_ENTER_STR % self._specDataFile.fileName)
        return self._specDataFile
    
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
    
