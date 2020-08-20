"""
    This module implements four different optimizer:
     - Brute Force
     - Pure Random Search
     - Hill Climbing
     - Particle Swarm Optimization
"""

import time
import data_methods as dm

from statistics import mean
from statistics import stdev
import matplotlib.pyplot as plt


def brute_force(data):
    """
    Evaluates fitness (altitude) for every location represented in the data structure
    :param data: data structure
    :return: highest altitude
    """
    # Initialize vars
    highest_altitude = 0
    len_y = len(data)
    len_x = len(data[0])

    # Loop through data structure
    for x in range(0, len_x):
        for y in range(0, len_y):
            fitness = dm.get_fitness(data, x, y)
            # Store highest altitude
            if fitness > highest_altitude:
                highest_altitude = fitness

    return highest_altitude


def pure_random_search(data, number_of_evaluations):
    """
    Evaluates the fitness (altitude) at a random location in the data structure. Repeats for a given number.
    :param data: data structure
    :param number_of_evaluations: How often the fitness of a random location is evaluated
    :return: highest altitude found
    """

    # Initialize vars
    highest_altitude = 0

    # Repeat evaluation process for given number
    for i in range(0, number_of_evaluations):
        # Get random coordinates
        coords = dm.random_coords()

        # Evaluate fitness (altitude)
        index = dm.coords_to_index(coords[0], coords[1])
        altitude = dm.get_fitness(data, index[0], index[1])

        # Store highest altitude
        if float(altitude) > highest_altitude:
            highest_altitude = float(altitude)

    return highest_altitude


def hill_climbing(data, restart):
    """
    Implementation of the Hill Climbing Optimizer.
    :param data: data structure
    :param restart: number of random restarts
    :return: highest altitude found
    """

    # Initialize vars
    highest_altitude = 0
    count_evaluations = 0

    # Do evaluation process for given number of random restarts. At least once.
    for i in range(0, restart + 1):

        # Initialize vars
        f_previous = 0

        # Get random coordinates for start point
        coords = dm.random_coords()
        x = coords[0]
        y = coords[1]

        # Evaluate fitness (altitude) of init point
        index = dm.coords_to_index(x, y)
        f_now = dm.get_fitness(data, index[0], index[1])

        # Count number of fitness evaluations
        count_evaluations += 1

        # Step to next point until a local (global) maximum is found
        while f_now > f_previous:

            # Initialize fitness for next step
            f_previous = f_now

            # Initialize four locations nearby the current location
            index_north = dm.coords_to_index(x, y + 200)
            index_east = dm.coords_to_index(x + 200, y)
            index_south = dm.coords_to_index(x, y - 200)
            index_west = dm.coords_to_index(x - 200, y)

            # Evaluate fitness at these four locations
            f_north = dm.get_fitness(data, index_north[0], index_north[1])
            f_east = dm.get_fitness(data, index_east[0], index_east[1])
            f_south = dm.get_fitness(data, index_south[0], index_south[1])
            f_west = dm.get_fitness(data, index_west[0], index_west[1])
            count_evaluations += 4

            # Check which one of these four locations is best
            fitness = [f_north, f_east, f_south, f_west]
            f_now = max(fitness)
            f_index = fitness.index(f_now)

            # Set location of the next step to the best location nearby the current position
            if f_index == 0:
                y += 200
            elif f_index == 1:
                x += 200
            elif f_index == 2:
                y -= 200
            elif f_index == 3:
                x -= 200

        # If during the current evaluation process a better altitude is found, store it.
        if f_previous > highest_altitude:
            highest_altitude = f_previous

    return [highest_altitude, count_evaluations]


