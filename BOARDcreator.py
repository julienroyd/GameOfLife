from PyQt5 import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
import sys
import os
import numpy as np



class BOARDcreator(QtWidgets.QWidget):

    def __init__(self):
        super(BOARDcreator, self).__init__() # Initializes the base class QMainWindow

        # BOARD initialization
        self.BOARD = np.zeros(shape=(10,10), dtype=np.bool)

        # Initializes the GUI widgets and layout
        self.setupGUI()

        # Establisehs the accepted size for the image
        self.listOfSizes = [10, 20, 50, 100, 200]
        self.currentSize = 0
        self.checkAllowedSizes()
    
    # WIDGETS AND LAYOUT ----------------------------------------------------------------------------------------------
    def setupGUI(self):

        # Sets the name, incon and size of the main window
        self.setWindowTitle('The Game Of Life') 
        self.setWindowIcon(QtGui.QIcon('Conway.jpg'))
        self.resize(800,800)

        # GraphicView
        self.Image = pg.ImageItem()
        self.Plot = pg.PlotWidget(title="", labels={"left":"Cell number", "bottom":"Depth"})
        self.Plot.hideAxis("bottom")
        self.Plot.hideAxis("left")
        self.Plot.addItem(self.Image)
        
        self.Image.setImage(image=np.transpose(np.flip(self.BOARD, axis=0)))
        self.Image.mousePressEvent = self.getPos

        # Build lookup table
        lut = np.zeros((256,3), dtype=np.ubyte)
        lut[:,2] = np.arange(0,256)
        self.Image.setLookupTable(lut, update=True)

        # Creates the buttons' size policy
        sizePolicyBtn = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        sizePolicyBtn.setHorizontalStretch(0)
        sizePolicyBtn.setVerticalStretch(0)

        # Save button
        self.SaveBtn = QtGui.QPushButton("Save")
        sizePolicyBtn.setHeightForWidth(self.SaveBtn.sizePolicy().hasHeightForWidth())
        self.SaveBtn.setSizePolicy(sizePolicyBtn)
        self.SaveBtn.setStyleSheet("background-color: rgba(17, 137, 107,200); color: black; font-size: 32px; font: bold; border-radius: 5px")
        self.SaveBtn.clicked.connect(self.showDialog)
        self.SaveBtn.setEnabled(True)
        
        # IncreaseSize button
        self.IncreaseSizeBtn = QtGui.QPushButton("Increase Size")
        sizePolicyBtn.setHeightForWidth(self.IncreaseSizeBtn.sizePolicy().hasHeightForWidth())
        self.IncreaseSizeBtn.setSizePolicy(sizePolicyBtn)
        self.IncreaseSizeBtn.setStyleSheet("background-color: gray; color: black; font-size: 16px; font: bold; border-radius: 5px")
        self.IncreaseSizeBtn.clicked.connect(self.increase)
        self.IncreaseSizeBtn.setEnabled(True)

        # DecreaseSize button
        self.DecreaseSizeBtn = QtGui.QPushButton("Decrease Size")
        sizePolicyBtn.setHeightForWidth(self.DecreaseSizeBtn.sizePolicy().hasHeightForWidth())
        self.DecreaseSizeBtn.setSizePolicy(sizePolicyBtn)
        self.DecreaseSizeBtn.setStyleSheet("background-color: rgba(200,200,200,250); color: rgba(150,150,150,250); font-size: 16px; font: bold; border-radius: 5px")
        self.DecreaseSizeBtn.clicked.connect(self.decrease)
        self.DecreaseSizeBtn.setEnabled(True)

        # Instanciates the layout
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.Plot, 0, 0, 50, 50)
        self.layout.addWidget(self.SaveBtn, 50, 30, 1, 20)
        self.layout.addWidget(self.IncreaseSizeBtn, 50, 10, 1, 10)
        self.layout.addWidget(self.DecreaseSizeBtn, 50, 0, 1, 10)

        # Display the interface on the screen
        self.show()

        return


    def getPos(self , event):
        y = int(event.pos().x())
        x = (self.BOARD.shape[0] - 1) - int(event.pos().y())

        if self.BOARD[x,y] == True:
            self.BOARD[x,y] = False
        else:
            self.BOARD[x,y] = True

        self.updateImage()


    def increase(self):
        if self.currentSize < len(self.listOfSizes) - 1:
            self.currentSize += 1
            self.checkAllowedSizes()
            self.enlargeImage()
            self.Image.setImage(image=np.transpose(np.flip(self.BOARD, axis=0)))


    def decrease(self):
        if self.currentSize > 0:
            self.currentSize -= 1
            self.checkAllowedSizes()
            self.diminishImage()
            self.Image.setImage(image=np.transpose(np.flip(self.BOARD, axis=0)))


    def enlargeImage(self):
        biggerImage = np.zeros(shape=(self.listOfSizes[self.currentSize], self.listOfSizes[self.currentSize]), dtype=np.bool)
        biggerImage[:self.BOARD.shape[0],:self.BOARD.shape[1]] = self.BOARD
        self.BOARD = biggerImage


    def diminishImage(self):
        smallerImage = self.BOARD[:self.listOfSizes[self.currentSize], :self.listOfSizes[self.currentSize]]
        self.BOARD = smallerImage


    def checkAllowedSizes(self):
        if self.currentSize == len(self.listOfSizes) - 1:
            self.IncreaseSizeBtn.setEnabled(False)
            self.IncreaseSizeBtn.setStyleSheet("background-color: rgba(200,200,200,250); color: rgba(150,150,150,250); font-size: 16px; font: bold; border-radius: 5px")
        else:
            self.IncreaseSizeBtn.setEnabled(True)
            self.IncreaseSizeBtn.setStyleSheet("background-color: gray; color: black; font-size: 16px; font: bold; border-radius: 5px")
        

        if self.currentSize == 0:
            self.DecreaseSizeBtn.setEnabled(False)
            self.DecreaseSizeBtn.setStyleSheet("background-color: rgba(200,200,200,250); color: rgba(150,150,150,250); font-size: 16px; font: bold; border-radius: 5px")
        else:
            self.DecreaseSizeBtn.setEnabled(True)
            self.DecreaseSizeBtn.setStyleSheet("background-color: gray; color: black; font-size: 16px; font: bold; border-radius: 5px")


    def updateImage(self):
        self.Image.setImage(image=np.transpose(np.flip(self.BOARD, axis=0)))


    def showDialog(self):
        # Shows a dialogue pop-up box to enter a name for the newly created initialBOARD
        text, ok = QtWidgets.QInputDialog.getText(self, 'Final Step', 'Name (no spaces) :')
        
        if ok:
            np.save(os.path.join("InitialBOARDs", text.replace(" ", "") + ".npy"), self.BOARD)
            self.close()


# If we run the file directly
if __name__ == '__main__':
    global app
    app = QtWidgets.QApplication(sys.argv)   # Every PyQt application must create an application object
    gui = BOARDcreator()                     # Create an object "GuiManager"
    sys.exit(app.exec_())                    # Enter the main loop of the application
