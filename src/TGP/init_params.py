#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: init_params.py
    author: Tadeas Kachyna, <xkachy00@fit.vutbr.cz>
    date: 8/5/2023
    brief: A file containing constans and initialization parameters.
"""
# set of allowed instructions
TERMINALS = ['LEFT', 'RIGHT', 'MOVE'] 
FUNCTIONS = ['PROGN2', 'PROGN3', 'IF_FOOD_AHEAD']

""" PROGRAM LENGTH'S PARAMS """
MIN_DEPTH = 3
MAX_DEPTH = 5

""" GENETIC PROGRAMMING PARAMS """
POP_SIZE = 300
GENS = 100 

""" GEN OP MUTATION PARAMS """
MUTATION_RATE = 0.1

""" GEN OP CROSSOVER PARAMS """
CROSSOVER_RATE = 0.7 

""" GEN OP SELECTION PARAMS """
TOURNAMENT_SIZE = 20

""" OTHER PARAMS """
COMPLEX_OUTPUT = True  # possible: True/False
CREATE_GIF = True  # possible: True/False/'ASK'
GRID_SIZE = 32  # need to be modified whenever changing the the trail in trails_plots.py
GRID = GRID_SIZE * GRID_SIZE 
MAX_TIME = 1000  # maximal time stopper, so it does not go into endless loop
MAX_ANT_TRAIL_LEN = 200  # maximal allowed length of ant's trail
POS_X = 0 
POS_Y = 1