def plot_swarm(positions):
    """
    Method for plotting the swarm.
    :param positions: Particle positions, coordinate list [[x1,y1], [x2,y2], ...]
    :return: None
    """

    # Initialize vars
    x = []
    y = []

    # convert all given coordinates to data structure indexes
    for element in positions:
        index = dm.coords_to_index(element[0], element[1])
        x.append(index[0])
        y.append(index[1])

    # Plot positions
    plt.xlim(0, 1925)
    plt.ylim(0, 1140)
    plt.scatter(x, y)
    time.sleep(0.1)
    plt.show()
    time.sleep(0.1)


def particle_swarm_optimization(data, number_of_particles, time_steps, v_inertia, v_best_global, v_best_local, v_swarm_center, enable_hc, number_of_hc_elements, plot_enable):
    """
    Implements the Particle Swarm Optimizer.
    :param data: data structure
    :param number_of_particles: How many particles are initialized for building a swarm
    :param time_steps: How often the particles move
    :param v_inertia: Base velocity
    :param v_best_global: velocity towards the global maximum
    :param v_best_local: velocity towards the local maximum
    :param v_swarm_center: velocity towards the swarm center
    :param enable_hc: enable hill climbing modification (True/False)
    :param number_of_hc_elements: number of elements which will do hill climbing (always the best ones will do it)
    :param plot_enable: enable if swarm is plotted at each time step (True/False)
    :return: highest altitude found
    """

    # Initialize vars
    positions = []
    pm_best = []
    fitness_list = []
    vm = [[0, 0]] * number_of_particles
    count_evaluations = 0

    # Convert steps to 200m-grid
    v_best_local *= 200
    v_best_global *= 200
    v_swarm_center *= 200

    # Initialize start positions
    for i in range(number_of_particles):
        init_position = dm.random_coords()
        positions.append(init_position)
        pm_best = positions

    # Evaluate fitness for start positions and set p_global
    for element in pm_best:
        index = dm.coords_to_index(element[0], element[1])
        fitness_list.append(dm.get_fitness(data, index[0], index[1]))
        count_evaluations += 1

    # Store the best fitness values in a list, needed for hill climbing modification
    best_fitness_values = dm.best_m_values_in_list(fitness_list, number_of_hc_elements)

    # Evaluate the currently best position and store as p_global
    best_fitness_index = fitness_list.index(max(fitness_list))
    p_global = pm_best[best_fitness_index]

    # Repeat the swarm process for a given number of time steps
    for m in range(time_steps):

        # Initialize vars
        fitness_list = []

        # Create a list with all current x and y coordinates from positions
        x_positions = []
        y_positions = []
        for element in positions:
            x_positions.append(element[0])
            y_positions.append(element[1])

        # Set new velocity and position for each element (particle)
        i = 0  # counter
        for element in positions:

            # Hill Climbing modification for a given number of best elements
            index = dm.coords_to_index(element[0], element[1])
            f_element = dm.get_fitness(data, index[0], index[1])
            count_evaluations += 1
            if enable_hc and f_element in best_fitness_values:
                # Current element position
                x = element[0]
                y = element[1]

                # Initialize four locations nearby the current location
                index_north = dm.coords_to_index(x, y + 200)
                index_east = dm.coords_to_index(x + 200, y)
                index_south = dm.coords_to_index(x, y - 200)
                index_west = dm.coords_to_index(x - 200, y)

                # Evaluate fitness at these four locations
                f_north = dm.get_fitness(data, index_north[0], index_north[1])
                f_east = dm.get_fitness(data, index_east[0], index_east[1])
                f_south = dm.get_fitness(data, index_south[0], index_south[1])
                f_west = dm.get_fitness(data, index_west[0], index_west[1])
                count_evaluations += 4

                # Check which one of these four locations is best
                fitness = [f_north, f_east, f_south, f_west]
                f_new = max(fitness)
                f_index = fitness.index(f_new)

                # Set location of the next step to the best location nearby the current position
                if f_index == 0:
                    y += 200
                elif f_index == 1:
                    x += 200
                elif f_index == 2:
                    y -= 200
                elif f_index == 3:
                    x -= 200

                # Choose new position if fitness is better there
                if f_new > f_element:
                    positions[i] = [x, y]

                # Evaluate if new position is better than p_global
                index = dm.coords_to_index(p_global[0], p_global[1])
                f_global = dm.get_fitness(data, index[0], index[1])
                count_evaluations += 1
                if f_new > f_global:
                    p_global = [x, y]

            # Not HC for all other particles
            else:
                # Force towards the center of the swarm. Implementation: force towards center if pos > st. deviation
                st_dev_x_position = stdev(x_positions)
                st_dev_y_position = stdev(y_positions)
                mean_x_position = mean(x_positions)
                mean_y_position = mean(y_positions)
                v_swarm_center_x = 0
                v_swarm_center_y = 0

                # x-position change
                if abs(element[0] - mean_x_position) > st_dev_x_position:
                    if element[0] > mean_x_position:
                        v_swarm_center_x = -v_swarm_center
                    else:
                        v_swarm_center_x = v_swarm_center

                # y-position change
                if abs(element[1] - mean_y_position) > st_dev_y_position:
                    if element[1] > mean_y_position:
                        v_swarm_center_y = -v_swarm_center
                    else:
                        v_swarm_center_y = v_swarm_center

                # Force towards p_global
                if element[0] > p_global[0]:
                    v_p_global_x = -v_best_global
                else:
                    v_p_global_x = v_best_global

                if element[1] > p_global[1]:
                    v_p_global_y = -v_best_global
                else:
                    v_p_global_y = v_best_global

                # Force towards pm_best
                if element[0] > pm_best[i][0]:
                    v_pm_best_x = -v_best_local
                else:
                    v_pm_best_x = v_best_local
                if element[1] > pm_best[i][1]:
                    v_pm_best_y = -v_best_local
                else:
                    v_pm_best_y = v_best_local

                # Add together x and y velocities
                v_x = v_inertia[0] + v_swarm_center_x + v_p_global_x + v_pm_best_x
                v_y = v_inertia[1] + v_swarm_center_y + v_p_global_y + v_pm_best_y
                vm[i] = [v_x, v_y]

                # Define new position of current element (i)
                positions[i] = [positions[i][0] + vm[i][0], positions[i][1] + vm[i][1]]

                # Evaluate previous best fitness of current particle
                index = dm.coords_to_index(pm_best[i][0], pm_best[i][1])
                fitness_old = dm.get_fitness(data, index[0], index[1])
                count_evaluations += 1

                # Evaluate fitness at new position of current particle
                index = dm.coords_to_index(positions[i][0], positions[i][1])
                fitness_new = dm.get_fitness(data, index[0], index[1])
                count_evaluations += 1

                # If new fitness is better than before, update pm_best (best location of current particle)
                if fitness_new > fitness_old:
                    pm_best[i] = [positions[i][0], positions[i][1]]

            # Update counter
            i += 1

        # Update fitness list for next time step
        for element in pm_best:
            index = dm.coords_to_index(element[0], element[1])
            fitness_list.append(dm.get_fitness(data, index[0], index[1]))
            count_evaluations += 1

        # Update best fitness values for next step (for HC modification)
        best_fitness_values = dm.best_m_values_in_list(fitness_list, number_of_hc_elements)

        # Update best global position
        index = dm.coords_to_index(p_global[0], p_global[1])
        count_evaluations += 1
        if max(fitness_list) > dm.get_fitness(data, index[0], index[1]):
            best_fitness_index = fitness_list.index(max(fitness_list))
            p_global = pm_best[best_fitness_index]

        # Plot all particle positions (swarm) if enabled
        if plot_enable:
            print(dm.get_fitness(data, index[0], index[1]))
            plot_swarm(positions)
            time.sleep(0.2)

    # Evaluate fitness of p_global at the end of the whole PSO process and return it
    index = dm.coords_to_index(p_global[0], p_global[1])
    count_evaluations += 1
    return [dm.get_fitness(data, index[0], index[1]), count_evaluations]
