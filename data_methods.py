"""
    This module provides various data management functions:
     - get_x_list               Returns List of all x-coordinates
     - get_y_list               Returns List of all y-coordinates
     - get_z_list               Returns List of all z-coordinates
     - generate_data_structure  Returns data structure (double list) based on dhm25/200
     - best_m_values_in_list    Returns a list with the best m elements from a given list
     - random_coords            Returns random coordinate tuple [x, y]
     - coords_to_index          Returns data structure indexes converted from given coordinates
     - get_fitness              Returns fitness (altitude) of a given x,y-location
"""

from random import *
import heapq

# Global vars
FILE_PATH = "./data/DHM200.xyz"


def get_x_list():
    """
    Reads the file given in FILE_PATH and extracts file coordinates
    :return: list with all x-coordinates
    """
    x_list = []
    with open(FILE_PATH, "r") as file:
        for line in file:
            temp_array = line.split()
            x_list.append(temp_array[0])

    return x_list


def get_y_list():
    """
    Reads the file given in FILE_PATH and extracts file coordinates
    :return: list with all y-coordinates
    """
    y_list = []
    with open(FILE_PATH, "r") as file:
        for line in file:
            temp_array = line.split()
            y_list.append(temp_array[1])

    return y_list


def get_z_list():
    """
    Reads the file given in FILE_PATH and extracts file coordinates
    :return: list with all z-coordinates
    """
    z_list = []
    with open(FILE_PATH, "r") as file:
        for line in file:
            temp_array = line.split()
            z_list.append(float(temp_array[2]))

    return z_list


def generate_data_structure():
    """
    Generates a double list (list in list) in order to quickly access height points with given [x,y]-coordinates.
    [[z(x1,y1), z(x2,y1),  ...]  [z(x1,y2), z(x2,y2), ...]
    :return: data structure
    """

    # Get coordinate lists
    x_list = get_x_list()
    y_list = get_y_list()
    z_list = get_z_list()

    # Set max y_coordinate
    y_max = 302000

    # Initialize vars
    data = []
    y = y_max
    i_start = 0
    i_end = 0
    sub_data = []
    length = len(x_list)

    while i_end < length:
        # Fill sub data with zeroes until first x-coord has a given altitude (case "before Switzerland")
        for m in range(0, int((float(x_list[i_start])-480000)/200)):
            sub_data.append(0)

        # Fill sub data with given altitudes for a given y-coord (case "in Switzerland")
        i = i_start
        while i < length and (float(y_list[i])) == y:
            i_end += 1
            i += 1
        for n in range(i_start, i_end+1):
            sub_data.append(z_list[n])

        # Fill sub data with zeroes until max length of 1925 (case "after Switzerland")
        for o in range(0, 1925-len(sub_data)):
            sub_data.append(0)

        # Prepare for next iteration
        data.append(sub_data)  # Add sub data list to full data list
        y -= 200  # Go to next y-coordinate
        i_start = i_end + 1  # set interval start index of to next x-cord in full list
        sub_data = []  # empty sub_data list

        # Break if at eof
        if i_start >= length - 1:
            break

    return data


def best_m_values_in_list(list, m):
    """
        Returns m best elements in a list with n elements
    :param list: List with n elements
    :param m:
    :return: m-best elements out of a given list
    """
    if m > len(list):
        print("ERROR in function best_m_values_in_list: m > n")
        return list

    return heapq.nlargest(m, list)


def random_coords():
    """
    Generates random coordinates
    :return: random coordinates as tupel [x, y]
    """
    # must be multiple of 200, so [480'000/200, 865'000/200] -> randint*200
    x = randint(2400, 4325) * 200
    # must be multiple of 200, so [74'000/200, 302'000/200] -> randint*200
    y = randint(370, 1510) * 200

    return [x, y]


def coords_to_index(x, y):
    """
    Converts given coordinates to corresponding indexes in data structure for data structure altitude evaluation.
    :param x: x-coordinate
    :param y: y-coordinate
    :return: (x,y)-index
    """

    x_index = int((x - 480000) / 200)
    y_index = int((302000 - y) / 200)

    return[x_index, y_index]


def get_fitness(data, x, y):
    """
    Evaluates data structure. x, y must be index, not coordinates! Use function coords_to_index(x, y) first.
    :param data: data structure
    :param x: x-index
    :param y: y-index
    :return: altitude (z)
    """

    if y >= len(data) - 1:
        return 0

    if x >= len(data[0]) - 1:
        return 0

    return float(data[y][x])
