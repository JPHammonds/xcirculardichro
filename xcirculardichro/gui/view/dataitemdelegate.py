'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
import logging
from xcirculardichro.config.loggingConfig import METHOD_ENTER_STR
logger = logging.getLogger(__name__)

class DataItemDelegate(qtWidgets.QStyledItemDelegate):
    '''
    View delegate to be used in tree view to display data items as a node
    with a description and a checkbox to show whether this should be used
    in plots
    '''
    
    def __init__(self, parent=None):
        super(DataItemDelegate, self).__init__(parent)
        logger.debug(METHOD_ENTER_STR)
        self.editor = None
        
    def createEditor(self, parent, option, index):
        logger.debug("index.model().itemFromIndex(index) %s" % index.model().itemFromIndex(index))
        logger.debug("parent %s" % parent)
        logger.debug("option %s" % option)
        checkBox = qtWidgets.QCheckBox(index.model().itemFromIndex(index).text(), parent=parent)
        self.editor = checkBox
        self.editor.setAutoFillBackground(True)
        self.editor.stateChanged[int].connect(self.editorDataChanged)
        self.index = index
        return checkBox
    
    def setEditorData(self, editor, value):
        logger.debug(METHOD_ENTER_STR % ((editor, value),))
        valueData = value.data()
        logger.debug ("value, valueData %s %s" % (value,valueData,))
        editor.setChecked((valueData))
        self.index.model().setData(self.index, bool(editor.isChecked()))

    @qtCore.pyqtSlot(bool)
    def setChecked(self, checked):
        logger.debug(METHOD_ENTER_STR)
        self.editor.setChecked(checked)
        self.commitData.emit(self.sender())
        
    @qtCore.pyqtSlot()
    def currentIndexChanged(self):
        logger.debug(METHOD_ENTER_STR)
        self.commitData.emit(self.sender())
        
    def setModelData(self, editor, model, index):
        logger.debug(METHOD_ENTER_STR % ((editor, model, index),))
        model.setData(index, bool(editor.isChecked()))
        
    @qtCore.pyqtSlot(int)
    def editorDataChanged(self, state):
        logger.debug(METHOD_ENTER_STR % state)
        value = False
        if state == qtCore.Qt.Checked:
            value = True
        self.setModelData(self.editor, self.index.model(), self.index)
        self.commitData.emit(self.sender())
        