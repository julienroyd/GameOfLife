import numpy as np
import scipy.signal



class GameOfLife(object):

    def __init__(self, initialBOARD=None, name=""):

        if initialBOARD == None:

            # Default BOARD initialization
            self.BOARD = np.zeros(shape=(20,20), dtype=np.bool)
            self.BOARD[[1,1,2,3,3,4,4,4,4], [2,5,6,2,6,3,4,5,6]] = True # The Lightweight Spaceship
            self.name = "The Lightweight Spaceship"

            # Saves the initial board for future reference
            self.initialBOARD = np.copy(self.BOARD)
        
        elif type(initialBOARD) == np.ndarray and initialBOARD.shape == (20,20):

            # User defined BOARD initialization
            self.BOARD = initialBOARD
            self.name = name

            # Saves the initial board for future reference
            self.initialBOARD = np.copy(self.BOARD)

        else:

            # initialBOARD with unrecognized type or shape
            raise(ValueError, 'The argument "initialBOARD" provided to instanciate a "GameOfLife" should be a ndarray of shape (20, 20)')


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
        self.BOARD = NewBOARD
        
        return