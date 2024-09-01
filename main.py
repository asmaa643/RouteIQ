import csv
import sys
import time

from matplotlib import pyplot as plt
import matplotlib.image as mpimg

from planning_problem import max_level, PlanningProblem
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
        create_domain_problem_files(sys.argv[1], data, orders[:i + 1])
        domain = "domain" + commands[1]
        problem = "problem" + commands[1]
        problems_.append(PlanningProblem(domain, problem))
    map_file.close()
    orders_file.close()

    return problems_


def compare(problems_, probs_):
    """
        Compares the performance of A* search and planning.
    """
    ############################### A* search ############################
    searcher = AStarSearch()
    a_star_times = []
    a_star_costs = []
    a_star_results(a_star_costs, a_star_times, problems_, searcher)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 9), a_star_times, linestyle='-', color='b',
             label='A* Search')
    plt.xlabel('Orders number')
    plt.ylabel('Time (seconds) taken to find a solution')
    plt.title('Time taken for code execution across different orders numbers')
    plt.grid(True)

    ############################### Planning ############################
    planning_times = []
    planning_costs = []
    planning_nodes = []
    planning_results(planning_costs, planning_nodes, planning_times, problems_,
                     probs_)
    ############################### First plot ############################

    plt.plot(range(1, 8), planning_times, linestyle='-', color='r',
             label='Planning')
    # plt.show()
    plt.legend(loc='upper center')
    plt.savefig("a_star_vs_planning_time.png", format='png', bbox_inches='tight')
    plt.show()
    ############################### Second plot ############################

    a_star_planning_costs(a_star_costs, planning_costs)

    print("Comparing A* star and planning: Done.")
    ############################### Third plot ############################
    planning_plot(planning_nodes)
    print("Planning results: Done.")
    ############################ Comparing A* ###############################
    a_star_compare_results(a_star_costs, problems_, searcher)


def planning_plot(planning_nodes):
    plt.figure(figsize=(10, 6))
    plt.xlabel('Orders number')
    plt.ylabel("Expanded nodes")
    plt.title("Expanded nodes in planning across different orders numbers")
    plt.grid(True)
    plt.plot(range(1, 8), planning_nodes, linestyle='-', color='r',
             label='expanded nodes')
    plt.savefig("planning_nodes.png", format='png', bbox_inches='tight')
    plt.show()


def a_star_planning_costs(a_star_costs, planning_costs):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 9), a_star_costs, linestyle='-', color='b',
             label='A* Search')
    plt.xlabel('Orders number')
    plt.ylabel("Solution's cost")
    plt.title("Solutions' Costs across different orders numbers")
    plt.grid(True)
    plt.plot(range(1, 8), planning_costs, linestyle='-', color='r',
             label='Planning')
    # plt.show()
    plt.legend(loc='upper center')
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
    plt.grid(True)
    plt.plot(range(1, 9), mst_costs, linestyle='-', color='g',
             label='mst')
    plt.plot(range(1, 9), a_star_costs, linestyle='--', color='b',
             label='max')
    plt.legend(loc='upper center')
    plt.savefig("max_vs_mst.png", format='png',
                bbox_inches='tight')
    plt.show()


def planning_results(planning_costs, planning_nodes, planning_times, problems_,
                     probs_):
    for i, prob in enumerate(probs_):
        if i == 7: break
        print("Run planning over", i+1, "orders")

        # print([(order.source, order.destination) for order in
        #        problems_[i].orders])
        start_time = time.time()
        plan = a_star_search_planning(prob, max_level)
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


def run_num_orders(search, planning, num):
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
    check_plan(elapsed_time, plan, total_cost)


def check_plan(elapsed_time, plan, total_cost):
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


def check_argv(argv):
    if len(argv) != 5:
        print("Can't run the Code. Run it using: "
              "map.txt air_distances.csv orders.txt (ordersNum=*)/(results)/(use)")
        exit(1)
    if argv[1] != 'map.txt' or argv[2] != 'air_distances.csv' or argv[3] != 'orders.txt':
        print("Can't run the Code. Run it using: "
              "map.txt air_distances.csv orders.txt (ordersNum=*)/(results)/(use)")
        exit(1)
    if argv[4] != 'use' and argv[4] != 'results' and 'ordersNum=' not in argv[4]:
        print("Can't run the Code. Run it using: "
              "map.txt air_distances.csv orders.txt (ordersNum=*)/(results)/(use)")
        exit(1)


def user_problem():
    input("Click enter to see the MAP!'\n Close it, then write your orders! ")
    show_map()
    user_orders = open("user_orders.txt", 'w')
    # Prompt the user for input after the image is closed
    print("Write your list, one another one. When done write done!")
    get_inputs(user_orders)
    user_orders.close()
    problems_, routes_ = create_A_search_problems(
        [0, sys.argv[1], sys.argv[2], "user_orders.txt"])
    probs_ = create_planning_problem(
        [0, sys.argv[1], sys.argv[2], "user_orders.txt"])
    if len(problems_) > 0:
        run_num_orders(problems_, probs_, 0)
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


def get_inputs(user_orders):
    user_input = input(
        "Please enter your first order (letter-number), then click ENTER: ")
    while user_input != "done":
        if '-' in user_input and user_input.count('-') == 1 and user_input[
            1] == '-':
            src, dest = user_input.split('-')
            if src not in SOURCES or dest not in DESTS:
                print("Wrong format.")
                user_input = input(
                    "Please enter your order(letter-number), then click ENTER: ")
                continue
        else:
            print("Wrong format.")
            user_input = input(
                "Please enter your order(letter-number), then click ENTER: ")
            continue

        user_orders.write(user_input + '\n')
        user_input = input(
            "Please enter your order(letter-number), then click ENTER: ")


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
    check_argv(sys.argv)
    problems, routes = create_A_search_problems(sys.argv)
    probs = create_planning_problem(sys.argv)
    if sys.argv[4] == "results":
        compare(problems, probs)

    if sys.argv[4].split("=")[0] == "ordersNum":
        if int(sys.argv[4].split("=")[1]) > 10 or int(sys.argv[4].split("=")[1]) < 1:
            print("Usage: ordersNum runs with less than 11 orders.")
            exit(1)
        run_num_orders(problems, probs, int(sys.argv[4].split("=")[1]))
    if sys.argv[4] == "use":
        user_problem()

