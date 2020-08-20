"""
    This module provides evaluation functions for each implemented optimizer.
    Returns average time and average success rate for a given number of repetitions
    Logs the mentioned value in the folder logfiles_evaluation
"""

import time
import datetime
import optimizers as opt
from statistics import mean
from pathlib import Path


def bf_evaluation(data, number_of_tests):
    time_list = []
    success_list = []
    print("BRUTE FORCE EVALUATION STARTED")
    for i in range(number_of_tests):
        start = time.time()
        best = opt.brute_force(data)
        end = time.time()
        time_list.append((end-start)*1000)
        if best == 4556.63:
            success_list.append(1)
        else:
            success_list.append(0)
        print("Best in test ", i, ": ", best)

    print("BF EVALUATION FINISHED")
    print("Time list:", time_list)
    print("Success list:", success_list)
    print("Average time: ", mean(time_list))
    print("Success rate in percent:", mean(success_list)*100)

    # Create log file
    filename = "bf_tests_" + str(number_of_tests) + "_num_0.txt"
    path = Path(str("./logfiles_evaluation/" + filename))
    number = 1
    while path.is_file():
        filename = "bf_tests_" + str(number_of_tests) + "_num_" + str(number) +".txt"
        path = Path(str("./logfiles_evaluation/" + filename))
        number += 1

    # Log evaluated data
    with open(str("./logfiles_evaluation/" + filename), "w") as file:
        file.write("BF Evaluation \n \n")
        file.write(str("Date and Time: " + str(datetime.datetime.now()) + "\n \n"))
        file.write(str("Number of tests: " + str(number_of_tests) + "\n"))
        file.write(str("Average time in ms: " + str(mean(time_list)) + "\n"))
        file.write(str("Success rate in percent: " + str(mean(success_list)*100)))


def prs_evaluation(data, number_of_tests, number_of_evaluations):
    time_list = []
    success_list = []
    print("PURE RANDOM SEARCH EVALUATION STARTED")
    for i in range(number_of_tests):
        start = time.time()
        best = opt.pure_random_search(data, number_of_evaluations)
        end = time.time()
        time_list.append((end-start)*1000)
        if best == 4556.63:
            success_list.append(1)
        else:
            success_list.append(0)
        print("Best in test ", i, ": ", best)

    print("PRS EVALUATION FINISHED")
    print("Time list:", time_list)
    print("Success list:", success_list)
    print("Average time: ", mean(time_list))
    print("Success rate in percent:", mean(success_list)*100)

    # Create log file
    filename = "prs_tests_" + str(number_of_tests) + "_evaluations_" + str(number_of_evaluations) + "_num_0.txt"
    path = Path(str("./logfiles_evaluation/" + filename))
    number = 1
    while path.is_file():
        filename = "prs_tests_" + str(number_of_tests) + "_evaluations_" + str(number_of_evaluations) + "_num_" + str(number) +".txt"
        path = Path(str("./logfiles_evaluation/" + filename))
        number += 1

    # Log evaluated data
    with open(str("./logfiles_evaluation/" + filename), "w") as file:
        file.write("PRS Evaluation \n \n")
        file.write(str("Date and Time: " + str(datetime.datetime.now()) + "\n \n"))
        file.write(str("Number of tests: " + str(number_of_tests) + "\n"))
        file.write(str("Number of fitness evaluations: " + str(number_of_evaluations) + "\n \n"))
        file.write(str("Average time in ms: " + str(mean(time_list)) + "\n"))
        file.write(str("Success rate in percent: " + str(mean(success_list)*100)))


