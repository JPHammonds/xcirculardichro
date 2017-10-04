'''
Created on Aug 21, 2017

@author: hammonds
'''
import unittest
from xcirculardichro.test.data.testdatanode import TestDataNode
from xcirculardichro.test.dataselection.testabstractselectiondisplay import TestWithAbstractClass
from xcirculardichro.test.dataselection.testabstractselectiondisplay import TestSubClassWithMethod


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDataNode())
    suite.addTest(TestWithAbstractClass())
    suite.addTest(TestSubClassWithMethod())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)