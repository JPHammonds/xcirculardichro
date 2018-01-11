'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import sys
import PyQt5.QtWidgets as qtWidgets
from xcirculardichro import __path__ as XCD_PATH
from xcirculardichro.gui.xmcdmainwindow import XMCDMainWindow
from  spec2nexus.plugin import PLUGIN_SEARCH_PATH_ENVIRONMENT_VARIABLE \
    as S2N_PLUGIN_ENV_VAR
import os
import logging
logger = logging.getLogger(__name__)

def addXmcdPluginsToS2NPluginPath():
    #Append the directory for xcirculardichro._spec2nexus.plugins
    # to the spec2nexus plugin path so that the plugin for finding #U
    # parameters is found
    logger.debug("path " + str(XCD_PATH))
    REL_PATH_TO_S2N_PLUGINS = "_spec2nexus/plugins"
    PATH_TO_S2N_PLUGINS = os.path.join(XCD_PATH[0], \
                                       REL_PATH_TO_S2N_PLUGINS)
    logger.debug("PATH_TO_S2N_PLUGINS" + str(PATH_TO_S2N_PLUGINS))
    try:
        spec2nexusEnvPath = os.environ[S2N_PLUGIN_ENV_VAR]
        os.environ[S2N_PLUGIN_ENV_VAR] = PATH_TO_S2N_PLUGINS \
                                        + os.pathsep \
                                        + spec2nexusEnvPath
        logger.debug(S2N_PLUGIN_ENV_VAR  + " = " + str(os.environ[S2N_PLUGIN_ENV_VAR]))
    except KeyError:
        os.environ[S2N_PLUGIN_ENV_VAR] = PATH_TO_S2N_PLUGINS
        logger.debug(S2N_PLUGIN_ENV_VAR + "  =  " +  str(os.environ[S2N_PLUGIN_ENV_VAR]))
        
def main():
    
    # Add our plugins to the spec2nexus plugin path
    addXmcdPluginsToS2NPluginPath()
    # Start the app.    
    app = qtWidgets.QApplication(sys.argv)
    mainWindow = XMCDMainWindow()
#    mainWindow.show()
    sys.exit(app.exec_())