import csv
import sys
import time

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

from planning_problem import max_level, PlanningProblem, level_sum, null_heuristic
import preprocess_search
from preprocess_planning import create_domain_problem_files
from search import *
from heuristics import maxPointAirDistHeuristic, \
    sumAirDistHeuristic, mstAirDistHeuristic
from search import a_star_search_planning

"""
This script compares the performance of different search algorithms and heuristics 
in solving a delivery problem with multiple orders. It utilizes A* search and planning 
algorithms to find optimal delivery paths, based on various heuristics such as air distances 
and minimum spanning tree calculations.
"""

SOURCES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
DESTS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
n_groups = 8
index = np.arange(n_groups)
bar_width = 0.15

def show_path(path):
    """
        Displays the path of moves taken.
    """
    to_show = "#"
    for move in path:
        to_show += " -> " + move[1]
    print(to_show)


def create_A_search_problems(commands):
    """
        Prepares the A* search problems based on input commands.
    """
    map_file = open(commands[1], "r")
    data = list(map_file)
    map_routes = preprocess_search.get_map_routes(data)
    map_file.close()
    orders_file = open(commands[3], "r")
    orders = preprocess_search.get_orders_list(orders_file)
    orders_file.close()

    file_path = commands[2]  # Update with your file path
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    points = data[0][1:]  # The header row, without the first column
    matrix = [' '.join(row[1:]) for row in data[1:]]
    routes_ = preprocess_search.add_air_distances(map_routes, points, matrix)

    problems_ = []
    for i in range(len(orders)):
        start_state = (
        '#', [False for _ in orders[:i + 1]], [False for _ in orders[:i + 1]])

        problems_.append(DeliveryProblem(start_state, orders[:i + 1], routes_))
    return problems_, routes_


def create_planning_problem(commands):
    """
        Prepares planning problems for comparison.
    """
    map_file = open(commands[1], "r")
    data = list(map_file)
    orders_file = open(commands[3], "r")
    orders = list(orders_file)
    problems_ = []
    for i in range(len(orders)):
        create_domain_problem_files(commands[1], data, orders[:i + 1])
        domain = "domain" + commands[1]
        problem = "problem" + commands[1]
        problems_.append(PlanningProblem(domain, problem))
    map_file.close()
    orders_file.close()

    return problems_


def compare(problems_, probs_, routes):
    """
        Compares the performance of A* search and planning.
    """
    ############################### A* search ############################
    searcher = AStarSearch()
    a_star_times = []
    a_star_costs = []
    a_star_results(a_star_costs, a_star_times, problems_, searcher)
    plt.figure(figsize=(10, 6))
    plt.bar(index, a_star_times, bar_width,color='b',
             label='A* Search')
    plt.xlabel('Orders number')
    plt.ylabel('Time (seconds) taken to find a solution')
    plt.title('Time taken for code execution across different orders numbers')


    ############################### Planning-max ############################
    planning_times_max = []
    planning_costs_max = []
    planning_nodes_max = []
    planning_results(planning_costs_max, planning_nodes_max, planning_times_max,
                     probs_, routes, max_level, True)
    planning_times_max = planning_times_max + [0] * (
                n_groups - len(planning_times_max))
    planning_costs_max = planning_costs_max + [0] * (
                n_groups - len(planning_costs_max))
    planning_nodes_max = planning_nodes_max + [0] * (
                n_groups - len(planning_nodes_max))

    ############################### Planning-levelSum ########################
    planning_times_level = []
    planning_costs_level = []
    planning_nodes_level = []
    planning_results(planning_costs_level, planning_nodes_level,
                     planning_times_level,
                     probs_, routes, level_sum, False)
    ############################### Planning-zero ############################
    planning_times_zero = []
    planning_costs_zero = []
    planning_nodes_zero = []
    planning_results(planning_costs_zero, planning_nodes_zero,
                     planning_times_zero,
                     probs_, routes, null_heuristic, False)
    ############################### First plot ############################

    plt.bar(index+bar_width, planning_times_max,bar_width, color='r',
             label='maxPlanning')
    plt.bar(index + bar_width*2, planning_times_level, bar_width, color='c',
            label='levelSumPlanning')
    plt.bar(index + bar_width*3, planning_times_zero, bar_width, color='m',
            label='zeroPlanning')
    # plt.show()
    plt.xticks(index + bar_width / 2, range(1, n_groups + 1))
    plt.legend()
    plt.savefig("a_star_vs_planning_time.png", format='png', bbox_inches='tight')
    plt.show()
    ############################### Second plot ############################

    a_star_planning_costs_max(a_star_costs, planning_costs_max, planning_costs_level, planning_costs_zero)

    print("Comparing A* star and planning: Done.")
    ############################### Third plot ############################
    planning_plot(planning_nodes_max, planning_nodes_level, planning_nodes_zero)
    print("Planning results: Done.")
    ############################ Comparing A* ###############################
    a_star_compare_results(a_star_costs, problems_, searcher)


