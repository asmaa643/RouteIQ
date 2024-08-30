import csv
import sys
import time

from planning_problem import max_level, PlanningProblem
import preprocess_search
from preprocess_planning import create_domain_problem_files
from search import*
from heuristics import null_heuristic, maxPointAirDistHeuristic, \
    sumAirDistHeuristic, mstAirDistHeuristic
from search import a_star_search_planning


def show_path(path):
    to_show = "#"
    for move in path:
        to_show += " -> " + move[1]
    print(to_show)


def create_A_search_problems(commands):
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
        start_state = ('#', [False for _ in orders[:i+1]], [False for _ in orders[:i+1]])

        problems.append(DeliveryProblem(start_state, orders[:i+1], routes))
    return problems,routes

def create_planning_problem(commands):
    map_file = open(commands[1], "r")
    data = list(map_file)
    orders_file = open(commands[3], "r")
    orders = list(orders_file)
    problems = []
    for i in range(len(orders)):
        create_domain_problem_files(sys.argv[1], data, orders[:i+1])
        domain = "domain" + commands[1]
        problem = "problem" + commands[1]
        problems.append(PlanningProblem(domain, problem))
    map_file.close()
    orders_file.close()



    return problems

if __name__ == '__main__':

    ############################### A* Search ############################

    problems, routes = create_A_search_problems(sys.argv)

    searcher = AStarSearch()
    import time

    a_star_times = []

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
        print(f"Optimal path with maxPointAirDistHeuristic:", total_cost)
        show_path(optimal_path)


        # Calculate elapsed time in seconds and append to the list
        elapsed_time = (end_time - start_time)
        a_star_times.append(elapsed_time)

        # optimal_path = a_star_search(problem,
        #                              heuristic=maxPointAirDistHeuristic)
        # print(f"Optimal path with maxPointAirDistHeuristic:")
        # show_path(optimal_path)

        # optimal_path = depth_first_search(problem)
        # print(f"Path with dfs: {optimal_path}")

        optimal_path, total_cost = searcher.a_star(problem,
                                                   heuristic=sumAirDistHeuristic)
        print(f"Optimal path with sumAirDistHeuristic:", total_cost)
        show_path(optimal_path)

        optimal_path, total_cost = searcher.a_star(problem,
                                                   heuristic=mstAirDistHeuristic)
        print(f"Optimal path with mstAirDistHeuristic:", total_cost)
        show_path(optimal_path)
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 9), a_star_times, marker='o', linestyle='-', color='b')
    plt.xlabel('Range (1-9)')
    plt.ylabel('Time (seconds)')
    plt.title('Time taken for code execution across different ranges')
    plt.grid(True)
    # plt.show()
    plt.savefig("a_star.png", format='png', bbox_inches='tight')

    ############################### Planning ############################
    planning_times = []

    probs = create_planning_problem(sys.argv)
    for i,prob in enumerate(probs):
        if i == 7: break
        # start = time.perf_counter()
        start_time = time.time()
        plan = a_star_search_planning(prob, max_level)
        end_time = time.time()

        # Calculate elapsed time in seconds and append to the list
        elapsed_time = (end_time - start_time)
        planning_times.append(elapsed_time)

        # elapsed = time.perf_counter() - start
        if plan is not None:
            print("Plan found with %d actions in %.2f seconds" % (
                len(plan), elapsed_time))
            for act in plan:
                print(act.get_name())
        else:
            print("Could not find a plan in %.2f seconds" % elapsed_time)
        print("Search nodes expanded: %d" % prob.expanded)
        total = 0
        for act in plan:
            if "Move" in act.get_name():
                w = act.get_name().split("_")
                p1, p2 = w[1], w[3]
                total += routes.get_distance(p1, p2)
        print(f"Total cost planning: {total}")
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 8), planning_times, marker='o', linestyle='-', color='b')
    plt.xlabel('Range (1-9)')
    plt.ylabel('Time (seconds)')
    plt.title('Time taken for code execution across different ranges')
    plt.grid(True)
    # plt.show()
    plt.savefig("planning.png", format='png', bbox_inches='tight')