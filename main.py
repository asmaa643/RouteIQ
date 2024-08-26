from search import AStarSearch, DeliveryProblem, a_star_search, \
    uniform_cost_search, depth_first_search
from heuristics import null_heuristic, maxPointAirDistHeuristic, \
    sumAirDistHeuristic, mstAirDistHeuristic
from map_routes import MapRoutes
from order import Order


def get_orders_list(lst):
    orders_list = []
    for line in lst:
        src, dest = line.split("-")
        orders_list.append(Order(src, dest))
    return orders_list


def get_map_routes(line):
    point, neighbors = line.split(":")
    routes = MapRoutes(None)
    for neighbor in neighbors.split("-"):
        inf = neighbor[1:-1]
        n,dist = inf.split(",")
        routes.add_route(point, n, float(dist))
    return routes

def add_air_distances(routes, points, matrix):
    for p,line in points,matrix:
        dists = line.split()
        for index, point in enumerate(points):
            routes.add_air_distance(p, point, float(dists[index]))
    return routes




if __name__ == '__main__':
    map_routes = MapRoutes(None)

    orders = [
        Order('A', '3'),
        Order('B', '4'),
        Order('C', '2'),
        Order('D', '5'),
        Order('E', '1')
    ]

    start_state = ('#',[False for o in orders], [False for o in orders])
    problem = DeliveryProblem(start_state, orders, map_routes)

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
    # print(f"Total cost with maxPointAirDistHeuristic: {total_cost}")
    # # # Standard MST
    # optimal_path, total_cost = searcher.a_star(problem, heuristic=mst_heuristic)
    # print(f"Optimal path with MST heuristic: {optimal_path}")
    # print(f"Total cost with MST heuristic: {total_cost}")
    # #
    # # MST revisiting
    # optimal_path, total_cost = searcher.a_star(problem, heuristic=mst_heuristic_with_revisiting)
    # print(f"Optimal path with MST heuristic (with revisiting): {optimal_path}")
    # print(f"Total cost with MST heuristic (with revisiting): {total_cost}")

    optimal_path = uniform_cost_search(problem)
    print(f"Path with uniform: {optimal_path}")

    # optimal_path = depth_first_search(problem)
    # print(f"Path with dfs: {optimal_path}")

    optimal_path = a_star_search(problem, heuristic=sumAirDistHeuristic)
    print(f"Optimal path with sumAirDistHeuristic: {optimal_path}")

    optimal_path = a_star_search(problem, heuristic=mstAirDistHeuristic)
    print(f"Optimal path with mstAirDistHeuristic: {optimal_path}")

