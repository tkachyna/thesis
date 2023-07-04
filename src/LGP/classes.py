#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: classes.py
    author: Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 8/5/2023
    brief: This folder contains classes to represent individuals and instructions and their methods.
"""
import numpy as np

class Instruction:
    """Represents instuctions in individuals"""

    def __init__(self, data, label=False, fnc=False, symb=None):
        self.data = data
        self.label = label  # whether instruction does not preforms an operation nor not, default set to False
        self.fnc = fnc  # whether instruction is a fuction or terminal, default set to False
        self.symb = symb


    def set_inst(self, data, fnc=False):
        self.data = data
        self.fnc = fnc


class Individual:
    """Represents individuals in population"""
    instructions = []

    def __init__(self):
        self.fitness = 0
        self.trail = [[0,0]]
        self.ant = { 'pos': [0,0], 'dir': 'right' }
        self.instructions = []


    def reset_ant_info(self):
        self.trail = [[0,0]]
        self.ant = { 'pos': [0,0], 'dir': 'right' }


    def set_ant_info(self, trail, ant):
        self.trail = trail
        self.ant = ant


    def insert_inst(self, instruction):
        """Inserts instruction at the end of the program"""
        self.instructions.append(instruction)
        

    def get_fitness(self):
        """Returns value of the fitness"""
        return self.fitness


    def set_fitness(self, fitness):
        """Sets the fitness's value"""
        self.fitness = fitness


    def get_length(self):
        """Returns length of the whole program including subroutines"""
        return len(self.instructions)


    def get_length_main_program(self):
        """Gets the length of the main program

        Returns:
            int: length
        """
        length = 0
        inst_ord = 0
        while not self.instructions[inst_ord].label:
            length += 1
            if self.instructions[inst_ord+1] == self.instructions[-1]: break
            inst_ord += 1
        
        return length

    def get_length_subroutine(self, subroutine):
        """Gets the length of the subroutine

        Args:
            subroutine (int): number of subroutine 

        Returns:
            int: length
        """
        length = 0
        inst_ord = self.get_first_inst_subroutine(subroutine) + 1  # position
        while not self.instructions[inst_ord].label:
            length += 1
            if self.instructions[inst_ord] == self.instructions[-1]: # if this is the last instruction
                break
            inst_ord += 1
    
        return length

    def get_first_inst_subroutine(self, subroutine):
        """Gets the position of the first instruction of the subroutine

        Args:
            subroutine (int): number of subroutine 

        Returns:
            int: position
        """
        subroutines_dict = {
            1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F',
            7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L',
            13: 'M', 14: 'N'
        }

        inst_ord = 1  # starts indexing from number one 
        while(self.instructions[inst_ord].data != ('* SR ' + subroutines_dict[subroutine] + ":")):
            inst_ord += 1
        
        return inst_ord
    
    def count_fitness(self, array):
        """ Fitness function, which counts number of ones present in the arrat

        Args:
            ant_path (array): ant's path
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