def planning_plot(planning_nodes_max, planning_nodes_level, planning_nodes_zero):
    plt.figure(figsize=(10, 6))
    plt.xlabel('Orders number')
    plt.ylabel("Expanded nodes")
    plt.title("Expanded nodes in planning across different orders numbers")

    plt.bar(index, planning_nodes_max,bar_width, color='r',
             label='maxPlanning')
    plt.bar(index + bar_width, planning_nodes_level, bar_width, color='c',
            label='levelSumPlanning')
    plt.bar(index + bar_width * 2, planning_nodes_zero, bar_width, color='m',
            label='zeroPlanning')
    plt.xticks(index + bar_width / 2, range(1, n_groups + 1))
    plt.legend()
    plt.savefig("planning_nodes_max.png", format='png', bbox_inches='tight')
    plt.show()


def a_star_planning_costs_max(a_star_costs, planning_max, planning_level, planning_zero):
    plt.figure(figsize=(10, 6))
    plt.bar(index, a_star_costs,bar_width, color='b',
             label='A* Search')
    plt.xlabel('Orders number')
    plt.ylabel("Solution's cost")
    plt.title("Solutions' Costs across different orders numbers")

    plt.bar(index+bar_width, planning_max, bar_width, color='r',
            label='maxPlanning')
    plt.bar(index + bar_width*2, planning_level, bar_width, color='c',
            label='levelSumPlanning')
    plt.bar(index + bar_width * 3, planning_zero, bar_width, color='m',
            label='zeroPlanning')
    # plt.show()
    plt.xticks(index + bar_width / 2, range(1, n_groups + 1))
    plt.legend()
    plt.savefig("a_star_vs_planning_cost.png", format='png',
                bbox_inches='tight')
    plt.show()


def a_star_compare_results(a_star_costs, problems_, searcher):
    mst_costs = []
    for i, problem in enumerate(problems_):
        if i == 8: break
        print("Run mst over", i+1)
        optimal_path, mst_cost = searcher.a_star(problem,
                                                 heuristic=mstAirDistHeuristic)
        mst_costs.append(mst_cost)
    plt.figure(figsize=(10, 6))
    plt.xlabel('Orders number')
    plt.ylabel("Heuristic costs")
    plt.title("A* Search heuristics costs")

    plt.bar(index, mst_costs,bar_width, color='g',
             label='mst')
    plt.bar(index+bar_width, a_star_costs,bar_width, color='b',
             label='max')
    plt.xticks(index + bar_width / 2, range(1, n_groups + 1))
    plt.legend()
    plt.savefig("max_vs_mst.png", format='png',
                bbox_inches='tight')
    plt.show()


def planning_results(planning_costs, planning_nodes, planning_times,
                     probs_, routes, func, max_):
    for i, prob in enumerate(probs_):
        if i == 8 or (max_ and i == 6): break
        print("Run planning over", i+1, "orders")

        # print([(order.source, order.destination) for order in
        #        problems_[i].orders])
        start_time = time.time()
        plan = a_star_search_planning(prob, func)
        end_time = time.time()
        elapsed_time = (end_time - start_time)
        planning_times.append(elapsed_time)
        if plan is not None:
            total = 0
            for act in plan:
                if "Move" in act.get_name():
                    w = act.get_name().split("_")
                    p1, p2 = w[1], w[3]
                    total += routes.get_distance(p1, p2)
            planning_costs.append(total)
        planning_nodes.append(prob.expanded)


def a_star_results(a_star_costs, a_star_times, problems_, searcher):
    for i, problem in enumerate(problems_):
        if i == 8: break
        print("Run a_star over", i+1, "orders")
        # print([(order.source, order.destination) for order in problem.orders])

        start_time = time.time()

        optimal_path, total_cost = searcher.a_star(problem,
                                                   heuristic=maxPointAirDistHeuristic)
        end_time = time.time()

        # Calculate elapsed time in seconds and append to the list
        elapsed_time = (end_time - start_time)
        a_star_times.append(elapsed_time)
        a_star_costs.append(total_cost)


def run_num_orders(search, planning, num, routes):
    """
        Runs the search and planning algorithms for a specific number of orders.
    """
    searcher = AStarSearch()
    search_problem = search[num - 1]
    print("The orders list is:"),
    for order in search_problem.orders:
        print("(", order.source,",", order.destination,")")
    start_time = time.time()
    optimal_path, total_cost = searcher.a_star(search_problem,
                                               heuristic=maxPointAirDistHeuristic)
    end_time = time.time()
    elapsed_time = (end_time - start_time)
    print(f"A* found the optimal path with cost", total_cost,
          "in %.2f seconds" % elapsed_time, "\nBy taking this path:")
    show_path(optimal_path)
    print()
    planning_problem = planning[num - 1]
    start_time = time.time()
    plan = a_star_search_planning(planning_problem, max_level)
    end_time = time.time()
    elapsed_time = (end_time - start_time)
    check_plan(elapsed_time, plan, total_cost, routes)


