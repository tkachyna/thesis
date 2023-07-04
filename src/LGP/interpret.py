#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: interpret.py
    author: Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 14/4/2023
    brief: This component contains an algorithm to interpret the ant's trail.
"""
from copy import deepcopy
from init_params import GRID_SIZE, POS_X, POS_Y


def interpret_trail(individual, ant, trail, array):
    """Interprets ant's trail.

    Args:
        individual (Individual): program to be interpreted
        ant (dict): info about ant's position and direction
        trail (list): ant's trail
        array (array): 2d map
    """

    list_of_instructions = individual.instructions
    subroutine_ex = False
    callback_pos = None  # callback position after execution of subroutine

    # sequentially executing instructions
    i = 0
    while i < len(list_of_instructions):

        instruction = list_of_instructions[i]
        insdata = instruction.data
        x = ant['pos'][POS_X]
        y = ant['pos'][POS_Y]

        if insdata[:2] == 'IF':
            food_ahead = False

            # checking the position of the ant and the border of the grid
            if ant['dir'] == 'right' and not ant['pos'][POS_Y] == GRID_SIZE - 1:
                food_ahead = array[x][y + 1]
            if ant['dir'] == 'up' and not ant['pos'][POS_X] == 0:
                food_ahead = array[x - 1][y]
            if ant['dir'] == 'down' and not ant['pos'][POS_X] == GRID_SIZE - 1:
                food_ahead = array[x + 1][y]
            if ant['dir'] == 'left' and not ant['pos'][POS_Y] == 0:
                food_ahead = array[x][y - 1]

            data = instruction.data.split() # [IF, FOOD_AHEAD, ?, E, :, B]
            # [E, B] ... zero index = true opt, first index = false opt

            # decoding the 'data'
            # ternary operator is true
            if food_ahead:
                # just simple instruction 
                if data[3] in ['LEFT', 'RIGHT', 'MOVE', '2XMOVE']:
                    insdata = data[3]
                # or subroutine
                else:   
                    for count, inst in enumerate(individual.instructions):
                        if inst.data == "* SR " + data[3] + ":":
                            # saving the positions
                            callback_pos = i
                            i = count
                            # program is going to jump to subroutine's label
                            subroutine_ex = True
                            break    

            # ternary operator is false             
            else: 
                # just simple instruction
                if data[5] in ['LEFT', 'RIGHT', 'MOVE', '2XMOVE']:
                    insdata = data[5]
                # or subroutine
                else:   
                    for count, inst in enumerate(individual.instructions):
                        if inst.data == "* SR " + data[5] + ":":
                            # saving the positions
                            callback_pos = i
                            i = count
                            # program is going to jump to subroutine's label
                            subroutine_ex = True
                            break

        if insdata == 'RIGHT':
            if ant['dir'] == 'up':      ant['dir'] = 'right'
            elif ant['dir'] == 'right': ant['dir'] = 'down'
            elif ant['dir'] == 'down':  ant['dir'] = 'left'
            elif ant['dir'] == 'left':  ant['dir'] = 'up'

        if insdata == 'LEFT':
            if ant['dir'] == 'up':      ant['dir'] = 'left'
            elif ant['dir'] == 'right': ant['dir'] = 'up'
            elif ant['dir'] == 'down':  ant['dir'] = 'right'
            elif ant['dir'] == 'left':  ant['dir'] = 'down'

        if insdata == 'MOVE':
            if ant['dir'] == 'up':
                if not ant['pos'][POS_X] == 0:
                    ant['pos'][POS_X]= x - 1
                else: 
                    ant['dir'] = 'right'

            elif ant['dir'] == 'right':
                if not ant['pos'][POS_Y] == GRID_SIZE - 1:
                    ant['pos'][POS_Y]= y + 1
                else:
                    ant['dir'] = 'down'

            elif ant['dir'] == 'down':
                if not ant['pos'][POS_X] == GRID_SIZE - 1:
                    ant['pos'][POS_X]= x + 1
                else:
                    ant['dir'] = 'left'

            if ant['dir'] == 'left':
                if not ant['pos'][POS_Y] == 0:
                    ant['pos'][POS_Y] = y - 1
                else:
                    ant['dir'] = 'right'
                    
            trail.append(deepcopy(ant['pos']))

        # ? Expansion 2XMOVE
        if insdata == '2XMOVE':
            first_move = None

            if ant['dir'] == 'up' and ant['pos'][POS_X] > 1:
                first_move = x - 1
                ant['pos'][POS_X] = x - 2

            elif ant['dir'] == 'right' and ant['pos'][POS_Y] < GRID_SIZE-2:
                first_move = y + 1
                ant['pos'][POS_Y] = y + 2

            elif ant['dir'] == 'down' and ant['pos'][POS_X] < GRID_SIZE-2:
                first_move = x + 1
                ant['pos'][POS_X] = x + 2

            if ant['dir'] == 'left' and ant['pos'][POS_Y] > 1:
                first_move = y - 1
                ant['pos'][POS_Y] = y - 2

            trail.append(deepcopy(first_move))
            trail.append(deepcopy(ant['pos']))

        # when subroutine is executed
        if subroutine_ex: 
            # check for the end of it, whether it is end of the whole program
            # or another subroutine
            if  individual.instructions[i] == individual.instructions[-1] \
                or individual.instructions[i+1].data[0] == '*':
                i = callback_pos
                callback_pos = None
                subroutine_ex = False

        # same as with subroutines but for the main program
        if not subroutine_ex and \
           (individual.instructions[i] == individual.instructions[-1] \
            or individual.instructions[i+1].data[0] == '*'):
            break

        i = i + 1