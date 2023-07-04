#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: gif.py
    author: Tadeas Kachyna, <xkachy00@fit.vutbr.cz>
    date: 8/5/2023
    brief: This file contains a function to create a gif animation and a function 
    to numerically sort the images needed for this animation.
"""
import os
import re
import trails_plots
import numpy as np
import imageio.v2 as imageio
from matplotlib import pyplot as plt
from matplotlib import colors
from init_params import GRID_SIZE, POS_X, POS_Y


def numerical_sort(list_to_sort):
    """Sorts the list of images numerically. First, using a regex expression, 
    the image number is extracted. Then tuples are created, which form a pair
    of the source string and the numeric value. These tuples are then serialized
    and then the first part of each tuple is extracted.

    Args:
        list_to_sort (list): list of images

    Returns:
        list: sorted list
    """
    regex = r'\d+' # regular expression

    # sometimes this item ranodmly appears, so in case of his presence, remove it
    if '.DS_Store' in list_to_sort:
        index = list_to_sort.index('.DS_Store')
        list_to_sort.pop(index)

    # creates the above mentioned tuples
    list_of_tuples = []
    for s in list_to_sort:
        match = int(re.findall(regex, s)[0])
        list_of_tuples.append((s, match))
    
    # sort the list by the number
    sorted_tuples = sorted(list_of_tuples, key=lambda x: x[1])
    
    # now when the list is sorted, extract the first part of the tuple
    sorted_list = []
    for t in sorted_tuples:
        sorted_list.append(t[0])
    
    return sorted_list


def create_gif(trail, solution_found=False):
    """A function to create a gif from given solution.

    Args:
        trail (list): ant's trail
        solution_found (bool, optional): If the best solution is found. Defaults to False.
    """

    # remove current images for image folder
    folder_path = './images'
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            os.remove(os.path.join(folder_path, filename))

    print("... creating a gif ...")
    data = np.zeros((GRID_SIZE, GRID_SIZE)) # generates a 2D matrix

    # just calculation of simple math percents for later use
    fifth = int(len(trail)/10) * 2 
    fifth_counter = 0

    for food_cell in trails_plots.trail_santafe_32x32:
        data[food_cell[POS_X]][food_cell[POS_Y]] = 1
        data[food_cell[POS_X]][food_cell[POS_Y]] = 1

    # starting color scheme
    cmap = colors.ListedColormap(['#EEECEF', '#84D52A','#ED2F2F'])
    
    for i, k in enumerate(trail):

        # informing about progress of creating gif, using that simple math i mentioned before
        if i % fifth == 0 and fifth_counter <= 5:
            print(str(10 * fifth_counter * 2) + " % of the trail processed.")
            fifth_counter += 1

        # changing palette scheme in time, having transitory colors from red to black
        if i == 1:
            cmap = colors.ListedColormap(['#EEECEF', '#84D52A',
                                          '#ED2F2F', '#BE2727'])
        if i == 2:
            cmap = colors.ListedColormap(['#EEECEF', '#84D52A',
                                          '#ED2F2F', '#BE2727','#8F1E1E'])
        if i == 3:
            cmap = colors.ListedColormap(['#EEECEF', '#84D52A','#ED2F2F',
                                          '#BE2727','#8F1E1E','#5F1111'])
        if i == 4:
            cmap = colors.ListedColormap(['#EEECEF', '#84D52A','#ED2F2F',
                                          '#BE2727','#8F1E1E','#5F1111', '#370A0A'])

        if i >= 4: data[trail[i - 4][POS_X]][trail[i - 4][POS_Y]] = 6  
        if i >= 3: data[trail[i - 3][POS_X]][trail[i - 3][POS_Y]] = 5
        if i >= 2: data[trail[i - 2][POS_X]][trail[i - 2][POS_Y]] = 4
        if i >= 1: data[trail[i - 1][POS_X]][trail[i - 1][POS_Y]] = 3
        data[k[POS_X]][k[POS_Y]] = 2

        # plotting the image
        plt.figure(figsize=(6,6))
        plt.pcolor(data[::-1],cmap=cmap,edgecolors='k', linewidths=1)
        plt.title("Langton's Ant Visualization\n")  
        plt.axis('off')
        plt.tight_layout()

        # saving the image
        fig_location = './images/IMG_'  + str(i) + '.png' 
        if fig_location:
            (dirname, filename) = os.path.split(fig_location)
            if dirname:  # create folder if doesnt exist
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
            plt.savefig(fig_location)
            plt.close()

    # if the optimal solution is found, make some special vis. effects at the end of the gif
    if solution_found:
        cmap = colors.ListedColormap(['#EEECEF', '#ED2F2F', '#ED2F2F'])
        data = np.zeros((GRID_SIZE, GRID_SIZE)) # generates a 2D matrix

        for food_cell in trail:
            data[food_cell[POS_X]][food_cell[POS_Y]] = 2
            data[food_cell[POS_X]][food_cell[POS_Y]] = 2

        # plot the image
        for i in range(3):
            plt.figure(figsize=(6,6))
            plt.pcolor(data[::-1],cmap=cmap,edgecolors='k', linewidths=1)
            plt.title("Langton's Ant Visualization\n")  
            plt.axis('off')
            plt.tight_layout()

            # saving the image
            fig_location = './images/IMG_'  + str(1000 + i) + '.png' 
            if fig_location:
                (dirname, filename) = os.path.split(fig_location)
                if dirname:  # create folder if doesnt exist
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)
                plt.savefig(fig_location)
                plt.close()

        for food_cell in trail:
            data[food_cell[POS_X]][food_cell[POS_Y]] = 2
            data[food_cell[POS_X]][food_cell[POS_Y]] = 2

    
    png_dir = './images'
    images = []

    # numerically sorting the images
    for file_name in numerical_sort((os.listdir(png_dir))):
        if file_name.endswith('.png'):
            file_path = os.path.join(png_dir, file_name)
            images.append(imageio.imread(file_path))

    # pause at the end
    for _ in range(20):
        images.append(imageio.imread(file_path))

    # creating gif
    print("... merging the pictures ...")
    imageio.mimsave('./gif/ant.gif', images, duration=0.05)
    print("... gif created ...")