def check_plan(elapsed_time, plan, total_cost, routes):
    if plan is not None:
        plan_ = "#"
        total = 0
        for act in plan:
            print(act.get_name())
            if "Move" in act.get_name():
                w = act.get_name().split("_")
                p1, p2 = w[1], w[3]
                total += routes.get_distance(p1, p2)
                plan_ += " -> " + p2
        print(
            "Planning found a plan with %d actions and %.2f cost in %.2f seconds" % (
                len(plan), total, elapsed_time))
        print("By following this path:")
        print(plan_)
        if total == total_cost:
            print("\nFound the same PATH/ COST")
    else:
        print("Could not find a plan in %.2f seconds" % elapsed_time)



def user_problem(commands, num=0):
    input("Click enter to see the MAP!'\n Close it, then write your orders! ")
    show_map()
    user_orders = open("user_orders.txt", 'w')
    # Prompt the user for input after the image is closed
    print("Write your list, one another one. When done write done!")
    get_inputs(user_orders, num)
    user_orders.close()
    problems_, routes_ = create_A_search_problems(
        [0, commands[1], commands[2], "user_orders.txt"])
    probs_ = create_planning_problem(
        [0, commands[1], commands[2], "user_orders.txt"])
    if len(problems_) > 0:
        run_num_orders(problems_, probs_, 0, routes_)
    else:
        print("No orders were entered.")


def show_map():
    plt.figure(figsize=(10, 6))
    # Load an image from a file
    img = mpimg.imread(
        'map_f.jpg')  # Replace with your image file path
    # Display the image
    plt.imshow(img)
    plt.axis('off')  # Hide the axes
    plt.show(
        block=True)  # Ensures the window remains open until manually closed


def get_inputs(user_orders, num):
    orders_list = []
    lst = True
    if num > 0:
        lst = False
    user_input = input(
        "Please enter your first order (letter-number), then click ENTER: ")
    while num > 0 or (lst and user_input != "done"):
        num -= 1
        if '-' in user_input and user_input.count('-') == 1 and user_input[
            1] == '-':
            src, dest = user_input.split('-')
            if src not in SOURCES or dest not in DESTS:
                print("Wrong format.")
                user_input = input(
                    "Please enter your order(letter-number), then click ENTER: ")
                num += 1
                continue
        else:
            print("Wrong format.")
            user_input = input(
                "Please enter your order(letter-number), then click ENTER: ")
            num += 1
            continue
        if user_input not in orders_list:
            user_orders.write(user_input + '\n')
            orders_list.append(user_input)
            if num > 0 or lst:
                user_input = input(
                    "Please enter your order(letter-number), then click ENTER: ")

        else:
            user_input = input(
                "You entered this order, another order then click ENTER: ")
            num += 1
            continue


def main():
    """
    Processes the command used to run the game from the command line.
    """
    from optparse import OptionParser
    usage_str = """
    USAGE:      python main.py <options>
    EXAMPLES:  
    """
    parser = OptionParser(usage_str)

    parser.add_option('-m', '--map', dest='map_file',
                      help='the map file to read from', default='map.txt')
    parser.add_option('-o', '--orders', dest='orders_file',
                      help='the orders file to read from', default='orders.txt')
    parser.add_option('-a', '--air', dest='air_distances_file',
                      help='the air distances file to read from',
                      default='air_distances.csv')

    parser.add_option('-n', '--ordersNum', dest='num',
                      type='int', nargs=1, help='the number of default orders.', default=-1)

    parser.add_option('-p', '--search-choice', dest='search_choice',
                      metavar='FUNC', help='search solution choice to use.',
                      type='choice',
                      choices=['a_star', 'planning'], default='a_star')

    parser.add_option('-u', '--user', dest='user',type='int',
                      help='run the program in user input mode', default=0)

    parser.add_option('-r', '--results', dest='results',type='int',
                      help='run the results code', default=0)


    options, _ = parser.parse_args()
    if options.num == -1 and options.user == 0 and options.results == 0:
        raise Exception("You didn't enter any choice!")
    elif (options.num > -1 or options.user == 1) and options.results == 1:
        raise Exception("Results runs alone!")
    commands = [0, options.map_file, options.air_distances_file, options.orders_file]
    problems, routes = create_A_search_problems(commands)
    probs = create_planning_problem(commands)

    if options.user == 1 and options.num == -1:
        user_problem(commands)
    elif options.user == 1 and options.num > -1:
        user_problem(commands, options.num)
    elif options.user == 0 and options.num != -1:
        if options.num > 10 or options.num < 1:
            print("Usage: ordersNum runs with less than 11 orders.")
            exit(1)
        run_num_orders(problems, probs, options.num, routes)
    elif options.results == 1:
        compare(problems, probs, routes)
    else:
        raise Exception('unrecognized options')


if __name__ == '__main__':
    """
    Run this script with appropriate command-line arguments to specify the input files and desired operations.
    """
    ############################## Commands format #######################
    # 1: map, 2: air distances on map, 3: orders list
    # 4: (ordersNum=*) / (results) /              (use)
    #           |            |                      |
    #    from 1 to *     Show overall results    use the program

    ############################### A* Search ############################
    main()

