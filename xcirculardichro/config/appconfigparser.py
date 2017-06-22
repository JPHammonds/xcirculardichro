'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

from ConfigParser import ConfigParser
from Canvas import Line
from os.path import expanduser

CONFIG_FILENAME_DEFAULT = 'XCircularChiro.ini'

class AppConfigParser(ConfigParser):
    '''
    parser to configure the application from config file or command Line
    '''
    
    def __init__(self, fileName="", **kwargs):
        ConfigParser.__init__(self, **kwargs)
        userDir = expanduser('~')
        