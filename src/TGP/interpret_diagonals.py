#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: interpret_diagonals.py
    author: Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 21/4/2023
    brief: This file contains interpret for ant's trail with diagonals motion.
"""

from copy import deepcopy
from init_params import GRID_SIZE, POS_X, POS_Y

def interpret_trail(tree, ant, trail, array):
    """Interprets ant's trail diagonally.

    Args:
        individual (Individual): program to be interpreted
        ant (dict): info about ant's position and direction
        trail (list): ant's trail
        array (array): 2d map
    """

    # gets current (non)terminal from a node in a tree
    current_data = str(getattr(tree, "data")) 

    # current ant's position
    x, y = ant['pos'][POS_X], ant['pos'][POS_Y]

    if "IF_FOOD_AHEAD" == current_data:
        food_ahead = 0

        if ant['dir'] == 'right' and not ant['pos'][POS_Y] == GRID_SIZE - 1:
            food_ahead = array[x][y + 1]

        if ant['dir'] == 'up' and not ant['pos'][POS_X] == 0:
            food_ahead = array[x - 1][y]

        if ant['dir'] == 'down' and not ant['pos'][POS_X] == GRID_SIZE - 1:
            food_ahead = array[x + 1][y]

        if ant['dir'] == 'left' and not ant['pos'][POS_Y] == 0:
            food_ahead = array[x][y - 1]

        if ant['dir'] == 'up-right' and not (ant['pos'][POS_Y] == GRID_SIZE-1 or ant['pos'][POS_X] == GRID_SIZE-1):
            food_ahead = array[x - 1][y + 1]

        if ant['dir'] == 'up-left' and not (ant['pos'][POS_Y] == 0 or ant['pos'][POS_X] == 0):
            food_ahead = array[x - 1][y - 1]

        if ant['dir'] == 'down-right' and not (ant['pos'][POS_Y] == GRID_SIZE-1 or ant['pos'][POS_X] == GRID_SIZE-1):
            food_ahead = array[x + 1][y + 1]

        if ant['dir'] == 'down-left' and not (ant['pos'][POS_X] == GRID_SIZE-1 or ant['pos'][POS_Y] == 0):
            food_ahead = array[x+  1][y - 1]

        if food_ahead == 1:
            ant, trail = interpret_trail(tree.left, ant, trail, array)

        else:
            ant, trail = interpret_trail(tree.right, ant,trail, array)

        return ant, trail

    elif "PROGN2" == current_data:

        ant, trail = interpret_trail(tree.left, ant, trail, array)
        ant, trail = interpret_trail(tree.right, ant, trail, array)

        return ant, trail
    
    elif "PROGN3" == current_data:

        ant, trail = interpret_trail(tree.left, ant, trail, array)
        ant, trail = interpret_trail(tree.middle, ant, trail, array)
        ant, trail = interpret_trail(tree.right, ant, trail, array)

        return ant, trail

    # the ant turns 45° or 90° clockwise on the spot
    elif "RIGHT" == current_data:

        if   ant['dir'] == 'up':         ant['dir'] = 'right'
        elif ant['dir'] == 'up-right':   ant['dir'] = 'right'
        elif ant['dir'] == 'right':      ant['dir'] = 'down'
        elif ant['dir'] == 'down-right': ant['dir'] = 'down'
        elif ant['dir'] == 'down':       ant['dir'] = 'left'
        elif ant['dir'] == 'down-left':  ant['dir'] = 'left'
        elif ant['dir'] == 'left':       ant['dir'] = 'up'
        elif ant['dir'] == 'up-left':    ant['dir'] = 'up'

        return ant, trail

    # the ant turns 45° or 90° counterclockwise on the spot
    elif "LEFT" == current_data:

        if   ant['dir'] == 'up':         ant['dir'] = 'left'
        elif ant['dir'] == 'up-left':    ant['dir'] = 'left'
        elif ant['dir'] == 'left':       ant['dir'] = 'down'
        elif ant['dir'] == 'down-left':  ant['dir'] = 'down'
        elif ant['dir'] == 'down':       ant['dir'] = 'right'
        elif ant['dir'] == 'down-right': ant['dir'] = 'right'
        elif ant['dir'] == 'right':      ant['dir'] = 'up'
        elif ant['dir'] == 'up-right':   ant['dir'] = 'up'

        return ant, trail

    # ^ this instruction needs to be added to instruction list in init_params.py
    # the ant turns 45° clockwise on the spot
    elif "RIGHT+" == current_data:

        if   ant['dir'] == 'up':         ant['dir'] = 'up-right'
        elif ant['dir'] == 'up-right':   ant['dir'] = 'right'
        elif ant['dir'] == 'right':      ant['dir'] = 'down-right'
        elif ant['dir'] == 'down-right': ant['dir'] = 'down'
        elif ant['dir'] == 'down':       ant['dir'] = 'down-left'
        elif ant['dir'] == 'down-left':  ant['dir'] = 'left'
        elif ant['dir'] == 'left':       ant['dir'] = 'up-left'
        elif ant['dir'] == 'up-left':    ant['dir'] = 'up'

        return ant, trail

    # ^ this instruction needs to be added to instruction list in init_params.py
    # the ant turns 45° counterclockwise on the spot
    elif "LEFT+" == current_data:

        if   ant['dir'] == 'up':         ant['dir'] = 'up-left'
        elif ant['dir'] == 'up-left':    ant['dir'] = 'left'
        elif ant['dir'] == 'left':       ant['dir'] = 'down-left'
        elif ant['dir'] == 'down-left':  ant['dir'] = 'down'
        elif ant['dir'] == 'down':       ant['dir'] = 'down-right'
        elif ant['dir'] == 'down-right': ant['dir'] = 'right'
        elif ant['dir'] == 'right':      ant['dir'] = 'up-right'
        elif ant['dir'] == 'up-right':   ant['dir'] = 'up'

        return ant, trail

    elif "MOVE" == current_data:
        if ant['dir'] == 'up' and not ant['pos'][POS_X] == 0:
            ant['pos'][POS_X]= x - 1

        elif ant['dir'] == 'right' and not ant['pos'][POS_Y] == GRID_SIZE - 1:
            ant['pos'][POS_Y]= y + 1

        elif ant['dir'] == 'down' and not ant['pos'][POS_X] == GRID_SIZE - 1:
            ant['pos'][POS_X]= x + 1

        elif ant['dir'] == 'left' and not ant['pos'][POS_Y] == 0:
            ant['pos'][POS_Y] = y - 1

        elif ant['dir'] == 'up-right' and not (ant['pos'][POS_Y] == GRID_SIZE - 1 or ant['pos'][POS_X] == 0):
            ant['pos'][POS_X]= x - 1
            ant['pos'][POS_Y]= y + 1

        elif ant['dir'] == 'up-left' and not (ant['pos'][POS_Y] == 0 or ant['pos'][POS_X] == 0):
            ant['pos'][POS_X]= x - 1
            ant['pos'][POS_Y]= y - 1

        elif ant['dir'] == 'down-right' and not (ant['pos'][POS_Y] == GRID_SIZE - 1 or ant['pos'][POS_X] == GRID_SIZE - 1):
            ant['pos'][POS_X]= x + 1
            ant['pos'][POS_Y]= y + 1

        elif ant['dir'] == 'down-left' and not (ant['pos'][POS_X] == GRID_SIZE - 1 or ant['pos'][POS_Y] == 0):
            ant['pos'][POS_X]= x + 1
            ant['pos'][POS_Y]= y - 1

        if ant['pos'] != trail[-1]:
            trail.append(deepcopy(ant['pos']))

        return ant, trail
