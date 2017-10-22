import numpy as np
import scipy.signal
from PyQt5 import QtGui, QtCore, QtWidgets
import pyqtgraph as pg 
import sys
import time


class Prototype(QtWidgets.QWidget):

    def __init__(self):
        super(Prototype, self).__init__() # Initializes the base class QMainWindow
        
        # Refresh rate
        self.timerDelay = 100

        # BOARD initialization
        self.BOARD = np.zeros(shape=(20,20), dtype=np.bool)
        self.BOARD[[1,1,2,3,3,4,4,4,4], [2,5,6,2,6,3,4,5,6]] = True # The Lightweight Spaceship
        #self.BOARD[[1,2,3,3,3,2,1,1], [1,1,1,2,3,3,3,4]] = True

        # Initializes the GUI widgets and layout
        self.setupGUI()

        # Starts propagation after 3 seconds
        QtCore.QTimer.singleShot(3000, lambda: self.displayTimer.start(self.timerDelay))
    
    # WIDGETS AND LAYOUT ----------------------------------------------------------------------------------------------
    def setupGUI(self):

        # Sets the name, incon and size of the main window
        self.setWindowTitle('The Game Of Life') 
        self.setWindowIcon(QtGui.QIcon('Conway.jpg'))
        self.resize(800,800)

        # GraphicView
        self.Image = pg.ImageItem()
        self.Plot = pg.PlotWidget(title="MAP", labels={"left":"Cell number", "bottom":"Depth"})
        self.Plot.hideAxis("bottom")
        self.Plot.hideAxis("left")
        self.Plot.addItem(self.Image)
        
        self.Image.setImage(image=np.transpose(np.flip(self.BOARD, axis=0)))

        # Build lookup table
        lut = np.zeros((256,3), dtype=np.ubyte)
        lut[:10,:] = 50
        lut[10:,0] = 255
        lut[:,1] = np.arange(0,256)
        self.Image.setLookupTable(lut, update=True)

        # Instanciates the layout objects and initialises the first one
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.Plot, 0, 0, 5, 5)

        # Add Timer for displaying and saving data
        self.displayTimer = QtCore.QTimer()
        self.displayTimer.timeout.connect(self.propagate)

        # Display the interface on the screen
        self.show()

        return


    def takeOneStep(self, BOARD):
        
        # Makes sure BOARD is a boolean matrix
        BOARD = BOARD.astype(np.bool)
        
        # This convolution kernel counts how many neighbors a cell has
        kernel = np.ones(shape=(3,3), dtype=np.int)
        kernel[1,1] = 0

        # Map of number of neighbors for each cell
        neighbors = scipy.signal.convolve2d(BOARD, kernel, mode="same")
        
        # Computing condition maps
        V2 = np.array((neighbors==2), dtype=np.bool)
        V3 = np.array((neighbors==3), dtype=np.bool)
        
        # Computing the Newborns map
        Newborns = np.invert(np.bitwise_or(BOARD, np.invert(V3)))

        # Computing the Survivors map
        Survivors = np.bitwise_and(BOARD, np.bitwise_or(V2, V3))

        # Computing the NewBOARD
        NewBOARD = Newborns + Survivors
        
        return NewBOARD

    def updateImage(self):

        self.Image.setImage(image=np.transpose(np.flip(self.BOARD, axis=0)))

    def propagate(self):

        self.BOARD = self.takeOneStep(self.BOARD)
        self.updateImage()



def run():
    global app
    app = QtWidgets.QApplication(sys.argv)   # Every PyQt application must create an application object
    gui = Prototype()                        # Create an object "GuiManager"
    sys.exit(app.exec_())                    # Enter the main loop of the application


if __name__ == '__main__':
    run()

