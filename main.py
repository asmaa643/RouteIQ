import csv
import sys

from search import AStarSearch, DeliveryProblem, a_star_search, \
    uniform_cost_search, depth_first_search
from heuristics import null_heuristic, maxPointAirDistHeuristic, \
    sumAirDistHeuristic, mstAirDistHeuristic
from map_routes import MapRoutes
from order import Order


def get_orders_list(lst):
    orders_list = []
    for line in lst.readlines():
        src, dest = line.rstrip('\n').split("-")
        orders_list.append(Order(src, dest))
    return orders_list


def get_map_routes(lines):
    routes = MapRoutes(None)
    for line in lines:
        point, neighbors = line.rstrip('\n').split(":")
        if neighbors:
            for neighbor in neighbors.split("-"):
                inf = neighbor[1:-1]
                n, dist = inf.split(",")
                routes.add_route(point, n, float(dist))
    return routes

def add_air_distances(routes, points, matrix):
    for p,line in zip(points,matrix):
        dists = line.split()
        for index, point in enumerate(points):
            routes.add_air_distance(p, point, float(dists[index]))
    return routes




if __name__ == '__main__':
    map_file = open(sys.argv[1], "r")
    data = list(map_file)
    map_routes = get_map_routes(data)
    print(sys.argv)
    orders_file = open(sys.argv[3], "r")
    orders = get_orders_list(orders_file)

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
    print(f"Optimal path with null heuristic: {optimal_path}")

    optimal_path = a_star_search(problem, heuristic=null_heuristic)
    print(f"Optimal path with null heuristic: {optimal_path}")
    print(f"Total cost with null heuristic: {total_cost}")

    optimal_path, total_cost = searcher.a_star(problem, heuristic=maxPointAirDistHeuristic)
    print(f"Optimal path with maxPointAirDistHeuristic: {optimal_path}")
    print(f"Total cost with maxPointAirDistHeuristic: {total_cost}")

    optimal_path = a_star_search(problem, heuristic=maxPointAirDistHeuristic)
    print(f"Optimal path with maxPointAirDistHeuristic: {optimal_path}")

    optimal_path = uniform_cost_search(problem)
    print(f"Path with uniform: {optimal_path}")

    # optimal_path = depth_first_search(problem)
    # print(f"Path with dfs: {optimal_path}")

    optimal_path, total_cost = searcher.a_star(problem, heuristic=sumAirDistHeuristic)
    print(f"Optimal path with sumAirDistHeuristic: {optimal_path}")
    print(total_cost)

    optimal_path, total_cost = searcher.a_star(problem, heuristic=mstAirDistHeuristic)
    print(f"Optimal path with mstAirDistHeuristic: {optimal_path}")
    print(total_cost)

