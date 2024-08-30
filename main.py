import csv
import sys

from planning_problem import max_level, PlanningProblem
from search import AStarSearch, DeliveryProblem, a_star_search, \
    uniform_cost_search, depth_first_search
from heuristics import null_heuristic, maxPointAirDistHeuristic, \
    sumAirDistHeuristic, mstAirDistHeuristic
from map_routes import MapRoutes
from order import Order
from search import a_star_search_planning



def get_orders_list(lst):
    orders_list = []
    for line in lst.readlines():
        src, dest = line.rstrip('\n').split("-")
        orders_list.append(Order(src, dest))
    return orders_list


def get_map_routes(lines):
    c_map_routes = MapRoutes(None)
    for line in lines:
        point, neighbors = line.rstrip('\n').split(":")
        if neighbors:
            for neighbor in neighbors.split("-"):
                inf = neighbor[1:-1]
                n, dist = inf.split(",")
                c_map_routes.add_route(point, n, float(dist))
    return c_map_routes

def add_air_distances(air_routes, map_points, air_distances_matrix):
    for p,line in zip(map_points, air_distances_matrix):
        dists = line.split()
        for index, point in enumerate(map_points):
            air_routes.add_air_distance(p, point, float(dists[index]))
    return air_routes

def create_domain_problem_files(name, lines, problem_orders):
    domain_file = open("domain"+name, 'w')
    problem_file = open("problem"+name, 'w')
    map_points = set()
    actions = list()
    pre = list()
    for line in lines:
        point, neighbors = line.rstrip('\n').split(":")
        map_points.add(point)
        if neighbors:
            for neighbor in neighbors.split("-"):
                inf = neighbor[1:-1]
                n, dist = inf.split(",")
                actions.append(
                    "\nName: Move_" + point + "_to_" + n + "\npre: @"
                    + point + "\nadd: @" + n + "\ndelete: @" + point)
                actions.append(
                    "\nName: Move_" + n + "_to_" + point + "\npre: @"
                    + n + "\nadd: @" + point + "\ndelete: @" + n)
    dests = []
    problem_file.write("Initial state: @#")
    for line in problem_orders.readlines():
        src, dest = line.rstrip('\n').split("-")
        problem_file.write(" order@" + src)
        actions.append(
            "\nName: Pickup_Order_" + dest + "\npre: @" + src + " order@"
            + src + "\nadd: has_Order_" + dest + "\ndelete: order@" + src)
        dests.append(" deliver_order_" + dest)
        actions.append(
            "\nName: Deliver_Order_" + dest + "\npre: @" + dest + " has_Order_"
            + dest + "\nadd: deliver_order_" + dest + "\ndelete: has_Order_" + dest)
        pre.append(
            "order@" + src + " has_Order_" + dest + " deliver_order_" + dest + " ")
    problem_file.write("\nGoal state:")
    for d in dests:
        problem_file.write(d)
    domain_file.write("Propositions:\n")
    for point in map_points:
        domain_file.write("@" + point + " ")
    for p in pre:
        domain_file.write(p)
    domain_file.write("\nActions:")
    for action in actions:
        domain_file.write(action)

def show_path(path):
    to_show = "#"
    for move in path:
        to_show += " -> " + move[1]
    print(to_show)


if __name__ == '__main__':
    map_file = open(sys.argv[1], "r")
    data = list(map_file)
    map_routes = get_map_routes(data)
    map_file.close()
    orders_file = open(sys.argv[3], "r")
    orders = get_orders_list(orders_file)
    orders_file.close()

    file_path = sys.argv[2]  # Update with your file path
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    points = data[0][1:]  # The header row, without the first column
    matrix = [' '.join(row[1:]) for row in data[1:]]
    routes = add_air_distances(map_routes, points, matrix)

    start_state = ('#',[False for o in orders], [False for o in orders])
    problem = DeliveryProblem(start_state, orders, routes)

    searcher = AStarSearch()

    # Null heuristic (Uniform Cost Search behavior)
    optimal_path, total_cost = searcher.a_star(problem, heuristic=null_heuristic)
    print(f"Optimal path with null heuristic:")
    show_path(optimal_path)

    optimal_path = a_star_search(problem, heuristic=null_heuristic)
    print(f"Optimal path with null heuristic:")
    show_path(optimal_path)
    print(f"Total cost with null heuristic: {total_cost}")

    optimal_path, total_cost = searcher.a_star(problem, heuristic=maxPointAirDistHeuristic)
    print(f"Optimal path with maxPointAirDistHeuristic:")
    show_path(optimal_path)
    print(f"Total cost with maxPointAirDistHeuristic: {total_cost}")

    optimal_path = a_star_search(problem, heuristic=maxPointAirDistHeuristic)
    print(f"Optimal path with maxPointAirDistHeuristic:")
    show_path(optimal_path)

    optimal_path = uniform_cost_search(problem)
    print(f"Path with uniform:")
    show_path(optimal_path)

    # optimal_path = depth_first_search(problem)
    # print(f"Path with dfs: {optimal_path}")

    optimal_path, total_cost = searcher.a_star(problem, heuristic=sumAirDistHeuristic)
    print(f"Optimal path with sumAirDistHeuristic:")
    show_path(optimal_path)
    print(total_cost)

    optimal_path, total_cost = searcher.a_star(problem, heuristic=mstAirDistHeuristic)
    print(f"Optimal path with mstAirDistHeuristic:")
    show_path(optimal_path)
    print(total_cost)

    import sys
    import time

    ############################### Planning ############################
    map_file = open(sys.argv[1], "r")
    data = list(map_file)
    orders_file = open(sys.argv[3], "r")
    create_domain_problem_files(sys.argv[1], data, orders_file)
    map_file.close()
    orders_file.close()

    domain = "domain"+sys.argv[1]
    problem = "problem"+sys.argv[1]

    prob = PlanningProblem(domain, problem)
    start = time.perf_counter()
    plan = a_star_search_planning(prob, max_level)
    elapsed = time.perf_counter() - start
    if plan is not None:
        print("Plan found with %d actions in %.2f seconds" % (
        len(plan), elapsed))
        for act in plan:
            print(act.get_name())
    else:
        print("Could not find a plan in %.2f seconds" % elapsed)
    print("Search nodes expanded: %d" % prob.expanded)