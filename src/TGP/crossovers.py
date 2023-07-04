#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: crossovers.py
    author: Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 8/5/2023
    brief: This file contains two different methods that try to deal with the bloat problem with the crossover operator.
"""

from copy import deepcopy
from random import randint
from init_params import MAX_DEPTH

def crossover_twice_mutation(parent1, parent2):
    """ Crossover of two trees with limited height MAX_HEIGHT

            Starts as the basic crossover, if the result is not acceptable,
            it runs the crossover again. If the result is not acceptable
            again, mutation is going to happen.

        Args:
            parent1 (GPTree): first parent
            parent2 (GPTree): second parent

        Returns:
            GPTree: offspring
        """
    copy_parent1  = deepcopy(parent1)
    copy_parent1_ = deepcopy(parent1)
    copy_parent2  = deepcopy(parent2)
   
    parent1.crossover(parent2) # FIRST crossover

    # check whether the FIRST offspring meets the limit requirements
    if parent1.height() > MAX_DEPTH:

        # if not, do the SECOND crossover
        copy_parent1.crossover(copy_parent2)

        # check whether the SECOND offspring meets the limit requirements
        if  copy_parent1.height() > MAX_DEPTH:
            
            # if not, do the MUTATION and eventually cut the tree
            copy_parent1_.mutation([randint(0, parent1.size())])
            copy_parent1_.align_tree()
            parent1 = deepcopy(copy_parent1_)

        else:
            parent1 = deepcopy(copy_parent1)

    return parent1
    
def crossover_and_cut(parent1, parent2):
    """Performs standard crossover and eventually align it
        to the maximum height if it does not meet the 
        limits.

    Args:
        parent1 (GPTree): first parent
        parent2 (GPTree): second parent

    Returns:
        GPTree: offspring
    """
    parent1.crossover(parent2)
    if parent1.height() > MAX_DEPTH:
        parent1.align_tree()

    return parent1
