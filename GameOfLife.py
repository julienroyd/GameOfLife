import numpy as np
import scipy.signal



class GameOfLife(object):

    def __init__(self, initialBOARD=None, name=""):

        self.BOARD = None
        self.initialBOARD = None


    def takeOneStep(self):
        
        # Makes sure the BOARD is a boolean matrix
        self.BOARD = self.BOARD.astype(np.bool)
        
        # This convolution kernel counts how many neighbors a cell has
        kernel = np.ones(shape=(3,3), dtype=np.int)
        kernel[1,1] = 0

        # Map of number of neighbors for each cell
        neighbors = scipy.signal.convolve2d(self.BOARD, kernel, mode="same")
        
        # Computing condition maps
        V2 = np.array((neighbors==2), dtype=np.bool)
        V3 = np.array((neighbors==3), dtype=np.bool)
        
        # Computing the Newborns map
        Newborns = np.invert(np.bitwise_or(self.BOARD, np.invert(V3)))

        # Computing the Survivors map
        Survivors = np.bitwise_and(self.BOARD, np.bitwise_or(V2, V3))

        # Computing the NewBOARD
        NewBOARD = Newborns + Survivors

        # Update the BOARD attribute
        self.BOARD = NewBOARD.astype(np.uint8)
        
        return