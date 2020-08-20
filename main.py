"""
    This python file is for using various optimizers implemented in optimizers.py.
    Optimizer is to be chosen by setting the respective optimizer to True/False (below).
    Evaluates needed TIME and BEST_VALUE, which is the highest altitude found.

    Evaluation mode: If set to true, respective functions of the evaluation module are called.
                     Repeats the optimizer test for a specified number and returns avg. time and avg. success rate
                     Result is logged in folder logfiles_evaluation
"""

import time
import data_methods as dm
import optimizers as opt
import evaluation as eval

# Enable/Disable optimizers for testing
BF = True  # Brute Force
PRS = False  # Pure Random Search
HC = False  # Hill Climbing
PSO = False  # Particle Swarm Optimization
TEST_COORDS = False  # Can be used for evaluation of a height given by x,y-user input

# Enable/Disable evaluation mode (description in introduction above)
EVALUATION = False
NUMBER_OF_TESTS = 5

# PRS constants
NUMBER_OF_EVALUATIONS = 100000

# HC constants
NUMBER_OF_RESTARTS = 1000

# PSO constants
NUMBER_OF_PARTICLES = 100  # How many particles are initialized
TIME_STEPS = 20  # How often new positions for all particles are evaluated
V_INERTIA = [0, 0]  # Base velocity in steps in x,y-direction
V_BEST_GLOBAL = 20  # Velocity towards position of global max. fitness in steps
V_BEST_LOCAL = 0  # Velocity towards position of local max. fitness in steps
V_SWARM_CENTER = 0   # Velocity towards swarm center in steps
ENABLE_HC = True  # If enabled, a specified amount of particles does hill climbing (HC) if among the best ones (T/F)
NUMBER_OF_HC_ELEMENTS = 30  # Number of particles doing HC (number of best ones, eg best, second-best, etc.)
PLOT = False  # If enabled, particles are plotted for each time step

# Initialize data set
print("START COLLECTING DATA")
data = dm.generate_data_structure()
print("DATA COLLECTED")

# Test Coords
if TEST_COORDS:
    print("TEST COORDS MODE")
    print("Specify x and y coordinate below")
    while True:
        x = int(input())
        y = int(input())
        index = dm.coords_to_index(x, y)
        print(dm.get_fitness(data, index[0], index[1]))

if EVALUATION:
    if BF:
        eval.bf_evaluation(data, NUMBER_OF_TESTS)
    elif PRS:
        eval.prs_evaluation(data, NUMBER_OF_TESTS, NUMBER_OF_EVALUATIONS)
    elif HC:
        eval.hc_evaluation(data, NUMBER_OF_TESTS, NUMBER_OF_RESTARTS)
    elif PSO:
        eval.pso_evaluation(data, NUMBER_OF_TESTS, NUMBER_OF_PARTICLES, TIME_STEPS, V_INERTIA, V_BEST_GLOBAL, V_BEST_LOCAL, V_SWARM_CENTER, ENABLE_HC, NUMBER_OF_HC_ELEMENTS, PLOT)
    else:
        print("ERROR: Evaluation started but no optimizer selected in main.py")

else:
    # Brute Force
    if BF:
        print("BRUTE FORCE STARTED")
        start = time.time()
        best = opt.brute_force(data)
        end = time.time()
        print("BF FINISHED")
        print("Highest Altitude: ", best)
        print("Time required in ms: ", (end - start)*1000)

    # Pure Random Search
    elif PRS:
        print("PURE RANDOM SEARCH STARTED")
        start = time.time()
        best = opt.pure_random_search(data, NUMBER_OF_EVALUATIONS)
        end = time.time()
        print("PRS FINISHED")
        print("Highest Altitude: ", best)
        print("Time required in ms: ", (end - start)*1000)

    # Hill Climbing
    elif HC:
        print("HILL CLIMBING STARTED")
        start = time.time()
        result = opt.hill_climbing(data, NUMBER_OF_RESTARTS)
        end = time.time()
        print("HC FINISHED")
        print("Highest Altitude: ", result[0])
        print("Number of fitness evaluations: ", result[1])
        print("Time required in ms: ", (end - start)*1000)

    # Particle Swarm Optimization
    elif PSO:
        print("PARTICLE SWARM OPTIMIZATION STARTED")
        start = time.time()
        result = opt.particle_swarm_optimization(data, NUMBER_OF_PARTICLES, TIME_STEPS, V_INERTIA, V_BEST_GLOBAL, V_BEST_LOCAL, V_SWARM_CENTER, ENABLE_HC, NUMBER_OF_HC_ELEMENTS, PLOT)
        end = time.time()
        print("PSO FINISHED")
        print("Highest Altitude: ", result[0])
        print("Number of fitness evaluations: ", result[1])
        print("Time required in ms: ", (end - start)*1000)

    else:
        print("ERROR: No optimizer selected in main.py")
