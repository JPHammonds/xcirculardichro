'''
Created on Aug 28, 2017

@author: hammonds
'''
import unittest
from xcirculardichro.gui.xmcddatanavigator import XMCDDataNavigator
from xcirculardichro.data.datanode import DataNode
from PyQt5.Qt import QApplication
from PyQt5.QtTest import QSignalSpy
import PyQt5.QtWidgets as qtWidgets
import sys

TORSO = "Torso"
HEAD = "Head"
NECK = "Neck"
SHOULDER_RIGHT = "RightShoulder"
SHOULDER_LEFT = "LeftShoulder"
ARM_RIGHT = "RightArm"
ARM_LEFT = "LeftArm"
HAND_RIGHT = "RightHand"
HAND_LEFT = "LeftHand"
HIPS = "Hips"
LEG_LEFT = "LeftLeg"
LEG_RIGHT = "RightLeg"
FOOT_RIGHT = "RightFoot"
FOOT_LEFT = "LeftFoot"

TORSO_CHILDREN = [NECK, SHOULDER_RIGHT, SHOULDER_LEFT, HIPS]
HIPS_CHILDREN = [LEG_RIGHT, LEG_LEFT]

app = QApplication(sys.argv)

class Test(unittest.TestCase):


    def setUp(self):
        self.dataNavigator = XMCDDataNavigator()
        self.spyDataSelectionChanged= QSignalSpy(self.dataNavigator.dataSelectionChanged)
    def tearDown(self):
        pass


    def createNodesWithParents(self):
        self.torso = DataNode(TORSO)
        self.neck = DataNode(NECK, self.torso)
        self.head = DataNode(HEAD, self.neck)
        self.rightShoulder = DataNode(SHOULDER_RIGHT, self.torso)
        self.leftShoulder = DataNode(SHOULDER_LEFT, self.torso)
        self.rightArm = DataNode(ARM_RIGHT, self.rightShoulder)
        self.leftArm = DataNode(ARM_LEFT, self.leftShoulder)
        self.rightHand = DataNode(HAND_RIGHT, self.rightArm)
        self.leftHand = DataNode(HAND_LEFT, self.leftArm)
        self.hips  = DataNode(HIPS, self.torso)
        self.rightLeg = DataNode(LEG_RIGHT, self.hips)
        self.leftLeg = DataNode(LEG_LEFT, self.hips)
        self.rightFoot = DataNode(FOOT_RIGHT, self.rightLeg)
        self.leftFoot = DataNode(FOOT_LEFT, self.leftLeg)

    def testInit(self):
        self.assertEqual(self.dataNavigator.model().rowCount(),0)
        self.assertEqual(self.dataNavigator.rootNode().name(), "/")
        self.assertEqual(self.dataNavigator.view().selectionMode(),  
                         qtWidgets.QAbstractItemView.SingleSelection)
        self.assertEqual(len (self.spyDataSelectionChanged), 0)
        
    def testAddDataNode(self):
        self.dataNavigator.addDataNode(TORSO)
        self.assertEquals(self.dataNavigator.model().rowCount(), 1)
        self.assertEquals(self.dataNavigator.rootNode().childCount(), 1)
        self.assertEquals(self.dataNavigator.rootNode().child(0).name(), TORSO)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()