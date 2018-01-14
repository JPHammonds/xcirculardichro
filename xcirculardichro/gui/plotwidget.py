'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''

import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
import PyQt5.QtGui as qtGui
import logging
import numpy as np
from xcirculardichro import METHOD_ENTER_STR, METHOD_EXIT_STR

logger = logging.getLogger(__name__)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

logger.setLevel(logging.DEBUG)
'''
Start from http://stackoverflow.com/questions/12459811/how-to-embed-matplotib-in-pyqt-for-dummies
'''

class PlotWidget(qtWidgets.QDialog):

    leftSelectionChanged = qtCore.pyqtSignal(str, name="leftSelectionChanged")
    rightSelectionChanged = qtCore.pyqtSignal(str, name="rightSelectionChanged")
    
    
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)
        logger.debug("Entering")
        layout = qtWidgets.QVBoxLayout()
        self.buttonPressId = None
        self.buttonReleaseId = None
        self.keyPressId = None
        self.keyReleaseId = None
        self.pickId = None
        self.figureEnterId = None
        self.figureLeaveId = None
        self.axesEnterId = None
        self.axesLeaveId = None
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFocusPolicy( qtCore.Qt.ClickFocus )
        self.canvas.setFocus()

        self.selector1 = {}
        self.selector2 = {}
        #self.switchPlot(1,1)
        self.clear()
        self.plotAx1(range(10), range(10), "line")
#         self.ax = None
#         self.ax2 = None
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.setMinimumSize(400, 300)
        self.show()
        
    def applyPickPoints(self, preEdgePoints, postEdgePoints):
        logger.debug(METHOD_ENTER_STR %((preEdgePoints, postEdgePoints),))
        print (METHOD_ENTER_STR % ((preEdgePoints, postEdgePoints),))
        currentAxis = self.currentPlotAxis()
        key1List = list(self.selector1.keys())
        key2List = list(self.selector2.keys())
        if currentAxis == 0:
            print("Axis = 0")
            if len(key1List)>0:
                key = key1List[-1]
                self.selector1[key].applyPickPoints(preEdgePoints, postEdgePoints)
        else:
            print("Axis = 0")
            if len(key2List)>0:
                key = key2List[-1]
                self.selector2[key].applyPickPoints(preEdgePoints, postEdgePoints)
        logger.debug(METHOD_EXIT_STR)
        
    def clear(self):
        logger.debug("Entering")
        plt.clf()
        self.canvas.draw()
        self.disconnectSignals()
        self.ax = plt.subplot(1, 1, 1)
        self.ax2 = self.ax.twinx()
        self.ax3 = self.ax.twinx()
        self.ax4 = self.ax.twinx()
        self.ax.cla()
        self.ax2.cla()
        self.ax3.cla()
        self.ax4.cla()
        self.figure.subplots_adjust(left=0.2,right=0.75)
        self.ax3.spines['right'].set_position( ('axes',-0.2))
        self.ax4.spines['right'].set_position(  ('axes',1.2))
        self.connectSignals()
        #self.ax2 = plt.subplot(1, 1, 1)
        
    def connectSignals(self):
        logger.debug(METHOD_ENTER_STR)
# #         self.buttonPressId = self.canvas.mpl_connect('button_press_event', self.onButtonPress)
# #         self.buttonReleaseId = self.canvas.mpl_connect('button_release_event', self.onButtonRelease)
        self.keyPressId = self.canvas.mpl_connect('key_press_event', self.onKeyPress)
#         self.keyReleaseId = self.canvas.mpl_connect('key_release_event', self.onKeyRelease)
        self.pickId = self.canvas.mpl_connect('pick_event', self.onPick)
