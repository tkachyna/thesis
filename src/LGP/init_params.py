#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: init_params.py
    author: Tadeas Kachyna, <xkachy00@fit.vutbr.cz>
    date: 8/5/2023
    brief: A file containing constants and initialization parameters.
"""

# set of allowed instructions
INSTRUCTION_LIST = ['LEFT', 'RIGHT', 'MOVE', 'IF FOOD_AHEAD ? '] 

""" PROGRAM LENGTH'S PARAMS """
MIN_PROGRAM_LENGTH    = 6  # must be > 0
MAX_PROGRAM_LENGTH    = 12
MAX_SUBROUTINE_LENGTH = 5
MIN_SUBROUTINE_LENGTH = 3  # must be > 0
MAX_SUBROUTINES       = 5  # must be > 0

INIT_TYPE = 'RANGE'  # MIN or MAX or CONST
INIT_PROGRAM_CONST = 5  # only if INIT_TYPE == 'CONST'

""" GENETIC PROGRAMMING PARAMS """
POP_SIZE = 1
GENS = 1

""" GEN OP MUTATION PARAMS """ 
MUTATION_RATE  = 0.5  # substituting one instruction for another
INSERTION_RATE = 0.5  # inserting instruction at the current position
DELETION_RATE  = 0.5  # deleting instruction at the current position
MICROMUT_RATE  = 0.5  # substituing parts of an instruction

""" GEN OP CROSSOVER PARAMS """
XO_RATE = 0.4

""" GEN OP SELECTION PARAMS """
TOURNAMENT_SIZE = 20

""" OTHER PARAMS """
GRID_SIZE = 32  # needs to be modified whenever changing the the trail in trails_plots.py
GRID = GRID_SIZE * GRID_SIZE
POS_X = 0
POS_Y = 1
SUBROUTINE_SYMBOLS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']  # maximum of 14 supported subroutines at the momemnt
COMPLEX_OUTPUT = True  # possible: True/False
CREATE_GIF = True  # possible: True/False/'ASK'
MAX_TIME = 1000  # maximal time stopper, so it does not go into endless loop
MAX_ANT_TRAIL_LEN = 200  # maximal allowed length of ant's trail
