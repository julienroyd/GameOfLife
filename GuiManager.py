import numpy as np
import time
import sys
import os
from PyQt5 import QtGui, QtCore, QtWidgets
import pyqtgraph as pg 

from GameOfLife import GameOfLife


# GUI MANAGER
class GuiManager(QtWidgets.QWidget):

    def __init__(self):
        super(GuiManager, self).__init__() # Initializes the base class QMainWindow

        # Instanciates a GameOfLife object
        self.game = GameOfLife()

        # Reads the .npy files of our initial BOARDs collection
        self.initialBOARDs = self.readinitialBOARDsFiles()
        self.currentInitialBOARD = 0

        # Initializes the GUI widgets and layout
        self.setupGUI()

        # Load the initial BOARD and update it in the game object
        self.loadInitialBOARD()
        self.game.BOARD = np.copy(self.game.initialBOARD)
        self.updatePlot()
    
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
        self.StartBtn.setStyleSheet("background-color: green; color: black; font-size: 32px; font: bold; border-radius: 3px")
        self.StartBtn.clicked.connect(self.start)
        self.StartBtn.setEnabled(True)

        # Pause button
        self.PauseBtn = QtGui.QPushButton("Pause")
        sizePolicyBtn.setHeightForWidth(self.PauseBtn.sizePolicy().hasHeightForWidth())
        self.PauseBtn.setSizePolicy(sizePolicyBtn)
        self.PauseBtn.setStyleSheet("background-color: gray; color: black; font-size: 32px; font: bold; border-radius: 3px")
        self.PauseBtn.clicked.connect(self.pause)
        self.PauseBtn.setEnabled(False)
        
        # Reset button
        self.ResetBtn = QtGui.QPushButton("Reset")
        sizePolicyBtn.setHeightForWidth(self.ResetBtn.sizePolicy().hasHeightForWidth())
        self.ResetBtn.setSizePolicy(sizePolicyBtn)
        self.ResetBtn.setStyleSheet("background-color: gray; color: black; font-size: 32px; font: bold; border-radius: 3px")
        self.ResetBtn.clicked.connect(self.reset)
        self.ResetBtn.setEnabled(True)

        # PLUS button
        self.PlusBtn = QtGui.QPushButton("+")
        sizePolicyBtn.setHeightForWidth(self.PlusBtn.sizePolicy().hasHeightForWidth())
        self.PlusBtn.setSizePolicy(sizePolicyBtn)
        self.PlusBtn.setStyleSheet("background-color: gray; color: black; font-size: 48px; font: bold; border-radius: 3px")
        self.PlusBtn.clicked.connect(self.plusOne)
        self.PlusBtn.setEnabled(True)

        # RIGHT button
        self.RightBtn = QtGui.QPushButton("->")
        sizePolicyBtn.setHeightForWidth(self.RightBtn.sizePolicy().hasHeightForWidth())
        self.RightBtn.setSizePolicy(sizePolicyBtn)
        self.RightBtn.setStyleSheet("background-color: rgba(40,97,130,250); color: black; font-size: 48px; font: bold; border-radius: 3px")
        self.RightBtn.clicked.connect(self.right)
        self.RightBtn.setEnabled(True)

        # LEFT button
        self.LeftBtn = QtGui.QPushButton("<-")
        sizePolicyBtn.setHeightForWidth(self.LeftBtn.sizePolicy().hasHeightForWidth())
        self.LeftBtn.setSizePolicy(sizePolicyBtn)
        self.LeftBtn.setStyleSheet("background-color: rgba(40,97,130,250); color: black; font-size: 48px; font: bold; border-radius: 3px")
        self.LeftBtn.clicked.connect(self.left)
        self.LeftBtn.setEnabled(True)

        # CreateBOARD button
        self.CreateBOARDBtn = QtGui.QPushButton("Create New")
        sizePolicyBtn.setHeightForWidth(self.CreateBOARDBtn.sizePolicy().hasHeightForWidth())
        self.CreateBOARDBtn.setSizePolicy(sizePolicyBtn)
        self.CreateBOARDBtn.setStyleSheet("background-color: rgba(40,97,130,250); color: black; font-size: 32px; font: bold; border-radius: 3px")
        self.CreateBOARDBtn.clicked.connect(self.createNewInitialBOARD)
        self.CreateBOARDBtn.setEnabled(True)

        # GraphicView
        self.Image = pg.ImageItem()
        self.Plot = pg.PlotWidget(title="The "+self.initialBOARDs[self.currentInitialBOARD].split('.')[0], labels={"left":"Cell number", "bottom":"Depth"})
        self.Plot.hideAxis("bottom")
        self.Plot.hideAxis("left")
        self.Plot.addItem(self.Image)

        # Build lookup table
        lut = np.zeros((256,3), dtype=np.ubyte)
        lut[:10,:] = 50
        lut[10:,0] = 255
        lut[:,1] = np.arange(0,256)
        self.Image.setLookupTable(lut, update=True)

        # Instanciates the layout
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.Plot, 0, 0, 50, 50)    
        
        self.layout.addWidget(self.StartBtn, 5, 50, 5, 10)
        self.layout.addWidget(self.PauseBtn, 10, 50, 5, 10)
        self.layout.addWidget(self.PlusBtn, 15, 50, 5, 10)
        self.layout.addWidget(self.ResetBtn, 22, 50, 5, 10)
        
        self.layout.addWidget(self.RightBtn, 35, 55, 5, 5)
        self.layout.addWidget(self.LeftBtn, 35, 50, 5, 5)
        self.layout.addWidget(self.CreateBOARDBtn, 40, 50, 5, 10)

        # Add Timer for displaying and saving data
        self.displayTimer = QtCore.QTimer()
        self.displayTimer.timeout.connect(self.propagate)

        # Display the interface on the screen
        self.show()

    def start(self):
        # Disable Start-Button and enable Pause-Button
        self.PauseBtn.setEnabled(True)
        self.PauseBtn.setStyleSheet("background-color: red; color: black; font-size: 32px; font: bold; border-radius: 3px")

        self.StartBtn.setEnabled(False)
        self.StartBtn.setStyleSheet("background-color: gray; color: black; font-size: 32px; font: bold; border-radius: 3px")

        # Starts the display loop
        self.displayTimer.start(50) #Timer is set to 100 ms
        return

    def pause(self):
        # Disable Pause-Button and enable Start-Button
        self.StartBtn.setEnabled(True)
        self.StartBtn.setStyleSheet("background-color: green; color: black; font-size: 32px; font: bold; border-radius: 5px")

        self.PauseBtn.setEnabled(False)
        self.PauseBtn.setStyleSheet("background-color: gray; color: black; font-size: 32px; font: bold; border-radius: 5px")

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

    def right(self):
        # Sets the initial BOARD to next in the list
        self.currentInitialBOARD += 1
        if self.currentInitialBOARD >= len(self.initialBOARDs):
            self.currentInitialBOARD = 0

        self.loadInitialBOARD()
        self.reset()
        return

    def left(self):
        # Sets the initial BOARD to previous in the list
        self.currentInitialBOARD -= 1
        if self.currentInitialBOARD < 0:
            self.currentInitialBOARD = len(self.initialBOARDs) - 1
        self.loadInitialBOARD()
        self.reset()
        return

    def createNewInitialBOARD(self):
        # TODO
        return

    def loadInitialBOARD(self):
        # Loads the initial BOARD corresponding to the index currentInitialBOARD in the list
        array = np.load(os.path.join("InitialBOARDs", self.initialBOARDs[self.currentInitialBOARD]))
        
        # Updates the initial BOARD and its name in the game object
        self.game.initialBOARD = np.copy(array)
        self.Plot.setTitle(title="The "+self.initialBOARDs[self.currentInitialBOARD].split('.')[0])
        return

    def readinitialBOARDsFiles(self):
        # Creates a list of strings with the name of .npy files in Data Directory
        fileList = os.listdir("InitialBOARDs")
        numpyFiles = [f for f in fileList if f.split('.')[-1] == 'npy']

        # Sort alpha-numerically the list of files
        sortedFiles = sorted(numpyFiles, key=lambda item: (int(item.partition('.')[0]) if item[0].isdigit() else float('inf'), item))

        return sortedFiles



def run():
    global app
    app = QtWidgets.QApplication(sys.argv)  # Every PyQt application must create an application object
    gui = GuiManager()                      # Create an object "GuiManager"
    sys.exit(app.exec_())                   # Enter the main loop of the application


if __name__ == '__main__':
    run()