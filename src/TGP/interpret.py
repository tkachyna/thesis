#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: interpret.py
    author: Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 21/4/2023
    brief: This file contains interpret for ant's trail.
"""

from copy import deepcopy
from init_params import GRID_SIZE, POS_X, POS_Y


def interpret_trail(tree, ant_params, ant_path, array):
    """Interprets ant's trail.

    Args:
        individual (Individual): program to be interpreted
        ant (dict): info about ant's position and direction
        trail (list): ant's trail
        array (array): 2d map
    """

    # gets current (non)terminal from a node in a tree
    current_data = str(getattr(tree, "data")) 

    # current ant's position
    x, y = ant_params['pos'][POS_X], ant_params['pos'][POS_Y]

    if "IF_FOOD_AHEAD" in current_data:
        food_ahead = 0

        if ant_params['dir'] == 'right' and not ant_params['pos'][POS_Y] == GRID_SIZE - 1:
            food_ahead = array[x][y + 1]

        if ant_params['dir'] == 'up' and not ant_params['pos'][POS_X] == 0:
            food_ahead = array[x - 1][y]

        if ant_params['dir'] == 'down' and not ant_params['pos'][POS_X] == GRID_SIZE - 1:
            food_ahead = array[x + 1][y]

        if ant_params['dir'] == 'left' and not ant_params['pos'][POS_Y] == 0:
            food_ahead = array[x][y - 1]

        if food_ahead:
             
            # ^ EXTENSION -- when an ant sees food in front of it, it eats it
            # ^ (activate by uncommenting the code paragraph below)
        
            # if ant_params['dir'] == 'up' and not ant_params['pos'][POS_X] == 0:
            #     ant_params['pos'][POS_X]= x-1

            # elif ant_params['dir'] == 'right' and not ant_params['pos'][POS_Y] == GRID_SIZE-  1:
            #     ant_params['pos'][POS_Y]= y+1

            # elif ant_params['dir'] == 'down' and not ant_params['pos'][POS_X] == GRID_SIZE - 1:
            #     ant_params['pos'][POS_X]= x+1

            # if ant_params['dir'] == 'left' and not ant_params['pos'][POS_Y] == 0:
            #     ant_params['pos'][POS_Y] = y-1

            # if ant_params['pos'] != ant_path[-1]:
            #     ant_path.append(deepcopy(ant_params['pos']))

            ant_params, ant_path = interpret_trail(tree.left, ant_params, ant_path, array)

        else:
            ant_params, ant_path = interpret_trail(tree.right, ant_params,ant_path, array)

        return ant_params, ant_path

    elif "PROGN2" in current_data:

        ant_params, ant_path = interpret_trail(tree.left, ant_params, ant_path, array)
        ant_params, ant_path = interpret_trail(tree.right, ant_params, ant_path, array)

        return ant_params, ant_path
    
    elif "PROGN3" in current_data:

        ant_params, ant_path = interpret_trail(tree.left, ant_params, ant_path, array)
        ant_params, ant_path = interpret_trail(tree.middle, ant_params, ant_path, array)
        ant_params, ant_path = interpret_trail(tree.right, ant_params, ant_path, array)

        return ant_params, ant_path

    # the ant turns 90° clockwise on the spot
    elif "RIGHT" in current_data:

        if ant_params['dir'] == 'up':      ant_params['dir'] = 'right'
        elif ant_params['dir'] == 'right': ant_params['dir'] = 'down'
        elif ant_params['dir'] == 'down':  ant_params['dir'] = 'left'
        elif ant_params['dir'] == 'left':  ant_params['dir'] = 'up'

        return ant_params, ant_path

    # the ant turns 90° counterclockwise on the spot
    elif "LEFT" in current_data:

        if ant_params['dir'] == 'up':      ant_params['dir'] = 'left'
        elif ant_params['dir'] == 'right': ant_params['dir'] = 'up'
        elif ant_params['dir'] == 'down':  ant_params['dir'] = 'right'
        elif ant_params['dir'] == 'left':  ant_params['dir'] = 'down'

        return ant_params, ant_path

    elif "MOVE" in current_data:

        if ant_params['dir'] == 'up' and not ant_params['pos'][POS_X] == 0:
            ant_params['pos'][POS_X]= x - 1

        elif ant_params['dir'] == 'right' and not ant_params['pos'][POS_Y] == GRID_SIZE - 1:
            ant_params['pos'][POS_Y]= y + 1

        elif ant_params['dir'] == 'down' and not ant_params['pos'][POS_X] == GRID_SIZE-  1:
            ant_params['pos'][POS_X]= x + 1

        if ant_params['dir'] == 'left' and not ant_params['pos'][POS_Y] == 0:
            ant_params['pos'][POS_Y] = y - 1

        if ant_params['pos'] != ant_path[-1]:
            ant_path.append(deepcopy(ant_params['pos']))

        return ant_params, ant_path

    # ^ EXTENSION -- JUMP instruction
    # ^ (activate by uncommenting the code paragraph below and adding
    # ^ instruction to list of instructions in init_params.py)

    # elif "JUMP" in current_data:

    #     if ant_params['dir'] == 'up' and not ant_params['pos'][0] < 2:
    #         ant_params['pos'][0]= x-2

    #     elif ant_params['dir'] == 'right' and not ant_params['pos'][1] >= GRID_SIZE-2:
    #         ant_params['pos'][1]= y+2

    #     elif ant_params['dir'] == 'down' and not ant_params['pos'][0] >= GRID_SIZE-2:
    #         ant_params['pos'][0]= x+2

    #     elif ant_params['dir'] == 'left' and not ant_params['pos'][1] < 2:
    #         ant_params['pos'][1] = y-2

    #     ant_path.append(copy(ant_params['pos']))

    #     return ant_params, ant_path