#         self.figureEnterId = self.canvas.mpl_connect('figure_enter_event', self.onFigureEnter)
#         self.figureLeaveId = self.canvas.mpl_connect('figure_leave_event', self.onFigureLeave)
#         self.axesEnterId = self.canvas.mpl_connect('axes_enter_event', self.onAxesEnter)
#         self.axesLeaveId = self.canvas.mpl_connect('axes_leave_event', self.onAxesLeave)
        
    def currentPlotAxis(self):
        logger.debug(METHOD_ENTER_STR)
        currentAxis = 0
        if self.ax2.get_zorder() > self.ax.get_zorder():
            currentAxis = 1
        else:
            currentAxis = 0
        return currentAxis
    
    def disconnectSignals(self):
        self.canvas.mpl_disconnect(self.buttonPressId)
        self.canvas.mpl_disconnect(self.buttonReleaseId)
        self.canvas.mpl_disconnect(self.keyPressId)
        self.canvas.mpl_disconnect(self.keyReleaseId)
#        self.canvas.mpl_disconnect(self.pickId)
        self.canvas.mpl_disconnect(self.figureEnterId)
        self.canvas.mpl_disconnect(self.figureLeaveId)
        self.canvas.mpl_disconnect(self.axesEnterId)
        self.canvas.mpl_disconnect(self.axesLeaveId)
        
#     def switchPlot(self, plotNum, numOfPlots):
#         logger.debug("Entering %d, %d" % (plotNum, numOfPlots))
#         plotPerRow = math.ceil(math.sqrt(numOfPlots))
#         self.figure.subplots_adjust(bottom=.1, left=0.1, right=0.9, top=0.9, wspace=.2, hspace=.2)
#         self.ax = plt.subplot(1, 1, 1)
        
    def getLeftSelectionIndexes(self, label):
        '''
        retrieve array indices of the Highlighted Selection
        '''
        logger.debug(METHOD_ENTER_STR % label)
        
        selector = self.getSelectorFromKey(label)
        indices = selector.getLeftSelectionIndexes() 
        
        return indices
        
    def getLeftSelectionAverage(self, label):
        '''
        retrieve average value of the Highlighted Selection
        '''
        logger.debug(METHOD_ENTER_STR % label)
        selector = self.getSelectorFromKey(label)
        averageValue = selector.getLeftSelectionAverage()
        
        return averageValue
        
    def getRightSelectionIndexes(self, label):
        '''
        retrieve array indices of the Highlighted Selection
        '''
        logger.debug(METHOD_ENTER_STR % label)
        selector = self.getSelectorFromKey(label)
        indices = selector.getRightSelectionIndexes() 

        return indices
        
    def getRightSelectionAverage(self, label):
        '''
        retrieve average value of the Highlighted Selection
        '''
        logger.debug(METHOD_ENTER_STR % label)
        selector = self.getSelectorFromKey(label)
        averageValue = selector.getRightSelectionAverage()
        
        return averageValue
        
        
    def getSelectorFromKey(self, key):
        selector1Keys = list(self.selector1.keys())
        logger.debug("selector1Keys: %s" % selector1Keys )
        selector2Keys = list(self.selector2.keys())
        logger.debug("selector1Keys: %s" % selector1Keys )
        if key in selector1Keys:
            return self.selector1[key]
        elif key in selector2Keys:
            return self.selector2[key]
        else:
            raise IndexError(key)
        
    def handleLeftSelectionChanged(self, label):
        '''
        Catch when a highlight selection changes and emit a signal from this 
        class to the caller of this class
        '''
        logger.debug(METHOD_ENTER_STR % label)
        self.leftSelectionChanged[str].emit(label)
        
    def handleRightSelectionChanged(self, label):
        '''
        Catch when a highlight selection changes and emit a signal from this 
        class to the caller of this class
        '''
        logger.debug(METHOD_ENTER_STR % label)
        self.rightSelectionChanged[str].emit(label)

    def onButtonPress(self, event):
        '''
        Handle generic button press events
        '''
        logger.debug(METHOD_ENTER_STR % dir(event))

    def onButtonRelease(self, event):
        '''
        Handle generic button release events
        '''
        logger.debug(METHOD_ENTER_STR % event)
    
    def onKeyPress(self, event):
        '''
        Handle key press events
        '''
        logger.debug(METHOD_ENTER_STR % event)
        logger.debug("Key: %s " % event.key)
        if event.key == 'l':
            HighlightSelected.setSelectLeft()
        elif event.key == 'r':
            HighlightSelected.setSelectRight()
        elif event.key == '+':
            HighlightSelected.setSelectOn()
        elif event.key == '-':
            HighlightSelected.setSelectOff()
        elif event.key == 't':
            logger.debug("ax.zorder %f, ax2.zorder %f" % 
                         ( self.ax.get_zorder(),self.ax2.get_zorder()))
            if self.ax.get_zorder() == 0:
                logger.debug("Setting for axis 2")
                self.ax.set_zorder(0.1)
                self.ax2.set_zorder(0)
                self.ax2.patch.set_visible(True)
                self.ax.patch.set_visible(False)
            else:
                logger.debug("Setting for axis 1")
                self.ax.set_zorder(0)
                self.ax2.set_zorder(0.1)
                self.ax2.patch.set_visible(False)
                self.ax.patch.set_visible(True)
            
    def onKeyRelease(self, event):
        logger.debug(METHOD_ENTER_STR % event)
    
    def onPick(self, event):
        logger.debug(METHOD_ENTER_STR % event)
        logger.debug("dir(event) %s" % dir(event))
        logger.debug("name %s" % event.name)
        logger.debug("ind %s" % event.ind)
        logger.debug("artist %s" %event.artist)
        logger.debug("canvas %s" % event.canvas)
        logger.debug("guiEvent %s" % event.guiEvent)
        logger.debug("mouseEvent %s" % event.mouseevent)
        artist = event.artist
