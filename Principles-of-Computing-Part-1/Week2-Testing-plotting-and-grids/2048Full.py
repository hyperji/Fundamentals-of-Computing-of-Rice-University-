"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def random_pick_odd(some_list, odds): 
    '''
    this function is a function which choose an object from some list according 
    to some probability distribution.
    
    '''
    table = [z for x,y in zip(some_list,odds) for z in [x] * y]   
    return random.choice(table)  





'''
 This is a merge function for single line.
 I just simply hope it can pass the mechine test.
 God, please don't be wrong again
'''
def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code
    result = []
    binner = []
    binner.extend(line)
    for thing in range(len(binner)):
        have_nonzero = False
        if binner[thing] != 0:
            if binner[thing] in binner[thing+1:]:
                indexing = binner[thing+1:].index(binner[thing])
                for omg in binner[thing+1:indexing+thing+1]:
                    if omg != 0 and omg != None:
                        have_nonzero = True
                if have_nonzero:
                    result.append(binner[thing])
                else:
                    result.append(2*binner[thing])
                    binner[thing] = 0
                    binner[binner.index(result[-1]/2)] = 0
            else:
                result.append(binner[thing])
            binner[thing] = 0
    for dummy_kindle in range(len(binner) - len(result)):
        result.append(0)
    return result



class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        
        
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.grid = [[0 for dummy_row in range(self.grid_width)]
                           for dummy_col in range(self.grid_height)]
        
               
        self.Initial_tiles = {UP: zip([0]*self.grid_width, range(0,self.grid_width)),
                        DOWN: zip([self.grid_height-1]*self.grid_width,range(0,self.grid_width)),
                        LEFT: zip(range(0,self.grid_height), [0]*self.grid_height),
                        RIGHT: zip(range(0,self.grid_height),[self.grid_width-1]*self.grid_height)}
      
        

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self.grid = [[0 for dummy_col in range(self.grid_width)]
                           for dummy_row in range(self.grid_height)]
        
        self.new_tile()
        self.new_tile()
        

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return "show yourself!"

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        changed = False
        if direction == 3 or direction == 4:
            iter_param = self.grid_width
        else:
            iter_param = self.grid_height
        for start_cell in self.Initial_tiles[direction]:
            temporary_list = []
            temporary = []
            for step in range(iter_param):
                row = start_cell[0] +  step*OFFSETS[direction][0]
                col = start_cell[1] +  step*OFFSETS[direction][1]
                temporary_list.append(self.grid[row][col])
            temporary = merge(temporary_list)
            if temporary != temporary_list:
                changed = True
            
 
            for step in range(iter_param):
                row = start_cell[0] +  step*OFFSETS[direction][0]
                col = start_cell[1] +  step*OFFSETS[direction][1]       
                self.grid[row][col] = temporary[step]
        if changed:        
            self.new_tile()
       


    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        finished = False
        while not finished:
            
            x_index1 = random.randrange(self.grid_height)
            y_index1 = random.randrange(self.grid_width)
            if self.grid[x_index1][y_index1] == 0:
                self.grid[x_index1][y_index1] = random_pick_odd([2,4],[9,1])
                finished = True
         
                


    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self.grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

