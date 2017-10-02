'''
Created on Aug 26, 2017

@author: hammonds
'''
import unittest
from xcirculardichro.data.datanode import DataNode

MINUS_ONE = -1

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

class Test(unittest.TestCase):


    def setUp(self):
        pass

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

    def createNodesWithoutParents(self):
        self.torso = DataNode(TORSO)
        self.neck = DataNode(NECK)
        self.head = DataNode(HEAD)
        self.rightShoulder = DataNode(SHOULDER_RIGHT)
        self.leftShoulder = DataNode(SHOULDER_LEFT)
        self.rightArm = DataNode(ARM_RIGHT)
        self.leftArm = DataNode(ARM_LEFT)
        self.rightHand = DataNode(HAND_RIGHT)
        self.leftHand = DataNode(HAND_LEFT)
        self.hips  = DataNode(HIPS)
        self.rightLeg = DataNode(LEG_RIGHT)
        self.leftLeg = DataNode(LEG_LEFT)
        self.rightFoot = DataNode(FOOT_RIGHT)
        self.leftFoot = DataNode(FOOT_LEFT)
    
    def createNodeHeirachy(self):
        self.torso.addChild(self.neck)
        self.torso.addChild(self.rightShoulder)
        self.torso.addChild(self.leftShoulder)
        self.torso.addChild(self.hips)
        self.hips.addChild(self.rightLeg)
        self.hips.addChild(self.leftLeg)
        self.neck.addChild(self.head)
        self.rightShoulder.addChild(self.rightArm)
        self.leftShoulder.addChild(self.leftArm)
        self.leftArm.addChild(self.leftHand)
        self.rightArm.addChild(self.rightHand)
        self.leftLeg.addChild(self.leftFoot)
        self.rightLeg.addChild(self.rightFoot)
        
    def createBadNodeHeirachy(self):
        self.torso.addChild(self.neck)
        self.torso.addChild(self.rightShoulder)
        self.torso.addChild(self.leftShoulder)
        self.torso.addChild(self.hips)
        self.hips.addChild(self.rightLeg)
        self.hips.addChild(self.leftLeg)
        self.neck.addChild(self.head)
        self.rightShoulder.addChild(self.rightArm)
        self.rightShoulder.addChild(self.leftArm)
        self.leftArm.addChild(self.leftHand)
        self.rightArm.addChild(self.rightHand)
        self.leftLeg.addChild(self.leftFoot)
        self.leftLeg.addChild(self.rightFoot)
        
    def testNameCreatedWithParents(self):
        self.createNodesWithParents()
        self.assertEqual(self.torso.name(), TORSO)
        self.assertEqual(self.neck.name(), NECK)
        self.assertEqual(self.head.name(), HEAD)
        self.assertEqual(self.rightShoulder.name(), SHOULDER_RIGHT)
        self.assertEqual(self.leftShoulder.name(), SHOULDER_LEFT)
        self.assertEqual(self.rightArm.name(), ARM_RIGHT)
        self.assertEqual(self.leftArm.name(), ARM_LEFT)
        self.assertEqual(self.rightHand.name(), HAND_RIGHT)
        self.assertEqual(self.leftHand.name(), HAND_LEFT)
        self.assertEqual(self.hips.name(), HIPS)
        self.assertEqual(self.leftLeg.name(), LEG_LEFT)
        self.assertEqual(self.rightLeg.name(), LEG_RIGHT)
        self.assertEqual(self.leftFoot.name(), FOOT_LEFT)
        self.assertEqual(self.rightFoot.name(), FOOT_RIGHT)
        
    def testNameCreatedWithoutParents(self):
        self.createNodesWithoutParents()
        self.assertEqual(self.torso.name(), TORSO)
        self.assertEqual(self.neck.name(), NECK)
        self.assertEqual(self.head.name(), HEAD)
        self.assertEqual(self.rightShoulder.name(), SHOULDER_RIGHT)
        self.assertEqual(self.leftShoulder.name(), SHOULDER_LEFT)
        self.assertEqual(self.rightArm.name(), ARM_RIGHT)
        self.assertEqual(self.leftArm.name(), ARM_LEFT)
        self.assertEqual(self.rightHand.name(), HAND_RIGHT)
        self.assertEqual(self.leftHand.name(), HAND_LEFT)
        self.assertEqual(self.hips.name(), HIPS)
        self.assertEqual(self.leftLeg.name(), LEG_LEFT)
        self.assertEqual(self.rightLeg.name(), LEG_RIGHT)
        self.assertEqual(self.leftFoot.name(), FOOT_LEFT)
        self.assertEqual(self.rightFoot.name(), FOOT_RIGHT)
    
    def testChildCountCreatedWithParents(self):
        self.createNodesWithParents()
        self.assertEqual(self.torso.childCount(), len(TORSO_CHILDREN))
        self.assertEqual(self.hips.childCount(), len(HIPS_CHILDREN))
        self.assertEqual(self.neck.childCount(), 1)
        self.assertEqual(self.head.childCount(), 0)
        self.assertEqual(self.rightArm.childCount(), 1)
        self.assertEqual(self.rightHand.childCount(), 0)
        self.assertEqual(self.leftArm.childCount(), 1)
        self.assertEqual(self.leftHand.childCount(), 0)
        self.assertEqual(self.rightLeg.childCount(), 1)
        self.assertEqual(self.rightFoot.childCount(), 0)
        self.assertEqual(self.leftLeg.childCount(), 1)
        self.assertEqual(self.leftFoot.childCount(), 0)

        #TODO setup so that multiple parents cannot reference a child
        # now create Hierarchy