def hc_evaluation(data, number_of_tests, number_of_restarts):
    time_list = []
    success_list = []
    count_evaluations_list = []
    print("HILL CLIMBING EVALUATION STARTED")
    for i in range(number_of_tests):
        start = time.time()
        [best, count] = opt.hill_climbing(data, number_of_restarts)
        end = time.time()
        time_list.append((end-start)*1000)
        count_evaluations_list.append(count)
        if best == 4556.63:
            success_list.append(1)
        else:
            success_list.append(0)
        print("Best in test ", i, ": ", best)

    print("HC EVALUATION FINISHED")
    print("Time list:", time_list)
    print("Success list:", success_list)
    print("Average time: ", mean(time_list))
    print("Success rate in percent:", mean(success_list)*100)
    print("Count evaluation list: ", count_evaluations_list)
    print("Average number of fitness evaluations: ", mean(count_evaluations_list))

    # Create log file
    filename = "hc_tests_" + str(number_of_tests) + "_restarts_" + str(number_of_restarts) + "_num_0.txt"
    path = Path(str("./logfiles_evaluation/" + filename))
    number = 1
    while path.is_file():
        filename = "hc_tests_" + str(number_of_tests) + "_restarts_" + str(number_of_restarts) + "_num_" + str(number) +".txt"
        path = Path(str("./logfiles_evaluation/" + filename))
        number += 1

    # Log evaluated data
    with open(str("./logfiles_evaluation/" + filename), "w") as file:
        file.write("HC Evaluation \n \n")
        file.write(str("Date and Time: " + str(datetime.datetime.now()) + "\n \n"))
        file.write(str("Number of tests: " + str(number_of_tests) + "\n"))
        file.write(str("Number of random restarts: " + str(number_of_restarts) + "\n \n"))
        file.write(str("Average time in ms: " + str(mean(time_list)) + "\n"))
        file.write(str("Success rate in percent: " + str(mean(success_list)*100) + "\n"))
        file.write(str("Number of fitness evaluations in total: " + str(mean(count_evaluations_list))))


def pso_evaluation(data, number_of_tests, number_of_particles, time_steps, v_inertia, v_best_global, v_best_local, v_swarm_center, enable_hc, number_of_hc_elements, plot_enable):
    time_list = []
    success_list = []
    count_evaluations_list = []
    print("PARTICLE SWARM OPTIMIZATION STARTED")
    for i in range(number_of_tests):
        start = time.time()
        result = opt.particle_swarm_optimization(data, number_of_particles, time_steps, v_inertia, v_best_global, v_best_local, v_swarm_center, enable_hc, number_of_hc_elements, plot_enable)
        end = time.time()
        time_list.append((end-start)*1000)
        count_evaluations_list.append(result[1])
        if result[0] == 4556.63:
            success_list.append(1)
        else:
            success_list.append(0)
        print("Best in test ", i, ": ", result[0])

    print("PSO EVALUATION FINISHED")
    print("Time list:", time_list)
    print("Success list:", success_list)
    print("Average time: ", mean(time_list))
    print("Success rate in percent:", mean(success_list)*100)
    print("Count evaluation list: ", count_evaluations_list)
    print("Average number of fitness evaluations: ", mean(count_evaluations_list))

    # Create log file
    filename = "pso_tests_" + str(number_of_tests) + "_particles_" + str(number_of_particles) + "_num_0.txt"
    path = Path(str("./logfiles_evaluation/" + filename))
    number = 1
    while path.is_file():
        filename = "pso_tests_" + str(number_of_tests) + "particles" + str(number_of_particles) + "_num_" + str(number) +".txt"
        path = Path(str("./logfiles_evaluation/" + filename))
        number += 1

    # Log evaluated data
    with open(str("./logfiles_evaluation/" + filename), "w") as file:
        file.write("PSO Evaluation \n \n")
        file.write(str("Date and Time: " + str(datetime.datetime.now()) + "\n \n"))
        file.write(str("Number of tests: " + str(number_of_tests) + "\n"))
        file.write(str("Number of particles: " + str(number_of_particles) + "\n \n"))
        file.write(str("Number of time steps: " + str(time_steps) + "\n"))
        file.write(str("v_inertia: " + str(v_inertia) + "\n"))
        file.write(str("v_best_global: " + str(v_best_global) + "\n"))
        file.write(str("v_best_local: " + str(v_best_local) + "\n"))
        file.write(str("v_swarm_center: " + str(v_swarm_center) + "\n"))
        file.write(str("hc_enable: " + str(enable_hc) + "\n"))
        file.write(str("hc_number_of_elements: " + str(number_of_hc_elements) + "\n"))
        file.write(str("Average time in ms: " + str(mean(time_list)) + "\n"))
        file.write(str("Success rate in percent: " + str(mean(success_list)*100) + "\n"))
        file.write(str("Number of fitness evaluations in total: " + str(mean(count_evaluations_list))))


