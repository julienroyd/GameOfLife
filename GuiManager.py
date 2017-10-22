import numpy as np
import time
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import pyqtgraph as pg 

from GameOfLife import GameOfLife


# GUI MANAGER
class GuiManager(QtWidgets.QWidget):

    def __init__(self):
        super(GuiManager, self).__init__() # Initializes the base class QMainWindow
        
        # Instanciates a GameOfLife object
        self.game = GameOfLife()

        # Initializes the GUI widgets and layout
        self.setupGUI()
    
    # WIDGETS AND LAYOUT ----------------------------------------------------------------------------------------------
    def setupGUI(self):

        # Sets the name, incon and size of the main window
        self.setWindowTitle('The Game Of Life') 
        self.setWindowIcon(QtGui.QIcon('Conway.jpg'))
        self.resize(1000,800)

        # Creates the buttons' size policy
        sizePolicyBtn = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        sizePolicyBtn.setHorizontalStretch(0)
        sizePolicyBtn.setVerticalStretch(0)
        
        # Start button
        self.StartBtn = QtGui.QPushButton("Start")
        sizePolicyBtn.setHeightForWidth(self.StartBtn.sizePolicy().hasHeightForWidth())
        self.StartBtn.setSizePolicy(sizePolicyBtn)
        self.StartBtn.setStyleSheet("background-color: green; color: black; font-size: 32px; font: bold")
        self.StartBtn.clicked.connect(self.start)
        self.StartBtn.setEnabled(True)

        # Pause button
        self.PauseBtn = QtGui.QPushButton("Pause")
        sizePolicyBtn.setHeightForWidth(self.PauseBtn.sizePolicy().hasHeightForWidth())
        self.PauseBtn.setSizePolicy(sizePolicyBtn)
        self.PauseBtn.setStyleSheet("background-color: gray; color: black; font-size: 32px; font: bold")
        self.PauseBtn.clicked.connect(self.pause)
        self.PauseBtn.setEnabled(False)
        
        # Reset button
        self.ResetBtn = QtGui.QPushButton("Reset")
        sizePolicyBtn.setHeightForWidth(self.ResetBtn.sizePolicy().hasHeightForWidth())
        self.ResetBtn.setSizePolicy(sizePolicyBtn)
        self.ResetBtn.setStyleSheet("background-color: gray; color: black; font-size: 32px; font: bold")
        self.ResetBtn.clicked.connect(self.reset)
        self.ResetBtn.setEnabled(True)

        # PLUS button
        self.PlusBtn = QtGui.QPushButton("+")
        sizePolicyBtn.setHeightForWidth(self.PlusBtn.sizePolicy().hasHeightForWidth())
        self.PlusBtn.setSizePolicy(sizePolicyBtn)
        self.PlusBtn.setStyleSheet("background-color: gray; color: black; font-size: 48px; font: bold")
        self.PlusBtn.clicked.connect(self.plusOne)
        self.PlusBtn.setEnabled(True)

        # GraphicView
        self.Image = pg.ImageItem()
        self.Plot = pg.PlotWidget(title=self.game.name, labels={"left":"Cell number", "bottom":"Depth"})
        self.Plot.hideAxis("bottom")
        self.Plot.hideAxis("left")
        self.Plot.addItem(self.Image)
        
        self.Image.setImage(image=np.transpose(np.flip(self.game.BOARD, axis=0)))

        # Build lookup table
        lut = np.zeros((256,3), dtype=np.ubyte)
        lut[:10,:] = 50
        lut[10:,0] = 255
        lut[:,1] = np.arange(0,256)
        self.Image.setLookupTable(lut, update=True)

        # Instanciates the layout
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.Plot, 0, 0, 4, 4)    
        self.layout.addWidget(self.StartBtn, 0, 4, 1, 1)
        self.layout.addWidget(self.PauseBtn, 1, 4, 1, 1)
        self.layout.addWidget(self.ResetBtn, 2, 4, 1, 1)
        self.layout.addWidget(self.PlusBtn, 3, 4, 1, 1)

        # Add Timer for displaying and saving data
        self.displayTimer = QtCore.QTimer()
        self.displayTimer.timeout.connect(self.propagate)

        # Display the interface on the screen
        self.show()

    def start(self):

        # Disable Start-Button and enable Pause-Button
        self.PauseBtn.setEnabled(True)
        self.PauseBtn.setStyleSheet("background-color: red; color: black; font-size: 32px; font: bold")

        self.StartBtn.setEnabled(False)
        self.StartBtn.setStyleSheet("background-color: gray; color: black; font-size: 32px; font: bold")

        # Starts the display loop
        self.displayTimer.start(100) #Timer is set to 100 ms
        return

    def pause(self):

        # Disable Pause-Button and enable Start-Button
        self.StartBtn.setEnabled(True)
        self.StartBtn.setStyleSheet("background-color: green; color: black; font-size: 32px; font: bold")

        self.PauseBtn.setEnabled(False)
        self.PauseBtn.setStyleSheet("background-color: gray; color: black; font-size: 32px; font: bold")

        # Stops the display loop
        self.displayTimer.stop()

        return

    def reset(self):
        
        # Pauses the game
        self.pause()

        # Resets the plot
        self.game.BOARD = np.copy(self.game.initialBOARD)
        self.updatePlot()
        return

    def plusOne(self):

        # Stops the display loop
        self.displayTimer.stop()
        
        # Propagates once
        self.propagate()
        return

    def propagate(self):
        
        # Updates the plot to the next iteration result
        self.game.takeOneStep()
        self.updatePlot()
        return


    def updatePlot(self):

        # Updates the plot with the current state of the game
        self.Image.setImage(image=np.transpose(np.flip(self.game.BOARD, axis=0)))
        return



def run():
    global app
    app = QtWidgets.QApplication(sys.argv)  # Every PyQt application must create an application object
    gui = GuiManager()                      # Create an object "GuiManager"
    sys.exit(app.exec_())                   # Enter the main loop of the application


if __name__ == '__main__':
    run()