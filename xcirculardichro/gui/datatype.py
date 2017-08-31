'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore

DATA_TYPES = ['None', ]

class DataType(qtWidgets.QDialog):
    dataTypeChanged = qtCore.pyqtSignal(int, name='dataTypeChanged')
    
    def __init__(self, parent=None, dataTypes=DATA_TYPES):
        super(DataType, self).__init__(parent)
        self.dataTypes = dataTypes
        layout = qtWidgets.QHBoxLayout()
        
        label = qtWidgets.QLabel("Select Type:")
        self.typeSelector = qtWidgets.QComboBox()
        self.typeSelector.insertItems(0, self.dataTypes)
        layout.addWidget(label)
        layout.addWidget(self.typeSelector)
        self.typeSelector.currentIndexChanged[int].connect(self.typeSelectionChanged)
        self.setLayout(layout)
        
    @qtCore.pyqtSlot(int)
    def typeSelectionChanged(self, typeIndex):
        self.dataTypeChanged.emit(typeIndex)