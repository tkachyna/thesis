#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: print_stats.py
    author: Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 7/5/2023
    brief: this file contains statistics functions
"""

import numpy as np
from gif import create_gif
from init_params import CREATE_GIF, COMPLEX_OUTPUT
from trails_plots import plot_result_trail, print_program


def print_stats_gen_avg_fitness(gen, fitnesses):
    """Prints number of average fitness (-> of all individuals) of each generation """
    
    print("Generation: " + str(gen) + " > Average Fitness: " + str(np.average(fitnesses)))


def print_best_of_run(best_of_run):
    """Prints the visualization and fitness value about current best run individual"""
    
    print("_________________________________________________")
    plot_result_trail(best_of_run['path'])
    print("\n_________________________________________________\nFittest individual attained at generation "\
           + str(best_of_run['gen']) + " and has fitness=" + str(best_of_run['fitness']))


def print_final_results(fitnesses, best_of_run):
    cell = None
    result_trail = []
    for pair in best_of_run['path']:
        if not pair == cell:
            result_trail.append(pair)
        cell = pair

    print("\n" + "** FINAL RESULTS --------------------------------------------" + "\n")
    print("** Ant's Final Trail Visualisation:")
    plot_result_trail(result_trail)
    print("\n" + "**  Solution Representation:" + "\n")
    print_program(best_of_run['individual'])
    print("\n" + "** Solution Info: " + "\n")
    print("> Gen > " + str(best_of_run['gen']))
    print("> Fitness > " + str(best_of_run['fitness']))
    print("> Trail > " + str(best_of_run['path']))
    print("> Trail Length > " + str(len(best_of_run['path'])))
    print(" ::: ")
    print("> Best Fitnesses > " + str(sorted(list(set(fitnesses['best_gen'])), reverse=True)))
    print("> Gen Best Fitnesses > " + str(fitnesses['best_gen']))
    print("> Gen Average Fitnesses > " + str(fitnesses['avg_gen']))
    print("> Gen Worst Fitnesses > " + str(fitnesses['worst_gen']))
    print(" ::: ")
    print(" --------------------------------------------------")

    best_solution = False
    if best_of_run['fitness'] == 0:
        best_solution = True
    if CREATE_GIF == True:
        create_gif(best_of_run['path'], best_solution)
    elif CREATE_GIF == 'ASK':
        answer = input("Do you want to create an animation (gif)? [yes(y)/no]")
        if answer == ('y' or 'yes'):
            create_gif(best_of_run['path'], best_solution)

    if COMPLEX_OUTPUT:
        f = open("./results/results.txt", "a")

        f.write("RUN -----------------------------------------------" + "\n")
        f.write("Solution Info: " + "\n")
        f.write("> Found at Gen > " + str(best_of_run['gen']) + "\n")
        f.write("> Best Fitness > " + str(best_of_run['fitness']) + "\n")
        f.write("> Trail > " + str(best_of_run['path']) + "\n")
        f.write("> Trail Length > " + str(len(best_of_run['path'])) + "\n")
        f.write(" ::: " + "\n")
        f.write("> Best Fitnesses > " + str(sorted(list(set(fitnesses['best_gen'])), reverse=True)))
        f.write("> Gen Best Fitnesses > " + str(fitnesses['best_gen']) + "\n")
        f.write("> Gen Average Fitnesses > " + str(fitnesses['avg_gen']) + "\n")
        f.write("> Gen Worst Fitnesses > " + str(fitnesses['worst_gen']) + "\n")
        f.write(" ::: " + "\n")
        f.write(" --------------------------------------------------" + "\n")

        f.close()