#         if isinstance(artist, Line2D):
#                 logger.debug("Selected from %s" % artist.name())
        
    def onFigureEnter(self, event):
        logger.debug(METHOD_ENTER_STR % event)
        self.canvas.setFocusPolicy(qtCore.Qt.ClickFocus)
        self.canvas
        
    def onFigureLeave(self, event):
        logger.debug(METHOD_ENTER_STR % event)
        
    def onAxesEnter(self, event):
        logger.debug(METHOD_ENTER_STR % event)
        
    def onAxesLeave(self, event):
        logger.debug(METHOD_ENTER_STR % event)
        
    
    def plotAx1(self, x, y, label):
        logger.debug(METHOD_ENTER_STR % ((label, x,y),))
        
        line, = self.ax.plot(x, y, label=label, picker=True, pickradius=6)
        self.selector1[label] = HighlightSelected(line, parent=self)
        self.selector1[label].rightSelectionChanged[str].connect(self.handleRightSelectionChanged)
        self.selector1[label].leftSelectionChanged[str].connect(self.handleLeftSelectionChanged)
        
    def plotAx1Average(self, x, y, label):
        logger.debug(METHOD_ENTER_STR % ((x,y),))
        
        line, = self.ax.plot(x, y, label=label, picker=True, pickradius=6)
        plt.setp(line, linewidth=2)
        self.selector1[label] = HighlightSelected(line, parent=self)
        self.selector1[label].rightSelectionChanged[str].connect(self.handleRightSelectionChanged)
        self.selector1[label].leftSelectionChanged[str].connect(self.handleLeftSelectionChanged)
        
    def plotAx3Corrected(self, x, y, label):
        logger.debug(METHOD_ENTER_STR % ((x,y),))
        line, = self.ax3.plot(x,y, label=label, linewidth=2)
        #line.setp( line, linewidth = 2)
        
    def plotAx2(self, x, y, label):
        logger.debug(METHOD_ENTER_STR % ((label, x,y),))
        
        line, = self.ax2.plot(x, y, label=label, 
                      linestyle=":", picker=True, pickradius=6)
        self.selector2[label] = HighlightSelected(line, parent=self)
        self.selector2[label].rightSelectionChanged[str].connect(self.handleRightSelectionChanged)
        self.selector2[label].leftSelectionChanged[str].connect(self.handleLeftSelectionChanged)
        
    def plotAx2Average(self, x, y, label):
        logger.debug(METHOD_ENTER_STR % ((x,y),))
        
        line, = self.ax2.plot(x, y, label=label, 
                              linestyle=":", linewidth=2, 
                              picker=True, pickradius=6)
        self.selector2[label] = HighlightSelected(line, parent=self)
        self.selector2[label].rightSelectionChanged[str].connect(self.handleRightSelectionChanged)
        self.selector2[label].leftSelectionChanged[str].connect(self.handleLeftSelectionChanged)
        
    def plotAx4Corrected(self, x, y, label):
        logger.debug(METHOD_ENTER_STR % ((x,y),))
        line, = self.ax4.plot(x,y, label=label, linestyle=":", linewidth=2)
        
    def plotDraw(self):
        self.ax.legend(loc=2)
        self.ax2.legend(loc=1)
        self.ax3.legend(loc=3)
        self.ax4.legend(loc=4)
        self.canvas.draw()
        
    @qtCore.pyqtSlot(int)
    def setPointSelectionAxis(self, axis):
        logger.debug(METHOD_ENTER_STR % axis)
        if axis == 0:
            logger.debug("Setting for axis 1")
            self.ax.set_zorder(0.1)
            self.ax.patch.set_visible(False)
            self.ax2.set_zorder(0)
            self.ax2.patch.set_visible(True)
        elif axis == 1:
            logger.debug("Setting for axis 2")
            self.ax.set_zorder(0)
            self.ax.patch.set_visible(True)
            self.ax2.set_zorder(0.1)
            self.ax2.patch.set_visible(False)
            
    @qtCore.pyqtSlot(int)
    def setPointSelectionType(self, selectionType):
        logger.debug(METHOD_ENTER_STR % selectionType)
        if selectionType == 0:
            HighlightSelected.setSelectLeft()
        else:
            HighlightSelected.setSelectRight()
            
    def setXLabel(self, label):
        logger.debug("Entering %s" % label)
        self.ax.set_xlabel(label)
        
    def setYLabel(self, label):
        logger.debug("Entering %s" % label) 
        self.ax.set_ylabel(label)
        
    def setY2Label(self, label):
        logger.debug("Entering %s" % label)
        self.ax2.set_ylabel(label)

    def sizeHint(self):
        return qtCore.QSize(800, 600)
