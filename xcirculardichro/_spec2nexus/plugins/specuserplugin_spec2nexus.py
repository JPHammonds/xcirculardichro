'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
from spec2nexus.plugin import ControlLineHandler, strip_first_word
from spec2nexus.spec import SpecDataFileHeader
from spec2nexus.eznx import makeGroup
import logging
from xcirculardichro import METHOD_ENTER_STR
logger = logging.getLogger(__name__)

class XCircularDichroU(ControlLineHandler):
    '''
    #U
    '''
    key = '#U'
    
    def process(self, text, spec_obj, *args, **kws):
        logger.debug(METHOD_ENTER_STR, text)
        subkey = text.split()[0].lstrip('#')
        if not hasattr(spec_obj, 'U'):
            spec_obj.U = {}
        textLine = strip_first_word(text)
        keyValue = textLine.split(":")
        try:
            spec_obj.U[keyValue[0]] = keyValue[1]
        except IndexError as ex:
            logger.exception("Error on: " +str(textLine))
        if isinstance(spec_obj, SpecDataFileHeader):
            spec_obj.addH5writer(self.key, self.writer)
            
            
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kwargs):
        '''Describe how to write U data'''
        
        desc = 'Sector4 User Parameters'
        group = makeGroup(h5parent, 'U', nxclass, description=desc)
        dd = {}
        for item, value in scan.U.items():
            dd[item] = map(str, value.split())
        writer.save_dict(group, dd)
        
class XCircularDichroX(ControlLineHandler):
    '''
    #X
    '''
    key = '#X'
    
    def process(self, text, spec_obj, *args, **kws):
        logger.debug(METHOD_ENTER_STR, text)
        subkey = text.split()[0].lstrip('#')
        if not hasattr(spec_obj, 'X'):
            spec_obj.X = {}
        textLine = strip_first_word(text)
        items = textLine.split("  ")
        for item in items:
            keyValue = item.split(":")
            try:
                spec_obj.X[keyValue[0]] = keyValue[1]
            except IndexError as ex:
                logger.exception("Error on: " +str(textLine))
            if isinstance(spec_obj, SpecDataFileHeader):
                spec_obj.addH5writer(self.key, self.writer)
            
            
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kwargs):
        '''Describe how to write X data'''
        
        desc = 'Sector4 Experiment Parameters'
        group = makeGroup(h5parent, 'X', nxclass, description=desc)
        dd = {}
        for item, value in scan.X.items():
            dd[item] = map(str, value.split())
        writer.save_dict(group, dd)
        
