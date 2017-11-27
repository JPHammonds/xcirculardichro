'''
Created on Oct 27, 2017

@author: hammonds
'''
import unittest
from xcirculardichro.writer.writer import Writer


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testCreate(self):
        with self.assertRaises(TypeError):
            writer = Writer()

    def testWriter1Create(self):
        with self.assertRaises(TypeError):
            writer = TestWriter1()

    def testWriter2Create(self):
        writer = TestWriter2("myOutFile.txt")
        
        
class TestWriter1(Writer):
    def __init__(self):
        super(TestWriter1, self).__init__()
        
class TestWriter2(Writer):
    def __init__(self, outFileName):
        super(TestWriter2, self).__init__()
        self.outputFileName = outFileName
        
    def writeNode(self, dataFile):
        pass

    def writeNodes(self, dataFileNodes):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreate']
    unittest.main()