# used code from https://matplotlib.org/api/lines_api.html
import matplotlib.lines as lines
class HighlightSelected(lines.VertexSelector, qtCore.QObject):
    # Class members
    selectOn = True
    selectLeft = True
    leftSelectionChanged = qtCore.pyqtSignal(str, name="leftSelectionChanged")
    rightSelectionChanged = qtCore.pyqtSignal(str, name="rightSelectionChanged")
    
    def __init__(self, line, fmt='ro', fmt2='bo', parent=None, **kwargs):
        logger.debug(METHOD_ENTER_STR % "HighlightSelected.__init__")
        lines.VertexSelector.__init__(self,line, **kwargs)
        qtCore.QObject.__init__(self, parent=parent)
        self.fmt = fmt
        self.fmt2 = fmt2
        self.markersLeft, = self.axes.plot([], [], fmt, **kwargs)
        self.markersRight, = self.axes.plot([], [], fmt2, **kwargs)
        self.averageLeft, = self.axes.plot([], [], **kwargs)
        self.averageRight, = self.axes.plot([], [], **kwargs)
        self.indLeft = set()
        self.indRight = set()
        self.leftAverageValue = 0.0
        self.rightAverageValue = 0.0
        
    
    def applyPickPoints(self, preEdgePoints, postEdgePoints):
        logger.debug(METHOD_ENTER_STR)
        print (METHOD_ENTER_STR % ((preEdgePoints, postEdgePoints, self.line._label),))
        self.indLeft = set(preEdgePoints)
        self.indRight = set(postEdgePoints)
        xsAll, ysAll = self.line.get_data()

        try:
            xs = xsAll[preEdgePoints]
            ys = ysAll[preEdgePoints]
        except IndexError as ex:
            return
        print ((xs, ys))
        if len(xs) > 1:
            print("Setting left")
            self.markersLeft.set_data(xs, ys)    
            self.leftAverageValue = np.sum(ys)/len(ys)
            yAverage = self.leftAverageValue * np.ones(len(ys))
            self.averageLeft.set_data(xs, yAverage)
            self.leftSelectionChanged.emit(str(self.line._label))
        
        xs = xsAll[postEdgePoints]
        ys = ysAll[postEdgePoints]
        print ((xs, ys))
        if len(xs) > 1:
            print("Setting right")
            self.markersRight.set_data(xs, ys)
            self.rightAverageValue = np.sum(ys)/len(ys)
            yAverage = self.rightAverageValue * np.ones(len(ys))
            self.averageRight.set_data(xs, yAverage)
            self.rightSelectionChanged.emit(str(self.line._label))
        self.canvas.draw()
        
    def getLeftSelectionIndexes(self):
        '''
        retrieve array indices of the Highlighted Selection
        '''
        logger.debug(METHOD_ENTER_STR % self.indLeft)
        indices = self.indLeft 
        
        return indices
        
    def getLeftSelectionAverage(self):
        '''
        retrieve average value of the Highlighted Selection
        '''
        logger.debug(METHOD_ENTER_STR % self.leftAverageValue)
        return self.leftAverageValue
        
    def getRightSelectionIndexes(self):
        '''
        retrieve array indices of the Highlighted Selection
        '''
        logger.debug(METHOD_ENTER_STR % self.indRight)
        return self.indRight
        
    def getRightSelectionAverage(self):
        '''
        retrieve average value of the Highlighted Selection
        '''
        logger.debug(METHOD_ENTER_STR % self.rightAverageValue)
        return self.rightAverageValue
        
        
    def onpick(self, event):
        if event.artist is not self.line: 
            return
        if HighlightSelected.selectOn:
            for i in event.ind:
                if HighlightSelected.selectLeft:
                    if i in self.indLeft:
                        self.indLeft.remove(i)
                    else:
                        self.indLeft.add(i)
                    ind = list(self.indLeft)
                    ind.sort()
                    xdata, ydata = self.line.get_data()
                    self.process_selected(ind, xdata[ind], ydata[ind])
                else:
                    if i in self.indRight:
                        self.indRight.remove(i)
                    else:
                        self.indRight.add(i)
                    ind = list(self.indRight)
                    ind.sort()
                    xdata, ydata = self.line.get_data()
                    self.process_selected(ind, xdata[ind], ydata[ind])
                
        
    def process_selected(self, ind, xs, ys):
        logger.debug(METHOD_ENTER_STR %  "HighlightSelected.process_selected")
        logger.debug("input params (ind, xs, ys) = (%s, %s, %s)" % (ind, xs,ys))
        if HighlightSelected.selectOn:
            if HighlightSelected.selectLeft:
                self.markersLeft.set_data(xs, ys)
                self.leftAverageValue = np.sum(ys)/len(ys)
                yAverage = self.leftAverageValue * np.ones(len(ys))
                self.averageLeft.set_data(xs, yAverage)
                self.leftSelectionChanged.emit(str(self.line._label))
            else:
                self.markersRight.set_data(xs, ys)
                self.rightAverageValue = np.sum(ys)/len(ys)
                yAverage = self.rightAverageValue * np.ones(len(ys))
                self.averageRight.set_data(xs, yAverage)
                self.rightSelectionChanged.emit(str(self.line._label))
        self.canvas.draw()
    
    @staticmethod
    def setSelectOn():
        HighlightSelected.selectOn = True
        
    @staticmethod
    def setSelectOff():
        HighlightSelected.selectOn = False
        
    @staticmethod
    def setSelectLeft():
        HighlightSelected.selectLeft = True
        
    @staticmethod
    def setSelectRight():
        HighlightSelected.selectLeft = False
    