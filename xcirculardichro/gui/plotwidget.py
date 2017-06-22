'''
Created on May 17, 2017

@author: hammonds
'''

import PyQt4.QtGui as qtGui

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
        layout = qtGui.QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.switchPlot(1,1)
        self.plot(range(10), range(10))
        self.ax = None
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.show()
        
    def clear(self):
        plt.clf()
        
    def switchPlot(self, plotNum, numOfPlots):
        plotPerRow = math.ceil(math.sqrt(numOfPlots))
        self.figure.subplots_adjust(bottom=.1, left=0.1, right=0.9, top=0.9, wspace=.2, hspace=.2)
        self.ax = plt.subplot(plotPerRow, plotPerRow, plotNum)
        
    
    def plot(self, x, y):
        
        self.ax.hold(False)
        
        self.ax.plot(x, y)
        self.canvas.draw()
        
    def plot2(self, y):
        self.ax = self.figure.add_subplot(111)
        
        self.ax.hold(False)
        
        self.ax.plot(range(len(y)), y)
        self.canvas.draw()
        
    def setXlabel(self, label):
        self.ax.set_xlabel(label)
        
    def setYlabel(self, label):
        self.ax.set_ylabel(label)
        