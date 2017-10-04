'''
Created on Aug 29, 2017

@author: hammonds
'''
import unittest
from xcirculardichro.gui.dataselection.specdisplay import SpecDisplay
from PyQt5.QtWidgets import QApplication
import sys
import os
from spec2nexus.spec import SpecDataFile
from xcirculardichro.data.specfiledatanode import SpecFileDataNode
from xcirculardichro.data.datanode import DataNode
from xcirculardichro.gui.choices.nonlockinxmcdchoices import NonLockinXMCDChoices
from xcirculardichro.gui.choices.lockinxmcdchoices import LockinXMCDChoices
from xcirculardichro.gui.choices.undefinedchoices import UndefinedChoices

app = QApplication(sys.argv)

FLUORESCENCE_FILE = "Brian-Nick/Fluorescence/lineup"
FLUORESCENCE_FILE = "Brian-Nick/Transmission/lineup"
DATAPATH = 'DATAPATH'
QXDICHRO_SCAN = 'qxdichro'
QXSCAN_SCAN = 'qxscan'
QXDICHRO_NODES = ['37', '38', '39', '40', '41', '42', '45', '46', '49', '50', 
                  '51', '59', '66', '67', '70', '87', '88', '90', '91', '92',
                  '93', '97', '98', '99', '100', '113', '116'] 
INITIAL_NODE_LABELS = ['', '', '']
DEFAULT_XMCD_PLOT_LABELS = ['Energy', 'XAS', 'XMCD']
DEFAULT_NONLOCKIN_LABELS = ["Energy", "D+", "D-", "M+", "M-"]
DEFAULT_LOCKIN_LABELS = ['Energy', 'XAS', 'XMCD']

class TestSpecDisplay(unittest.TestCase):


    def setUp(self):
        self.specDisplay = SpecDisplay() 
        self.dataPath = os.environ.get(DATAPATH)
        specFileName1 = os.path.join(self.dataPath, FLUORESCENCE_FILE)
        try:
            self.specFile1 = SpecDataFile(specFileName1)
        except Exception as ex:
            self.fail(ex)
        specFileName2 = os.path.join(self.dataPath, FLUORESCENCE_FILE)
        try:
            self.specFile2 = SpecDataFile(specFileName2)
        except Exception as ex:
            self.fail(ex)
        
    def tearDown(self):
        pass


    def testMethodsExist(self):
        try:
            self.specDisplay.isMultipleScansSelected()
        except NotImplementedError as ex:
            self.fail(ex)
        try: 
            self.specDisplay.calcPlotData(None)
        except NotImplementedError as ex:
            self.fail(ex)
        try:
            self.specDisplay.getPlotAxisLabels()
        except NotImplementedError as ex:
            self.fail(ex)
#         try:
#             self.specDisplay.getDataLabels()
#         except NotImplementedError as ex:
#             self.fail(ex)
        try:
            self.specDisplay.getPlotAxisLabelsIndex()
        except NotImplementedError as ex:
            self.fail(ex)
        try:
            self.specDisplay.getSelectedScans()
        except NotImplementedError as ex:
            self.fail(ex)
        try:
            self.specDisplay.plotIndividualData()
        except NotImplementedError as ex:
            self.fail(ex)
        try:
            self.specDisplay.plotAverageData()
        except NotImplementedError as ex:
            self.fail(ex)
        try:
            self.specDisplay.setupDisplayWithSelectedNodes()
        except NotImplementedError as ex:
            self.fail(ex)

        pass
    
    def testIsMultipleScansSelected(self):
        result = self.specDisplay.isMultipleScansSelected()
        self.assertEqual(result, False)
        topNode = DataNode("/")
        specFileNode1 = SpecFileDataNode(self.specFile1, parent=topNode)
        specFileNode2 = SpecFileDataNode(self.specFile2, parent=topNode)
        specFileNode1.setChecked(True)
        specFileNode2.setChecked(True)
        selectedNodes = [specFileNode1,]
        self.specDisplay.setSelectedNodes(selectedNodes)
        result = self.specDisplay.isMultipleScansSelected()
        self.assertEqual(result, False)
        specFileNode1.setChecked(True)
        selectedNodes = [specFileNode1,specFileNode2]
        self.specDisplay.setSelectedNodes(selectedNodes)
        result = self.specDisplay.isMultipleScansSelected()
        self.assertEqual(result, False)
        specFileNode1.setChecked(True)
        result = self.specDisplay.isMultipleScansSelected()
        self.assertEqual(result, False)

    def testGetPlotAxisLabels(self):
        result = self.specDisplay.getPlotAxisLabels()
        self.assertEqual(result, UndefinedChoices.COUNTER_OPTS)
        topNode = DataNode("/")
        specFileNode1 = SpecFileDataNode(self.specFile1, parent=topNode)
        specFileNode2 = SpecFileDataNode(self.specFile1, parent=topNode)
        self.specDisplay.setSelectedNodes([specFileNode1])
        
        result = self.specDisplay.getPlotAxisLabels()
        self.assertEqual(result, UndefinedChoices.COUNTER_OPTS)
        typeIndex = self.specDisplay.typeSelector.getTypeIndexFromName(QXDICHRO_SCAN)
        self.specDisplay.typeSelector.setCurrentType(typeIndex)
        self.assertIsInstance(self.specDisplay.subChoices.choiceWidget, NonLockinXMCDChoices)
        result = self.specDisplay.getPlotAxisLabels()
        self.assertEqual(result, DEFAULT_XMCD_PLOT_LABELS)
#         result = self.specDisplay.getDataLabels()
#         self.assertEqual(result, DEFAULT_XMCD_PLOT_LABELS) 

        typeIndex = self.specDisplay.typeSelector.getTypeIndexFromName(QXSCAN_SCAN)
        self.specDisplay.typeSelector.setCurrentType(typeIndex)
        result = self.specDisplay.getPlotAxisLabels()
        self.assertIsInstance(self.specDisplay.subChoices.choiceWidget, LockinXMCDChoices)
        self.assertEqual(result, DEFAULT_XMCD_PLOT_LABELS)        
#         result = self.specDisplay.getDataLabels()
#         self.assertEqual(result, DEFAULT_XMCD_PLOT_LABELS) 
        

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()