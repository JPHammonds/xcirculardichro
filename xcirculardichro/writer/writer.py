'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
from abc import abstractmethod, ABCMeta
import logging
from xcirculardichro import METHOD_ENTER_STR
logger = logging.getLogger(__name__)

class Writer(metaclass=ABCMeta):
    

    @abstractmethod
    def writeNodes(self, dataNodes):
        '''
        Write the combined output of severalNodes to the file using 
        this method
        '''
        raise NotImplementedError("Must subclass this and override " \
                                  "this method")
    