#         self.createNodeHeirachy()
#         self.assertEqual(self.torso.childCount(), len(TORSO_CHILDREN))
#         self.assertEqual(self.hips.childCount(), len(HIPS_CHILDREN))
#         self.assertEqual(self.neck.childCount(), 1)
#         self.assertEqual(self.head.childCount(), 0)
#         self.assertEqual(self.rightArm.childCount(), 1)
#         self.assertEqual(self.rightHand.childCount(), 0)
#         self.assertEqual(self.leftArm.childCount(), 1)
#         self.assertEqual(self.leftHand.childCount(), 0)
#         self.assertEqual(self.rightLeg.childCount(), 1)
#         self.assertEqual(self.rightFoot.childCount(), 0)
#         self.assertEqual(self.leftLeg.childCount(), 1)
#         self.assertEqual(self.leftFoot.childCount(), 0)
        
        
    def testChildCountCreatedWithoutParents(self):
        self.createNodesWithoutParents()
        self.assertEqual(self.torso.childCount(), 0)
        self.assertEqual(self.hips.childCount(), 0)
        self.assertEqual(self.neck.childCount(), 0)
        self.assertEqual(self.head.childCount(), 0)
        self.assertEqual(self.rightArm.childCount(), 0)
        self.assertEqual(self.rightHand.childCount(), 0)
        self.assertEqual(self.leftArm.childCount(), 0)
        self.assertEqual(self.leftHand.childCount(), 0)
        self.assertEqual(self.rightLeg.childCount(), 0)
        self.assertEqual(self.rightFoot.childCount(), 0)
        self.assertEqual(self.leftLeg.childCount(), 0)
        self.assertEqual(self.leftFoot.childCount(), 0)

        # now create Hierarchy
        self.createNodeHeirachy()
        self.assertEqual(self.torso.childCount(), len(TORSO_CHILDREN))
        self.assertEqual(self.hips.childCount(), len(HIPS_CHILDREN))
        self.assertEqual(self.neck.childCount(), 1)
        self.assertEqual(self.head.childCount(), 0)
        self.assertEqual(self.rightArm.childCount(), 1)
        self.assertEqual(self.rightHand.childCount(), 0)
        self.assertEqual(self.leftArm.childCount(), 1)
        self.assertEqual(self.leftHand.childCount(), 0)
        self.assertEqual(self.rightLeg.childCount(), 1)
        self.assertEqual(self.rightFoot.childCount(), 0)
        self.assertEqual(self.leftLeg.childCount(), 1)
        self.assertEqual(self.leftFoot.childCount(), 0)

    def testChild(self):
        self.createNodesWithParents()
        for childRow in range(self.torso.childCount()):
            self.assertEquals(self.torso.child(childRow).name(), 
                              TORSO_CHILDREN[childRow])
        self.assertEquals(self.torso.child(MINUS_ONE).name(), 
                          HIPS)
        with self.assertRaises(IndexError): 
            print(self.torso.child(MINUS_ONE*(len(TORSO_CHILDREN)+1)))
        with self.assertRaises(IndexError): 
            self.torso.child(len(TORSO_CHILDREN))

        for childRow in range(self.hips.childCount()):
            self.assertEquals(self.hips.child(childRow).name(), 
                              HIPS_CHILDREN[childRow])
        self.assertEquals(self.torso.child(MINUS_ONE).name(), 
                          HIPS)
        with self.assertRaises(IndexError): 
            print(self.torso.child(MINUS_ONE*(len(TORSO_CHILDREN)+1)))
        with self.assertRaises(IndexError): 
            self.torso.child(len(TORSO_CHILDREN))
        self.assertEquals(self.neck.child(0).name(), 
                          HEAD)
        self.assertEquals(self.neck.child(-1).name(), 
                          HEAD)
        with self.assertRaises(IndexError): 
            self.neck.child(1)
        with self.assertRaises(IndexError): 
            self.head.child(0)
        
    def testParent(self):
        self.createNodesWithParents()
        self.assertIsNone(self.torso.parent())
        for childRow in range(self.torso.childCount()):
            self.assertEquals(self.torso.child(childRow).parent(), 
                              self.torso)
        self.assertEquals(self.hips.parent(), self.torso)
        for childRow in range(self.hips.childCount()):
            self.assertEquals(self.hips.child(childRow).parent(), 
                              self.hips)
        self.assertEquals(self.head.parent(), self.neck)
        self.assertEquals(self.rightHand.parent(), self.rightArm)
        self.assertEquals(self.leftHand.parent(), self.leftArm)
        self.assertEquals(self.rightFoot.parent(), self.rightLeg)
        self.assertEquals(self.leftFoot.parent(), self.leftLeg)
        
    def testRow(self):
        self.createNodesWithParents()
        for childRow in range(len(TORSO_CHILDREN)):
            self.assertEquals(self.torso.child(childRow).row(), 
                              childRow)
        
        for childRow in range(len(HIPS_CHILDREN)):
            self.assertEquals(self.hips.child(childRow).row(), 
                              childRow)
        for childRow in range(self.torso.childCount()):
            self.assertEquals(self.torso.child(childRow).row(), 
                              childRow)
        self.assertEqual(self.head.row(), 0)
        self.assertEqual(self.leftArm.row(), 0)
        self.assertEqual(self.rightArm.row(), 0)
        self.assertEqual(self.leftFoot.row(), 0)
        self.assertEqual(self.rightFoot.row(), 0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()