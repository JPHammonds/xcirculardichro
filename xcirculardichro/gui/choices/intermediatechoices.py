'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
from xcirculardichro.gui.choices.abstractchoices import AbstractChoices


class IntermediateChoices(AbstractChoices):
    
    PLOT_OPTIONS = ["Individual & Average Scan Data",
                "Individual Scan Data Only", 
                "Average Scan Data Only",
                "Individual and Normalized Data",
                "Normalized Data Only"]

    def __init__(self, parent=None):
        super(IntermediateChoices, self).__init__(parent=parent)
    
    def calcStepCorrectedData(self, data, preEdge=None, postEdge=None):
        xas = data[0]
        xmcd = data[1]
        xasCor = (xas-preEdge)/(postEdge-preEdge)
        xmcdCor = (xmcd)/(postEdge-preEdge)
        return [xasCor, xmcdCor]
        
    
    def plotIndividualData(self):
        '''
        Logical to return if individually selected data sets should be plotted
        '''
        if (str(self.plotDataChoice.currentText()) == self.PLOT_OPTIONS[0]) or \
            (str(self.plotDataChoice.currentText()) == self.PLOT_OPTIONS[1]) or \
            (str(self.plotDataChoice.currentText()) == self.PLOT_OPTIONS[3]):
            return True
        else:
            return False
        
    def plotNormalizedData(self):
        if (str(self.plotDataChoice.currentText()) == self.PLOT_OPTIONS[3]) or \
           (str(self.plotDataChoice.currentText()) == self.PLOT_OPTIONS[4]):
            return True
        else:
            return False
        
