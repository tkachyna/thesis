#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: tree.py
    author: Moshe Sipper (see https://github.com/moshesipper), 
            edited and modified by Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 9/5/2023
    brief: This file contains a tree structure class representing GP programs and their methods.
"""

#                               CREDITS AND LICENSE TERMS                                #
#    This software (applies mainly for this file) is based on Tiny genetic programming   #
#    by © Moshe Sipper, available on github: https://github.com/moshesipper/tiny_gp,     #
#    and provided under the terms of the GNU GENERAL PUBLIC LICENSE,                     #
#    see https://www.gnu.org/licenses/gpl-3.0.txt                                        #

import numpy as np
from random import random, randint
from init_params import MIN_DEPTH, MAX_DEPTH, TERMINALS, FUNCTIONS


class GPTree:
    """
    This class contains the definition of a tree structure representing 
    individual candidate solutions in the population.
    """

    def __init__(self, data = None, left = None, middle = None, right = None):
        self.data  = data  # holds node's instruction
        self.left  = left  # reference to left sub-tree
        self.middle = middle  # reference to mid sub-tree
        self.right = right  # reference to right sub-tree
        self.fitness = 0 
        self.trail = [[0,0]]
        self.ant = { 'pos': [0,0], 'dir': 'right' } # holds ant's position and direction in 2d matrix


    def reset_ant_info(self):
        """ 
        Resets information about ant's position and direction.
        """
        self.trail = [[0,0]]
        self.ant = { 'pos': [0,0], 'dir': 'right' }


    def random_tree(self, grow, max_depth, depth = 0, mutation = False):
        """Creates random tree using either grow or full method

        Args:
            grow (bool): if set to true, grow method is turned on, else full method
            max_depth (int): max depth of generated tree
            depth (int, optional): curent depth of the tree, defaults set to 0
        """
        if not mutation and (depth < MIN_DEPTH or (depth < max_depth and not grow)): 
                self.data = FUNCTIONS[randint(0, len(FUNCTIONS)-1)]
                
        elif depth >= max_depth:   
                self.data = TERMINALS[randint(0, len(TERMINALS)-1)]

        else: # intermediate depth, grow
            if random () > 0.5: 
                self.data = TERMINALS[randint(0, len(TERMINALS)-1)]
            else:
                self.data = FUNCTIONS[randint(0, len(FUNCTIONS)-1)]

        # if function is chosen, create subt-rees
        if self.data in FUNCTIONS:

            self.left = GPTree() # left sub-tree         
            self.left.random_tree(grow, max_depth, depth = depth + 1)            
            self.right = GPTree() # right subt-tree
            self.right.random_tree(grow, max_depth, depth = depth + 1)
        
            if self.data in ['PROGN3']:
                self.middle = GPTree() # middle sub-tree
                self.middle.random_tree(grow, max_depth, depth = depth + 1)  


    def size(self):
        """Counts size of the tree.

        Returns:
            int: size
        """
        if self.data in TERMINALS: return 1

        l = self.left.size() if self.left else 0
        m = self.middle.size() if self.middle else 0
        r = self.right.size() if self.right else 0

        return 1 + l + r + m


    def height(self):
        """Counts height of the tree.

        Returns:
            int: height
        """
        left, middle, right = 0, 0, 0
        if self == None: return 0    

        if self.left: left = self.left.height()
        if self.middle: middle = self.middle.height()
        if self.right: right = self.right.height()

        return max(left, middle, right) + 1


    def print_tree(self, prefix = "", depth = 0):
        """Prints the tree.

        Args:
            prefix (str, optional): visual ascii prefix, defaults set to ""
            depth (int, optional): depth of the tree
        """
        print("%s|-%s" % (prefix, self.data))    
        if self.data in ['PROGN2', 'IF_FOOD_AHEAD']:   
            if self.left: self.left.print_tree (prefix + "   ", depth = depth + 1)
            if self.right: self.right.print_tree(prefix + "   ", depth = depth + 1)
        elif self.data == 'PROGN3':   
            if self.left: self.left.print_tree (prefix + "   ", depth = depth + 1)
            if self.middle: self.middle.print_tree (prefix + "   ", depth = depth + 1)
            if self.right: self.right.print_tree(prefix + "   ", depth = depth + 1)

    def build_subtree(self):
        t = GPTree()
        t.data = self.data
        if self.left: t.left = self.left.build_subtree()
        if self.middle: t.middle = self.middle.build_subtree()
        if self.right: t.right = self.right.build_subtree()
        return t


    def scan_tree(self, count, second):  # note: count is list, so it's passed "by reference"
        count[0] -= 1
        if count[0] <= 1:
            if not second: # return subtree rooted here
                return self.build_subtree()
            else: # glue subtree here
                self.data = second.data
                self.left = second.left
                self.middle = second.middle
                self.right = second.right
                return self.build_subtree()
        else:
            ret = None
            if self.left and count[0] > 1: ret = self.left.scan_tree(count, second)
            if self.middle and count[0] > 1: ret = self.middle.scan_tree(count, second)
            if self.right and count[0] > 1: ret = self.right.scan_tree(count, second)
            return ret
    
    def align_tree(self, depth = 0):
        """When maximal depth is exceeded, the tree is aligned with terminal symobls
        
        Args:
            depth (int): depth of the tree
        """

        # when reaches maximal depth, asks whether the current data are terminals
        # if not, set it to a random chosen terminal symbol and set references to
        # sub-trees to None
        if depth == MAX_DEPTH - 1:
            if not self.data in TERMINALS:
                self.data = TERMINALS[randint(0, len(TERMINALS)-1)]
            self.left = None
            self.middle = None
            self.right = None
            return
        
        # else just travel recursively in the tree
        else:
            ret = None
            if self.left: self.left.align_tree(depth + 1)
            if self.middle: self.middle.align_tree(depth + 1)
            if self.right: self.right.align_tree(depth + 1)
            return ret


    def crossover(self, other):
        """Crossover variation operator with choosing random point in each parent

        Args:
            other (GPTree): second parent, the first parent is "self"
        """

        cross_point = randint(1, other.size())  # choose cross-point in second parent
        second = other.scan_tree([cross_point], None) # return the part of the second tree after cross-point

        cross_point2 = randint(1, self.size())  # select cross-point in the first tree
        # glue the part of the "second" tree to this one and create new offspring
        self.scan_tree([cross_point2], second)  


    def mutation(self, mut_point):
        """Mutation variation operator randomly choosing a point in the tree and then 
        performs mutation with the maximal depth of 2 in the new subtree

        Args:
            mut_point (int): mutation point in the tree
        """

        mut_point[0] -= 1  # decrement mutation point by one

        if mut_point[0] <= 1:  # perform mutation
            self.random_tree(grow=True, max_depth=2, mutation=True)

        else: # else recursively search the tree
            ret = None
            if self.left and mut_point[0] > 1: ret = self.left.mutation(mut_point)
            if self.middle and mut_point[0] > 1: ret = self.middle.mutation(mut_point)
            if self.right and mut_point[0] > 1: ret = self.right.mutation(mut_point)
            return ret

    def count_fitness(self, array):
        """ Fitness function, which counts number of ones (1) present in the array

        Args:
            individual (GPTree): the tree 
            ant_path (array): ant's trail
            array (array): food tiles

        Returns:
            int: fitness value
        """
        fitness_value = None

        for point in self.trail:
            array[point[0]][point[1]] = 2
        fitness_value = np.count_nonzero(array == 1)
        self.fitness = fitness_value  

        return fitness_value