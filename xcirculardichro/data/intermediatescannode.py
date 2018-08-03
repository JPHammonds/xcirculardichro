'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
from xcirculardichro import METHOD_ENTER_STR
from xcirculardichro.data import ScanDataNode
import numpy as np

logger = logging.getLogger(__name__)

NAME = 'name'
DATA = 'data'

class IntermediateScanNode(ScanDataNode):
    
    def __init__(self, name, parent=None):
        super(IntermediateScanNode, self).__init__(name, parent=parent)
        self.isInverted = False
        
    def addData(self, scanNum, scanCmd, axisLabels, axisLabelIndex, data, counterNames):
        '''
        Add scan information to this node
        '''
        logger.debug(METHOD_ENTER_STR)
        self.scanNum = scanNum  
        self.axisLabels = axisLabels
        self.axisLabelIndex = axisLabelIndex
        self.scanCmd = scanCmd
        self.counterNames = axisLabels
        logger.debug("Data %s" % data)
        for label in range(len(self.axisLabels)):
            self.data[axisLabels[label]] = np.copy(data[label][:])
        
        
    def setInverted(self, inverted):
        '''
        Flip the XMCD data to accomodate signals that come in inverted.
        Also Record that this has been done so that we know whether 
        or not we actually need to do the flip.
        '''
        logger.debug(METHOD_ENTER_STR % inverted)
        if inverted and not self.isInverted:
            logger.debug("Inverting scanNum %s" % self.scanNum)
            self.data['XMCD'][:] =  self.data['XMCD'][:] * -1
            self.isInverted = True
        elif not inverted and self.isInverted:
            logger.debug("removing Invert from scanNum %s" % self.scanNum)
            self.data['XMCD'][:] =  self.data['XMCD'][:] * -1
            self.isInverted = False    