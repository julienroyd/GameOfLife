# GameOfLife
John Conway's Game of Life

After watching this [great video](https://www.youtube.com/watch?v=E8kUJL04ELA) from Numberfile on Youtube, I decided to try and implement this fun experiment.

### Requirements

* `conda create --name gameoflife_env python=3.7.4` 
* `pip install requirements.txt`

### The project
This project is meant to be a simple implementation of Conway's Game of Life, wrapped into a GUI in order to allow the user to play around and have fun exploring different board configurations.

GUI features:
* Start, Pause and Reset the propagation of living cells on the BOARD
* Interact or create new shapes during an experiment by clicking on the BOARD
* Change the propagation speed (slider)
* Try out different configurations (left and right arrows)
* Create New configurations (called initialBOARDs) and Save them
* Manage saved configurations by allowing to Delete unused ones
* Zoom-in Zoom-out and shift the display to observe in more detail certain areas
* Increase or Decrease the size of the BOARD (it can be interesting to confine an experiment within walls instead of giving it unlimited amount of space)

To run the program : `python GuiManager.py`

![John Conway and his game of Life (from Numberfile on Youtube)](https://i.ytimg.com/vi/R9Plq-D1gEk/maxresdefault.jpg)
*Image Source : [Inventing the Game of Life - Numberfile](https://www.youtube.com/watch?v=R9Plq-D1gEk)*
