from map_routes import MapRoutes
from order import Order


def get_orders_list(lst):
    """
    Parses a list of lines to create a list of Order objects.
    """
    orders_list = []
    for line in lst.readlines():
        src, dest = line.rstrip('\n').split("-")
        orders_list.append(Order(src, dest))
    return orders_list


def get_map_routes(lines):
    """
    Parses a list of lines to create a MapRoutes object with route information.
    """
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
    """
    Adds air distance data to the air_routes object based on provided distance matrix.
    """
    for p, line in zip(map_points, air_distances_matrix):
        dists = line.split()
        for index, point in enumerate(map_points):
            air_routes.add_air_distance(p, point, float(dists[index]))
    return air_routes
