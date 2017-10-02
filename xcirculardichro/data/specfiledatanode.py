'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
from xcirculardichro.data.datanode import DataNode
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR

logger = logging.getLogger(__name__)

class SpecFileDataNode(DataNode):
    
    def __init__(self, specDataFile, parent=None):
        super(SpecFileDataNode, self).__init__(specDataFile.fileName, 
                                               parent=parent)
        self._specDataFile = specDataFile
        
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