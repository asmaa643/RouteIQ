import csv
import sys
import time

from planning_problem import max_level, PlanningProblem
import preprocess_search
from preprocess_planning import create_domain_problem_files
from search import *
from heuristics import null_heuristic, maxPointAirDistHeuristic, \
    sumAirDistHeuristic, mstAirDistHeuristic
from search import a_star_search_planning

"""
This script compares the performance of different search algorithms and heuristics 
in solving a delivery problem with multiple orders. It utilizes A* search and planning 
algorithms to find optimal delivery paths, based on various heuristics such as air distances 
and minimum spanning tree calculations.
"""



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
    routes = preprocess_search.add_air_distances(map_routes, points, matrix)

    problems = []
    for i in range(len(orders)):
        start_state = (
        '#', [False for _ in orders[:i + 1]], [False for _ in orders[:i + 1]])

        problems.append(DeliveryProblem(start_state, orders[:i + 1], routes))
    return problems, routes


def create_planning_problem(commands):
    """
        Prepares planning problems for comparison.
    """
    map_file = open(commands[1], "r")
    data = list(map_file)
    orders_file = open(commands[3], "r")
    orders = list(orders_file)
    problems = []
    for i in range(len(orders)):
        create_domain_problem_files(sys.argv[1], data, orders[:i + 1])
        domain = "domain" + commands[1]
        problem = "problem" + commands[1]
        problems.append(PlanningProblem(domain, problem))
    map_file.close()
    orders_file.close()

    return problems


def compare(problems, probs):
    """
        Compares the performance of A* search and planning.
    """
    searcher = AStarSearch()
    import time

    a_star_times = []
    a_star_costs = []

    for i, problem in enumerate(problems):
        if (i == 8): break
        print("orders list:")
        print([(order.source, order.destination) for order in problem.orders])
        # Null heuristic (Uniform Cost Search behavior)
        # optimal_path, total_cost = searcher.a_star(problem,
        #                                            heuristic=null_heuristic)
        # print(f"Optimal path with null heuristic:", total_cost)
        # show_path(optimal_path)

        # optimal_path = a_star_search(problem, heuristic=null_heuristic)
        # print(f"Optimal path with null heuristic:")
        # show_path(optimal_path)
        # optimal_path = uniform_cost_search(problem)
        # print(f"Path with uniform:")
        # show_path(optimal_path)
        ######################

        start_time = time.time()

        optimal_path, total_cost = searcher.a_star(problem,
                                                   heuristic=maxPointAirDistHeuristic)
        end_time = time.time()
        # print(f"Optimal path with maxPointAirDistHeuristic:", total_cost)
        # show_path(optimal_path)

        # Calculate elapsed time in seconds and append to the list
        elapsed_time = (end_time - start_time)
        a_star_times.append(elapsed_time)
        a_star_costs.append(total_cost)

        # optimal_path = a_star_search(problem,
        #                              heuristic=maxPointAirDistHeuristic)
        # print(f"Optimal path with maxPointAirDistHeuristic:")
        # show_path(optimal_path)

        # optimal_path = depth_first_search(problem)
        # print(f"Path with dfs: {optimal_path}")

        # optimal_path, total_cost = searcher.a_star(problem,
        #                                            heuristic=sumAirDistHeuristic)
        # print(f"Optimal path with sumAirDistHeuristic:", total_cost)
        # show_path(optimal_path)
        #
        # optimal_path, total_cost = searcher.a_star(problem,
        #                                            heuristic=mstAirDistHeuristic)
        # print(f"Optimal path with mstAirDistHeuristic:", total_cost)
        # show_path(optimal_path)
    import matplotlib.pyplot as plt

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
    for i, prob in enumerate(probs):
        if i == 6: break
        print([(order.source, order.destination) for order in problems[i].orders])
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

    plt.plot(range(1, 7), planning_times, linestyle='-', color='r',
             label='Planning')
    # plt.show()
    plt.legend(loc='upper center')
    plt.savefig("a_star_vs_planning_time.png", format='png', bbox_inches='tight')
    plt.show()
