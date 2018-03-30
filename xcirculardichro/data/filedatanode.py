'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
from xcirculardichro.data import DataNode

class FileDataNode(DataNode):
    
    def __init__(self, name, parent=None):
        super(FileDataNode, self).__init__(name, parent=parent)
        self.scans = {}
        
    def getScanNodes(self):
        '''
        Return a dictionary of scans in this file
        :return: scans found in this file
        :rtype: dict  
        '''
        return self.scans
    
    def getFileName(self):
        '''
        Default method meant to determine the file name that provided 
        data in a node.
        '''
        raise NotImplementedError("This method must be implemented in the " \
                                  "subclass")
        
    def getWriterClass(self):
        '''
        Default class that indicates that a Writer class is not found 
        for a particular FileDataNode.  This will provide a proper 
        writer to handle writing a node to a file but will also assist
        in enabling/disabling the File->Save menu option.
        Should be overridden by the subclass, if not throws a 
        NotImplementedError which is handled by the caller to 
        disable the file menu.  On successful completion in a subclass,
        this should return a Writer class.
            :return: Writer class
            :rtype: xcirculardichro.writer.Writer
            :raises NotImplementedError
            
        '''
        raise NotImplementedError("Writing is not supported for the " \
                                  "current Node selection %s" % \
                                  str(self.__class__))