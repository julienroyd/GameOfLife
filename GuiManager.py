import numpy as np
import time
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import pyqtgraph as pg 


# GUI MANAGER
class GuiManager(QtWidgets.QWidget):

    def __init__(self):
        super(GuiManager, self).__init__() # Initializes the base class QMainWindow
        
        # Initializes the GUI widgets and layout
        self.setupGUI()
    
    # WIDGETS AND LAYOUT ----------------------------------------------------------------------------------------------
    def setupGUI(self):

        # Sets the name, incon and size of the main window
        self.setWindowTitle('The Game Of Life') 
        self.setWindowIcon(QtGui.QIcon('Conway.jpg'))
        self.resize(1500,800)

        # GraphicView for GameOfLife board       
        self.Image = pg.ImageItem()
        self.Board = pg.PlotWidget(title="B-mode Image", labels={"left":"Cell number", "bottom":"Depth"})
        self.Board.addItem(self.Image)

        # Creates the buttons' size policy
        sizePolicyBtn = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        sizePolicyBtn.setHorizontalStretch(0)
        sizePolicyBtn.setVerticalStretch(0)
        
        # Start button
        self.StartBtn = QtGui.QPushButton("Start")
        sizePolicyBtn.setHeightForWidth(self.StartBtn.sizePolicy().hasHeightForWidth())
        self.StartBtn.setSizePolicy(sizePolicyBtn)
        self.StartBtn.setStyleSheet("background-color: green; color: black; font-size: 16px; font: bold")
        self.StartBtn.clicked.connect(self.startPropagation)
        self.StartBtn.setEnabled(False)
        
        # Reset button
        self.ResetBtn = QtGui.QPushButton("Reset")
        sizePolicyBtn.setHeightForWidth(self.ResetBtn.sizePolicy().hasHeightForWidth())
        self.ResetBtn.setSizePolicy(sizePolicyBtn)
        self.ResetBtn.setStyleSheet("background-color: gray; color: black; font-size: 16px; font: bold")
        self.ResetBtn.clicked.connect(self.resetPlot)
        self.ResetBtn.setEnabled(False)

        # PLUS button
        self.PlusBtn = QtGui.QPushButton("+")
        sizePolicyBtn.setHeightForWidth(self.PlusBtn.sizePolicy().hasHeightForWidth())
        self.PlusBtn.setSizePolicy(sizePolicyBtn)
        self.PlusBtn.setStyleSheet("background-color: gray; color: black; font-size: 16px; font: bold")
        self.PlusBtn.clicked.connect(self.takeOneStep)
        self.PlusBtn.setEnabled(False)

        # GraphicView
        self.Image = pg.ImageItem()
        self.Plot = pg.PlotWidget(title="MAP", labels={"left":"Cell number", "bottom":"Depth"})
        self.Plot.hideAxis("bottom")
        self.Plot.hideAxis("left")
        self.Plot.addItem(self.Image)

        # Instanciates the layout objects and initialises the first one
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.Plot, 0, 0, 5, 5)    
        self.layout.addWidget(self.StartBtn, 4, 0, 1, 2)
        self.layout.addWidget(self.ResetBtn, 4, 2, 1, 2)
        self.layout.addWidget(self.PlusBtn, 4, 4, 1, 1)

        # Display the interface on the screen
        self.show()

    def startPropagation(self):
        return

    def resetPlot(self):
        return

    def takeOneStep(self):
        return



def run():
    global app
    app = QtWidgets.QApplication(sys.argv)  # Every PyQt application must create an application object
    gui = GuiManager()                      # Create an object "GuiManager"
    sys.exit(app.exec_())                   # Enter the main loop of the application


if __name__ == '__main__':
    run()