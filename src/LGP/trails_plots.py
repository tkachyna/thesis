#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: trails_plots.py
    author: Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 7/5/2023
    brief: File with pre-defined trail and ascii plots.
"""

import numpy as np
from colored import fg
from random import randint
from init_params import GRID_SIZE, GRID, POS_X, POS_Y

# Santa Fe Trail
trail_santafe_32x32 = [
    [0,1], [0,2], [0,3], [1,3], [2,3], [3,3], [4,3], [5,3], [5,4], [5,5], [5,6], 
    [5,8], [5,9], [5,10], [5,11], [5,12], [6,12], [7,12], [8,12], [9,12],
    [11,12], [12,12], [13,12], [14,12], [17,12], [18,12], [19,12], [20,12], [21,12],
    [22,12], [23,12], [24,11], [24,10], [24,9], [24,8], [24,7], [24,4], [24,3], [25,1],
    [26,1], [27,1], [28,1], [30,2], [30,3], [30,4], [30,5], [29,7], [28,7], [27,8],
    [27,9], [27,10], [27,11], [27,12], [27,13], [27,14], [26,16], [25,16], [24,16],
    [21,16], [20,16], [19,16], [18,16], [15,17], [14,20], [13,20], [10,20], [9,20],
    [8,20], [7,20], [5,21], [5,22], [4,24], [3,24], [2,25], [2,26], [2,27], [3,29],
    [4,29], [6,29], [9,29], [12,29], [14,28], [14,27], [14,26], [15,23], [18,24],
    [19,27], [22,26], [23,23]]

trail_ownbuild_20x20 = [ # Trail C
    [0,1], [0,2], [0,3], [1,3], [2,3], [3,3], [4,3], [5,5], [5,6], [5,8], [5,9],
    [5,10], [5,11], [5,12], [6,12],  [7,12], [8,12], [9,12], [11,12],
    [14,12], [17,12], [19,12], [19,14], [19,15], [19,19], [17,19]]

trail_ownbuild_20x20_2 = [ # Trail B
    [0,1], [0,2], [0,3], [1,3], [2,3], [3,3], [4,3], [5,3], [5,4], [5,5], [5,6],
    [5,8], [5,9], [5,10], [5,11], [5,12], [6,12], [8,12], [9,12], [11,12],
    [14,12], [17,12], [19,12], [19,10], [19,9], [18,5], [18,6], [18,7], [16,5]]

# Random Trail S
trail_random_20x20 = [ 
    [5, 7], [8, 19], [1, 10], [11, 16], [8, 10], [14, 9], [15, 4], [16, 2], [18, 8], [0, 6], [2, 1], [19, 9]]


""" :::: CHOOSE TRAIL TO RENDER HERE :::: """
trail = trail_santafe_32x32
""" :::: --------------------------- :::: """


def generate_food():
    """Generates a certain number of cells with the food of a given lower and upper boundary
    
    Return:
       food_tiles (array): randomly filled array with food tiles
    """

    food_tiles = []
    down_limit = GRID // 20  # lower boundary
    upper_limit = GRID // 15  # upper boundary

    rand = randint(down_limit, upper_limit)  # choosing random number from that boundaries
    print("Number of food cells is: " + str(rand))

    # generates food tiles with random [x, y] position as many times as the number of rand
    for _ in range(rand): 
        food = np.random.choice(a=np.arange(0, GRID_SIZE), size=2, replace=False)
        food_tiles.append(food.tolist())
    
    # filles array of zero with those food tiles, which are represented by number one (!)
    array_filled_with_food = np.zeros((GRID_SIZE, GRID_SIZE))
    for piece_of_food in food_tiles:
        array_filled_with_food[piece_of_food[POS_X]][piece_of_food[POS_Y]] = 1
    print(array_filled_with_food)

    return food_tiles


def plot_food_trail():
    """Visualises chosen food trail"""

    # creates a 2d matrix filled with zeros
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    for cell in trail: # displays food in the matrix
        grid[cell[POS_X]][cell[POS_Y]] = 1
    print("Total number of food cells: " + str(len(trail)))

    # plotting 2d matrix in terminal
    for _ in range(GRID_SIZE):
        print(fg('white') + "__", end="")
    print(fg('white') + "__", end="")
    print("")

    for x in grid:
        print(fg('white') + "| ", end="")
        for y in x:
            if y == 0:
                print(fg('white') + ". ", end="")
            else:
                print(fg('green') + "O ", end="")
        print(fg('white') + "|", end="")
        print("")

    for _ in range(GRID_SIZE):
        print(fg('white') + "--", end="")
    print(fg('white') + "--", end="")
    print("")


def plot_result_trail(ants_trail):
    """Visualises chosen ant's trail """

    # creates a 2d matrix filled with zeros
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    for cell in trail:
        grid[cell[POS_X]][cell[POS_Y]] = 1
    for cell in ants_trail:
        grid[cell[POS_X]][cell[POS_Y]] = 2
    for x in range(GRID_SIZE):
        print(fg('white') +"__", end="")
    print(fg('white') + "__", end="")
    print("")

    for x in grid:
        print("| ", end="")
        for y in x:
            if y == 0:
                print(fg('white') + ". ", end="")
            elif y == 1:
                print(fg('green') + "O ", end="")
            else:
                print(fg('red') + "x ", end="")
        print(fg('white') + "|", end="")
        print("")

    for x in range(GRID_SIZE):
        print(fg('white') + "--", end="")
    print(fg('white') + "--", end="")
    print("")


def print_program(program):
    """Prints a program.

    Args:
        program (Individual): program to be printed
    """

    for inst in program.instructions:
        print(inst.data)
        