'''
Created on May 17, 2017

@author: hammonds
'''

import PyQt4.QtGui as qtGui
import logging
logger = logging.getLogger(__name__)

# import matplotlib
# matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
import math
'''
Start from http://stackoverflow.com/questions/12459811/how-to-embed-matplotib-in-pyqt-for-dummies
'''

class PlotWidget(qtGui.QDialog):
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)
        logger.debug("Entering")
        layout = qtGui.QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        #self.switchPlot(1,1)
        self.clear()
        self.plotAx1(range(10), range(10))
        self.ax = None
        self.ax2 = None
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.setMinimumSize(800, 600)
        self.show()
        
    def clear(self):
        logger.debug("Entering")
        plt.clf()
        self.ax = plt.subplot(1, 1, 1)
        self.ax2 = self.ax.twinx()
        self.ax2 = plt.subplot(1, 1, 1)
        
#     def switchPlot(self, plotNum, numOfPlots):
#         logger.debug("Entering %d, %d" % (plotNum, numOfPlots))
#         plotPerRow = math.ceil(math.sqrt(numOfPlots))
#         self.figure.subplots_adjust(bottom=.1, left=0.1, right=0.9, top=0.9, wspace=.2, hspace=.2)
#         self.ax = plt.subplot(1, 1, 1)
        
    
    def plotAx1(self, x, y):
        logger.debug("Entering %s" % ((x,y),))
        
        self.ax.plot(x, y)
        
    def plotAx1Average(self, x, y):
        logger.debug("Entering %s" % ((x,y),))
        
        line, = self.ax.plot(x, y)
        plt.setp(line, linewidth=2)
        
    def plotAx2(self, x, y):
        logger.debug("Entering %s" % ((x,y),))
        
        self.ax2.plot(x, y)

    def plotAx2Average(self, x, y):
        logger.debug("Entering %s" % ((x,y),))
        
        line, = self.ax.plot(x, y)
        plt.setp(line, linewidth=2)
        
    def plotDraw(self):
        self.canvas.draw()

                
    def setXLabel(self, label):
        logger.debug("Entering %s" % label)
        self.ax.set_xlabel(label)
        
    def setYLabel(self, label):
        logger.debug("Entering %s" % label) 
        self.ax.set_ylabel(label)
        
    def setY2Label(self, label):
        logger.debug("Entering %s" % label)
        self.ax2.set_ylabel(label)
        