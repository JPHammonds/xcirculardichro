'''
Created on Aug 22, 2017

@author: hammonds
'''
import unittest
import PyQt5.QtGui as qtGui
import PyQt5.QtCore as qtCore
from xcirculardichro.gui.view.datanavigatorview import DataNavigatorView
from PyQt5.QtTest import QSignalSpy
from xcirculardichro.gui.view.dataitem import DataItem
from PyQt5.Qt import QApplication
import sys
from xcirculardichro.gui.model.datanavigatormodel import DataNavigatorModel

app =  QApplication(sys.argv)

class Test(unittest.TestCase):


    def setUp(self):
        self.dataNavigatorModel = DataNavigatorModel()
        self.dataNavigatorView = DataNavigatorView(dataModel = self.dataNavigatorModel)
        self.spyViewItemClicked = QSignalSpy(self.dataNavigatorView.clicked)
#        self.spyModelItemChanged = QSignalSpy(self.dataNavigatorModel.itemChanged[QStandardItem*])
        self.spyModelDataChanged = QSignalSpy(self.dataNavigatorModel.dataChanged)
        self.spyModelRowsInserted = QSignalSpy(self.dataNavigatorModel.rowsInserted)
        
    def tearDown(self):
        pass


    def testInit(self):
        DATA_TXT1 = "test1"
        DATA_TXT2 = "test2"
        
        row = 0
        col = 0
        rowsToAdd = 1
        
        self.assertEqual(self.dataNavigatorModel.rowCount(), 0)
        dataItem1 = DataItem(DATA_TXT1)
        dataItem2 = DataItem(DATA_TXT2)
        self.dataNavigatorModel.insertRows(row, rowsToAdd)
        self.assertEqual(self.dataNavigatorModel.rowCount(), 1)
#         self.dataNavigatorModel.setItem(row, dataItem1)
#         self.dataNavigatorModel.appendRow(dataItem1)
#         index = self.dataNavigatorModel.index(row, col)
#         dataFromIndex = self.dataNavigatorModel.data(index, role = qtCore.Qt.DisplayRole)
#         self.assertEqual(dataFromIndex, DATA_TXT1)
#         dataFromIndex = self.dataNavigatorModel.data(index, role = qtCore.Qt.CheckStateRole)
#         self.assertEqual(dataFromIndex, False)
# #        self.assertEqual(self.spyModelItemChanged, 1)
#         self.assertEqual(len(self.spyViewItemClicked), 0)
#         self.assertEqual(len(self.spyModelDataChanged), 0)
#         self.assertEqual(len(self.spyModelRowsInserted), 1)
#         self.assertEqual(self.dataNavigatorModel.rowCount(), 1)
        row += 1
        self.dataNavigatorModel.insertRows(row, rowsToAdd)
        self.assertEqual(self.dataNavigatorModel.rowCount(), 2)
        print(row)
        self.dataNavigatorModel.setItem(row, dataItem2)
        self.assertEqual(len(self.spyViewItemClicked), 0)
        self.assertEqual(len(self.spyModelDataChanged), 0)
        self.assertEqual(len(self.spyModelRowsInserted), 2)
        
        index = self.dataNavigatorModel.index(1,0)
        dataFromIndex = self.dataNavigatorModel.data(index, role = qtCore.Qt.DisplayRole)
        self.assertEqual(dataFromIndex, DATA_TXT2)
        dataFromIndex = self.dataNavigatorModel.data(index, role = qtCore.Qt.CheckStateRole)
        self.assertEqual(dataFromIndex, False)
#         dataFromIndex = self.dataNavigatorModel.data(index, role = qtCore.Qt.UserRole)
#         self.assertIsInstance(dataFromIndex, DataItem)
#         widgetFromIndex = self.dataNavigatorView.itemDelegate(index)
#         self.assertIsInstance(widgetFromIndex, DataItemDelegate)
#         widgetFromIndex.editor.setChecked(True)
#         self.assertEqual(dataFromIndex.data(), True)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()