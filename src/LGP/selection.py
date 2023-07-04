#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: selection.py
    author: Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 8/5/2023
    brief: The file comprises selection functions that select individuals to undergo 
           genetic operators such as crossover or mutation.
"""

from init_params import TOURNAMENT_SIZE
from random import randint, random, uniform
from copy import deepcopy


def tournament_selection(population):
    """
    A small sample of the population is selected and the fittest individual 
    is selected from it using a tournament. The selection pressure is adjustable 
    by the size of the selected sample of individuals.
    """
    # randomly select tournaments's participants by their position in the population
    tournament_participants = []
    for _ in range(TOURNAMENT_SIZE):
        participant = randint(0, len(population) - 1)
        tournament_participants.append(participant)
        
    tournament_individuals = []

    # select the individuals from the population
    for individual in tournament_participants:
        tournament_individuals.append(population[individual])

    # set the first individual as the winner 
    winner = tournament_individuals[0]

    # check for every individual's fitness
    for individual in tournament_individuals:
        # if it's fitness is better, set it as temp winner
        if individual.fitness < winner.fitness:
            winner = individual 

    return deepcopy(winner)


def roulette_selection(population, fitnesses, max_fitness):
    """
    Individuals in the population are assigned a portion of a roulette wheel based on 
    their fitness. The overall fitness of the roulette is the sum of all individuals' fitness. 
    An individual is selected at random by generating a number between 0 and 1 and selecting 
    the individual whose roulette portion contains that number.
    """
    # converts STANDARDIZED fitness to RAW fitness
    fitnesses = [max_fitness - f  for f in fitnesses]

    total_fitness = float(sum(fitnesses))
    # the for loop iterates over each element in fitnesses and divides it by total_fitness
    rel_fitness = []
    for f in fitnesses:
        rel_fitness.append(f / total_fitness)
    
    probs = []
    total = 0
    for i in range(len(rel_fitness)):
        total += rel_fitness[i]
        probs.append(total)
    
    selected_individual = []
    r = random()
    for (i, individual) in enumerate(population):
        if r < probs[i]:
            selected_individual = individual
            break
    
    # converts fitness back to STANDARDIZED
    fitnesses = [max_fitness - f  for f in fitnesses]

    return deepcopy(selected_individual)


def rank_selection(population):
    """
    Rank selection function that returns the selected parents for reproduction.
    The number of parents to be selected is specified by the 'num_parents' argument.
    """
    # assigns a rank to each individual in the population based on their fitness
    ranked_population = sorted(population, key=lambda x: x.fitness, reverse=True)
    ranks = []
    for i, ind in enumerate(ranked_population):
        ranks.append(i + 1)

    # calculates the total rank sum
    r_sum = 0
    for i in range(1, len(population) + 1):
        r_sum += i
    
    selected_individual = None
    rand_num = uniform(0, r_sum)
    
    # selects the parent corresponding to the random number generated
    partial_sum = 0
    for i, individual in enumerate(ranked_population):
        partial_sum += ranks[i]
        if partial_sum >= rand_num:
            selected_individual = deepcopy(individual)
            break

    return selected_individual