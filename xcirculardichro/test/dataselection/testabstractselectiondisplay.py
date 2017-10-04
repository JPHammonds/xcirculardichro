'''
Created on Aug 29, 2017

@author: hammonds
'''
import unittest
from xcirculardichro.gui.dataselection.AbstractSelectionDisplay import AbstractSelectionDisplay
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

class TestWithAbstractClass(unittest.TestCase):


    def setUp(self):
        self._display = AbstractSelectionDisplay()
        self._display1 = TestSubClassWithMethod()

    def tearDown(self):
        pass



    def testSetupWithSelectedFromNodes(self):
        with self.assertRaises(NotImplementedError):
            self._display.setupDisplayWithSelectedNodes()
        try:
            self._display1.setupDisplayWithSelectedNodes()
        except NotImplementedError:
            self.fail("Test subclass implements simple override, should work")
            
class TestSubClassWithMethod(AbstractSelectionDisplay):
    
    def setupDisplayWithSelectedNodes(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()