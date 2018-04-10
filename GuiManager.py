import numpy as np
import time
import sys
import os
from PyQt5 import QtGui, QtCore, QtWidgets
import pyqtgraph as pg 

from GameOfLife import GameOfLife


"""
For some reason, this makes sure the 
icon can be displayed properly in Windows taskbar
"""
import ctypes
import platform
if platform.system() == "Windows":
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# GUI MANAGER
class GuiManager(QtWidgets.QWidget):

    def __init__(self):
        super(GuiManager, self).__init__() # Initializes the base class QMainWindow

        # Instanciates a GameOfLife object
        self.game = GameOfLife()
        self.isRunning = False

        # Establishes the accepted size for the image
        self.listOfSizes = [10, 20, 50, 100, 200]

        # Reads the .npy files of our initial BOARDs collection
        self.initialBOARDs = self.readinitialBOARDsFiles()
        self.currentInitialBOARD = 0

        # Initializes the GUI widgets and layout
        self.setupGUI()

        # Load the initial BOARD and update it in the game object
        self.loadInitialBOARD()
    
    # WIDGETS AND LAYOUT ----------------------------------------------------------------------------------------------
    def setupGUI(self):

        # Sets the name, incon and size of the main window
        self.setWindowTitle('The Game Of Life') 
        self.setWindowIcon(QtGui.QIcon('Logo.PNG'))
        self.resize(1000,800)

        # Add Timer for displaying and saving data
        self.displayTimer = QtCore.QTimer()
        self.displayTimer.timeout.connect(self.propagate)

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
        self.PauseBtn.setStyleSheet("background-color: rgba(200,200,200,250); color: rgba(150,150,150,250); font-size: 32px; font: bold; border-radius: 3px")
        self.PauseBtn.clicked.connect(self.pause)
        self.PauseBtn.setEnabled(False)

        # PLUS button
        self.PlusBtn = QtGui.QPushButton("+")
        sizePolicyBtn.setHeightForWidth(self.PlusBtn.sizePolicy().hasHeightForWidth())
        self.PlusBtn.setSizePolicy(sizePolicyBtn)
        self.PlusBtn.setStyleSheet("background-color: gray; color: black; font-size: 32px; font: bold; border-radius: 3px")
        self.PlusBtn.clicked.connect(self.plusOne)
        self.PlusBtn.setEnabled(True)

        # Reset button
        self.ResetBtn = QtGui.QPushButton("Reset")
        sizePolicyBtn.setHeightForWidth(self.ResetBtn.sizePolicy().hasHeightForWidth())
        self.ResetBtn.setSizePolicy(sizePolicyBtn)
        self.ResetBtn.setStyleSheet("background-color: gray; color: black; font-size: 32px; font: bold; border-radius: 3px")
        self.ResetBtn.clicked.connect(self.reset)
        self.ResetBtn.setEnabled(True)

        # Slider for propagation speed
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider.setRange(1, 100)
        self.slider.setValue(10)
        self.freq = (1. / 10) * 1e3 # Frequency in ms
        self.slider.valueChanged[int].connect(self.changePropagationSpeed)
        self.slider.setEnabled(True)

        # RIGHT button
        self.RightBtn = QtGui.QPushButton("->")
        sizePolicyBtn.setHeightForWidth(self.RightBtn.sizePolicy().hasHeightForWidth())
        self.RightBtn.setSizePolicy(sizePolicyBtn)
        self.RightBtn.setStyleSheet("background-color: rgba(40,97,130,250); color: black; font-size: 32px; font: bold; border-radius: 3px")
        self.RightBtn.clicked.connect(self.right)
        self.RightBtn.setEnabled(True)

        # LEFT button
        self.LeftBtn = QtGui.QPushButton("<-")
        sizePolicyBtn.setHeightForWidth(self.LeftBtn.sizePolicy().hasHeightForWidth())
        self.LeftBtn.setSizePolicy(sizePolicyBtn)
        self.LeftBtn.setStyleSheet("background-color: rgba(40,97,130,250); color: black; font-size: 28px; font: bold; border-radius: 3px")
        self.LeftBtn.clicked.connect(self.left)
        self.LeftBtn.setEnabled(True)

        # Create New button
        self.CreateNewBtn = QtGui.QPushButton("Create New")
        sizePolicyBtn.setHeightForWidth(self.CreateNewBtn.sizePolicy().hasHeightForWidth())
        self.CreateNewBtn.setSizePolicy(sizePolicyBtn)
        self.CreateNewBtn.setStyleSheet("background-color: rgba(40,97,130,250); color: black; font-size: 24px; font: bold; border-radius: 3px")
        self.CreateNewBtn.clicked.connect(self.createNew)
        self.CreateNewBtn.setEnabled(True)

        # Save button
        self.SaveBtn = QtGui.QPushButton("Save")
        sizePolicyBtn.setHeightForWidth(self.SaveBtn.sizePolicy().hasHeightForWidth())
        self.SaveBtn.setSizePolicy(sizePolicyBtn)
        self.SaveBtn.setStyleSheet("background-color: rgba(17, 137, 107,200); color: black; font-size: 32px; font: bold; border-radius: 5px")
        self.SaveBtn.clicked.connect(self.save)
        self.SaveBtn.setEnabled(True)

        # Delete button
        self.DeleteBtn = QtGui.QPushButton("Delete")
        sizePolicyBtn.setHeightForWidth(self.DeleteBtn.sizePolicy().hasHeightForWidth())
        self.DeleteBtn.setSizePolicy(sizePolicyBtn)
        self.DeleteBtn.setStyleSheet("background-color: rgba(17, 137, 107,200); color: black; font-size: 32px; font: bold; border-radius: 3px")
        self.DeleteBtn.clicked.connect(self.delete)
        self.DeleteBtn.setEnabled(True)

        # IncreaseSize button
        self.IncreaseSizeBtn = QtGui.QPushButton("Increase Size")
        sizePolicyBtn.setHeightForWidth(self.IncreaseSizeBtn.sizePolicy().hasHeightForWidth())
        self.IncreaseSizeBtn.setSizePolicy(sizePolicyBtn)
        self.IncreaseSizeBtn.setStyleSheet("background-color: gray; color: black; font-size: 12px; font: bold")
        self.IncreaseSizeBtn.clicked.connect(self.increase)
        self.IncreaseSizeBtn.setEnabled(True)

        # DecreaseSize button
        self.DecreaseSizeBtn = QtGui.QPushButton("Decrease Size")
        sizePolicyBtn.setHeightForWidth(self.DecreaseSizeBtn.sizePolicy().hasHeightForWidth())
        self.DecreaseSizeBtn.setSizePolicy(sizePolicyBtn)
        self.DecreaseSizeBtn.setStyleSheet("background-color: gray; color: rgba(150,150,150,250); font-size: 12px; font: bold")
        self.DecreaseSizeBtn.clicked.connect(self.decrease)
        self.DecreaseSizeBtn.setEnabled(True)

        # GraphicView
        self.Image = pg.ImageItem()
        self.Image.mousePressEvent = self.getPos
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

        self.layout.addWidget(self.Plot, 0, 0, 60, 60)    
        
        self.layout.addWidget(self.StartBtn, 5, 60, 5, 10)
        self.layout.addWidget(self.PauseBtn, 10, 60, 5, 10)
        self.layout.addWidget(self.PlusBtn, 15, 60, 5, 10)
        
        self.layout.addWidget(self.slider, 22, 60, 2, 10)
        self.layout.addWidget(self.ResetBtn, 25, 60, 5, 10)
        
        self.layout.addWidget(self.RightBtn, 35, 65, 5, 5)
        self.layout.addWidget(self.LeftBtn, 35, 60, 5, 5)
        self.layout.addWidget(self.CreateNewBtn, 40, 60, 5, 10)
        
        self.layout.addWidget(self.SaveBtn, 50, 60, 5, 10)
        self.layout.addWidget(self.DeleteBtn, 55, 60, 5, 10)

        self.layout.addWidget(self.DecreaseSizeBtn, 60, 0, 1, 10)
        self.layout.addWidget(self.IncreaseSizeBtn, 60, 10, 1, 10)
        


        splash_pix = QtGui.QPixmap('Logo.PNG')
        splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        splash.show()
        time.sleep(0)

        # Display the interface on the screen
        self.show()

    def start(self):
        self.isRunning = True

        # Disable Start-Button and enable Pause-Button
        self.PauseBtn.setEnabled(True)
        self.PauseBtn.setStyleSheet("background-color: red; color: black; font-size: 32px; font: bold; border-radius: 3px")

        self.StartBtn.setEnabled(False)
        self.StartBtn.setStyleSheet("background-color: rgba(200,200,200,250); color: rgba(150,150,150,250); font-size: 32px; font: bold; border-radius: 3px")

        # Disables the PLUS button
        self.PlusBtn.setEnabled(False)
        self.PlusBtn.setStyleSheet("background-color: rgba(200,200,200,250); color: rgba(150,150,150,250); font-size: 32px; font: bold; border-radius: 3px")

        # Disables the Delete button
        self.DeleteBtn.setEnabled(False)
        self.DeleteBtn.setStyleSheet("background-color: rgba(174, 242, 225,200); color: rgba(150,150,150,250); font-size: 32px; font: bold; border-radius: 3px")

        # Starts the display loop
        self.displayTimer.start(self.freq)
        return

    def pause(self):
        self.isRunning = False

        # Disable Pause-Button and enable Start-Button
        self.StartBtn.setEnabled(True)
        self.StartBtn.setStyleSheet("background-color: green; color: black; font-size: 32px; font: bold; border-radius: 5px")

        self.PauseBtn.setEnabled(False)
        self.PauseBtn.setStyleSheet("background-color: rgba(200,200,200,250); color: rgba(150,150,150,250); font-size: 32px; font: bold; border-radius: 5px")

        # Enables the PLUS button
        self.PlusBtn.setEnabled(True)
        self.PlusBtn.setStyleSheet("background-color: gray; color: black; font-size: 32px; font: bold; border-radius: 3px")

        # Stops the display loop
        self.displayTimer.stop()

        return

    def reset(self):      
        # Pauses the game
        self.pause()

        # Resets the plot
        self.game.BOARD = np.copy(self.game.initialBOARD)
        self.updatePlot()

        # Enables the Delete button
        self.DeleteBtn.setEnabled(True)
        self.DeleteBtn.setStyleSheet("background-color: rgba(17, 137, 107,200); color: black; font-size: 32px; font: bold; border-radius: 3px")

        return

    def plusOne(self):
        # Stops the display loop
        self.displayTimer.stop()
        
        # Propagates once
        self.propagate()

        # Disables the Delete button
        self.DeleteBtn.setEnabled(False)
        self.DeleteBtn.setStyleSheet("background-color: rgba(174, 242, 225,200); color: rgba(150,150,150,250); font-size: 32px; font: bold; border-radius: 3px")

        return

    def propagate(self):
        # Updates the plot to the next iteration result
        self.game.takeOneStep()
        self.updatePlot()
        return


    def updatePlot(self):
        # Updates the plot with the current state of the game
        self.Image.setImage(image=np.transpose(np.flip(self.game.BOARD.astype(np.uint8), axis=0)))
        return

    def changePropagationSpeed(self, value):
        # The value corresponds to the number of steps per second
        self.freq = (1. / value) * 1e3 # Frequency in ms
        if self.isRunning:
            self.displayTimer.start(self.freq)

    def right(self):
        self.initialBOARDs = self.readinitialBOARDsFiles()
        # Sets the initial BOARD to next in the list
        self.currentInitialBOARD += 1
        if self.currentInitialBOARD >= len(self.initialBOARDs):
            self.currentInitialBOARD = 0

        self.loadInitialBOARD()
        self.reset()
        self.checkAllowedSizes()

        # Resets the zooming on the image
        self.Plot.autoRange()
        self.Plot.enableAutoRange()
        return

    def left(self):
        self.initialBOARDs = self.readinitialBOARDsFiles()
        # Sets the initial BOARD to previous in the list
        self.currentInitialBOARD -= 1
        if self.currentInitialBOARD < 0:
            self.currentInitialBOARD = len(self.initialBOARDs) - 1
        self.loadInitialBOARD()
        self.reset()
        self.checkAllowedSizes()
        
        # Resets the zooming on the image
        self.Plot.autoRange()
        self.Plot.enableAutoRange()
        return

    def createNewInitialBOARD(self):
        self.pause()
        creationWindow = BOARDcreator()
        return

    def loadInitialBOARD(self):
        # Loads the initial BOARD corresponding to the index currentInitialBOARD in the list
        array = np.load(os.path.join("InitialBOARDs", self.initialBOARDs[self.currentInitialBOARD]))
        
        # Updates the initial BOARD and its name in the game object
        self.game.initialBOARD = np.copy(array)
        self.game.BOARD = np.copy(self.game.initialBOARD.astype(np.uint8))
        self.updatePlot()
        self.Plot.setTitle(title="The "+self.initialBOARDs[self.currentInitialBOARD].split('.')[0])
        self.resetSize()
        self.checkAllowedSizes()
        return

    def readinitialBOARDsFiles(self):
        # Creates a list of strings with the name of .npy files in Data Directory
        fileList = os.listdir("InitialBOARDs")
        numpyFiles = [f for f in fileList if f.split('.')[-1] == 'npy']

        # Sort alpha-numerically the list of files
        sortedFiles = sorted(numpyFiles, key=lambda item: (int(item.partition('.')[0]) if item[0].isdigit() else float('inf'), item))

        return sortedFiles

    def getPos(self , event):
        y = int(event.pos().x())
        x = (self.game.BOARD.shape[0] - 1) - int(event.pos().y())

        if self.game.BOARD[x,y] == True:
            self.game.BOARD[x,y] = False
        else:
            self.game.BOARD[x,y] = True

        self.updatePlot()


    def increase(self):
        if self.currentSize < len(self.listOfSizes) - 1:
            self.currentSize += 1
            self.checkAllowedSizes()
            self.enlargeImage()
            self.Image.setImage(image=np.transpose(np.flip(self.game.BOARD.astype(np.uint8), axis=0)))


    def decrease(self):
        if self.currentSize > 0:
            self.currentSize -= 1
            self.checkAllowedSizes()
            self.diminishImage()
            self.Image.setImage(image=np.transpose(np.flip(self.game.BOARD.astype(np.uint8), axis=0)))


    def enlargeImage(self):
        biggerImage = np.zeros(shape=(self.listOfSizes[self.currentSize], self.listOfSizes[self.currentSize]), dtype=np.uint8)
        biggerImage[:self.game.BOARD.shape[0],:self.game.BOARD.shape[1]] = self.game.BOARD
        self.game.BOARD = biggerImage


    def diminishImage(self):
        smallerImage = self.game.BOARD[:self.listOfSizes[self.currentSize], :self.listOfSizes[self.currentSize]]
        self.game.BOARD = smallerImage


    def resetSize(self):
        if self.game.BOARD.shape[0] in self.listOfSizes:
            self.currentSize = self.listOfSizes.index(self.game.BOARD.shape[0])
        else:
            raise ValueError("The initial BOARD has an unrecognized grid size. Size should be one of those values : [10, 20, 50, 100, 200]")

    def checkAllowedSizes(self):        
        if self.currentSize == len(self.listOfSizes) - 1:
            self.IncreaseSizeBtn.setEnabled(False)
            self.IncreaseSizeBtn.setStyleSheet("background-color: rgba(200,200,200,250); color: rgba(150,150,150,250); font-size: 12px; font: bold")
        else:
            self.IncreaseSizeBtn.setEnabled(True)
            self.IncreaseSizeBtn.setStyleSheet("background-color: gray; color: black; font-size: 12px; font: bold")
        

        if self.currentSize == 0:
            self.DecreaseSizeBtn.setEnabled(False)
            self.DecreaseSizeBtn.setStyleSheet("background-color: rgba(200,200,200,250); color: rgba(150,150,150,250); font-size: 12px; font: bold")
        else:
            self.DecreaseSizeBtn.setEnabled(True)
            self.DecreaseSizeBtn.setStyleSheet("background-color: gray; color: black; font-size: 12px; font: bold")

    def save(self):
        # Shows a dialogue pop-up box to choose whether to overwrite or save as new BOARD
        message = 'Do you want to save with a new name or overwrite "The {0}"'.format(self.initialBOARDs[self.currentInitialBOARD])
        box = box = QtGui.QMessageBox()
        box.setIcon(QtGui.QMessageBox.Question)
        box.setWindowTitle('WAIT')
        box.setText(message)
        box.setStandardButtons(QtGui.QMessageBox.Yes|QtGui.QMessageBox.Cancel|QtGui.QMessageBox.Apply)
        OverwriteBtn = box.button(QtGui.QMessageBox.Apply)
        OverwriteBtn.setText('Overwrite')
        NewNameBtn = box.button(QtGui.QMessageBox.Yes)
        NewNameBtn.setText('New name')
        CancelBtn = box.button(QtGui.QMessageBox.Cancel)
        box.exec_()

        if box.clickedButton() == OverwriteBtn:
            # Overwrites the .npy file with current self.game.BOARD
            np.save(os.path.join("InitialBOARDs", self.initialBOARDs[self.currentInitialBOARD]), self.game.BOARD)

        elif box.clickedButton() == NewNameBtn:
            # Shows a dialogue pop-up box to enter a name for the newly created initialBOARD
            text, ok = QtWidgets.QInputDialog.getText(self, 'Final Step', 'Name (no spaces) :')
            if ok:
                np.save(os.path.join("InitialBOARDs", text.replace(" ", "")), self.game.BOARD)
                self.initialBOARDs = self.readinitialBOARDsFiles()
                self.currentInitialBOARD = self.initialBOARDs.index(text.replace(" ", "") + ".npy")
                self.loadInitialBOARD()



    def delete(self):
        # Shows a pop-up asking for confirmation
        message = 'Are you sure you want to delete initial BOARD "The {0}"?'.format(self.initialBOARDs[self.currentInitialBOARD].split('.')[0])
        reply = QtGui.QMessageBox.question(self, 'WAIT', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            os.remove(os.path.join("InitialBOARDs", self.initialBOARDs[self.currentInitialBOARD]))
            self.initialBOARDs = self.readinitialBOARDsFiles()
            if self.currentInitialBOARD > 0:
                self.currentInitialBOARD -= 1
            else:
                self.currentInitialBOARD = 0
            self.loadInitialBOARD()
        return


    def createNew(self):
        self.pause()
        self.game.BOARD = np.zeros(shape=(self.listOfSizes[self.currentSize], self.listOfSizes[self.currentSize]), dtype=np.uint8)
        self.updatePlot()
        self.Plot.setTitle(title="NEW BOARD (still unamed)")
        return




# If we run the file directly
if __name__ == '__main__':
    global app
    app = QtWidgets.QApplication(sys.argv)  # Every PyQt application must create an application object
    gui = GuiManager()                      # Create an object "GuiManager"
    sys.exit(app.exec_())                   # Enter the main loop of the application