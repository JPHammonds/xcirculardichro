'''
Created on Sep 1, 2017

@author: hammonds
'''
import unittest
from xcirculardichro.gui.dataselection.intermediatedataselection import IntermediateDataSelection
from PyQt5.QtWidgets import QApplication
import sys
from xcirculardichro.data.specfiledatanode import SpecFileDataNode
from spec2nexus.spec import SpecDataFile
import os

app = QApplication(sys.argv)
DATAPATH = 'DATAPATH'
FLUORESCENCE_FILE = "Brian-Nick/Fluorescence/lineup"

class Test(unittest.TestCase):


    def setUp(self):
        self.selection = IntermediateDataSelection()
        print(dir (self.selection))
        self.dataPath = os.environ.get(DATAPATH)
        specDataFileName = os.path.join(self.dataPath, FLUORESCENCE_FILE)
        specDataFile = SpecDataFile(specDataFileName)
        specNode = SpecFileDataNode(specDataFile)
        
        
    def tearDown(self):
        pass


    def testMethodsExist(self):
        try:
            self.selection.isMultipleScansSelected()
        except NotImplementedError as ex:
            self.fail(ex)
        try:
            self.selection.getPlotAxisLabels()
        except NotImplementedError as ex:
            self.fail(ex)
        except IndexError as ex:
            print("No scansselected")
            
#         try:
#             self.selection.getDataLabels()
#         except NotImplementedError as ex:
#             self.fail(ex)
        try:
            self.selection.getPlotAxisLabelsIndex()
        except NotImplementedError as ex:
            self.fail(ex)
        try:
            self.selection.getSelectedScans()
        except NotImplementedError as ex:
            self.fail(ex)
        try:
            self.selection.plotIndividualData()
        except NotImplementedError as ex:
            self.fail(ex)
        try:
            self.selection.plotAverageData()
        except NotImplementedError as ex:
            self.fail(ex)
        try:
            self.selection.setupDisplayWithSelectedNodes()
        except NotImplementedError as ex:
            self.fail(ex)
        try: 
            self.selection.calcPlotData([])
        except NotImplementedError as ex:
            self.fail(ex)

    def testIsMultipleScansSelected(self):
        result = self.selection.isMultipleScansSelected()
        self.assertEqual(result, False)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()