###########################################

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 9), a_star_costs, linestyle='-', color='b',
             label='A* Search')
    plt.xlabel('Orders number')
    plt.ylabel("Solution's cost")
    plt.title("Solutions' Costs across different orders numbers")
    plt.grid(True)
    plt.plot(range(1, 7), planning_costs, linestyle='-', color='r',
             label='Planning')
    # plt.show()
    plt.legend(loc='upper center')
    plt.savefig("a_star_vs_planning_cost.png", format='png', bbox_inches='tight')
    plt.show()

    print("Comparing A* star and planning: Done.")
##################################################33
    plt.figure(figsize=(10, 6))
    plt.xlabel('Orders number')
    plt.ylabel("Expanded nodes")
    plt.title("Expanded nodes in planning across different orders numbers")
    plt.grid(True)
    plt.plot(range(1, 7), planning_nodes, linestyle='-', color='r',
             label='expanded nodes')
    plt.savefig("planning_nodes.png", format='png', bbox_inches='tight')
    plt.show()
    print("Planning results: Done.")
    ############################ A* #################################
    mst_costs = []
    sum_costs = []
    dfs_costs = []
    for i, problem in enumerate(problems):
        if (i == 8): break
        print("orders list:")
        print([(order.source, order.destination) for order in problem.orders])
        ######################

        # optimal_path, total_cost = searcher.a_star(problem,
        #                                            heuristic=maxPointAirDistHeuristic)
        # print(f"Optimal path with maxAirDistHeuristic:", total_cost)


        optimal_path, sum_cost = searcher.a_star(problem,
                                                   heuristic=sumAirDistHeuristic)
        # print(f"Optimal path with sumAirDistHeuristic:", sum_cost)
        sum_costs.append(sum_cost)
        # show_path(optimal_path)
        #
        optimal_path, mst_cost = searcher.a_star(problem,
                                                   heuristic=mstAirDistHeuristic)
        # print(f"Optimal path with mstAirDistHeuristic:", mst_cost)
        mst_costs.append(mst_cost)
        # show_path(optimal_path)
        #
        # path, dfs = depth_first_search(problem)
        # print(f"Path with dfs: {dfs}")
        # dfs_costs.append(dfs)

    plt.figure(figsize=(10, 6))

    plt.xlabel('Orders number')
    plt.ylabel("Heuristic costs")
    plt.title("A* Search heuristics costs")
    plt.grid(True)
    plt.plot(range(1, 9), mst_costs, linestyle='-', color='g',
             label='mst')
    plt.plot(range(1, 9), sum_costs, linestyle='-', color='y',
             label='sum')
    plt.plot(range(1, 9), a_star_costs, linestyle='--', color='b',
             label='max')
    plt.legend(loc='upper center')
    plt.savefig("a_star_vs.png", format='png',
                bbox_inches='tight')
    plt.show()




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
    if plan is not None:
        plan_ = "#"
        total = 0
        for act in plan:
            if "Move" in act.get_name():
                w = act.get_name().split("_")
                p1, p2 = w[1], w[3]
                total += routes.get_distance(p1, p2)
                plan_ += " -> " + p2
        print("Planning found a plan with %d actions and %.2f cost in %.2f seconds" % (
            len(plan), total, elapsed_time ))
        print("By following this plan:")
        print(plan_)
        if total == total_cost:
            print("\nFound the same PATH/ COST")
    else:
        print("Could not find a plan in %.2f seconds" % elapsed_time)



if __name__ == '__main__':
    """
    Run this script with appropriate command-line arguments to specify the input files and desired operations.
    """
    ############################## Commands format #######################
    # 1: map, 2: air distances on map, 3: orders list
    # 4: (ordersNum=*) / (compare) / ()
    #           |            |
    #    from 1 to *     Show overall results

    ############################### A* Search ############################

    problems, routes = create_A_search_problems(sys.argv)
    probs = create_planning_problem(sys.argv)
    if sys.argv[4] == "compare":
        compare(problems, probs)

    if sys.argv[4].split("=")[0] == "ordersNum":
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg

        # Load an image from a file
        img = mpimg.imread(
            'map_f.jpg')  # Replace with your image file path

        # Display the image
        plt.imshow(img)
        plt.axis('off')  # Hide the axes
        plt.show(
            block=True)  # Ensures the window remains open until manually closed

        # Prompt the user for input after the image is closed
        user_input = input("Please enter your input: ")

        # Print or use the user input
        print(f'You entered: {user_input}')

        run_num_orders(problems, probs, int(sys.argv[4].split("=")[1]))
