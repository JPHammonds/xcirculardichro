
'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import logging
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR
logger = logging.getLogger(__name__)
from xcirculardichro.gui.view.dataitem import DataItem

class SpecDataFileItem(DataItem):
    
    def __init__(self, fileName, specDataFile):
        super(SpecDataFileItem, self).__init__(fileName)
        logger.debug(METHOD_ENTER_STR % fileName)
        self.specDataFile = specDataFile
#        self.setData(self.specDataFile.fileName)
        
    def getSpecDataFile(self):
        logger.debug(METHOD_ENTER_STR)
        return self.specDataFile

