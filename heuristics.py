import networkx as nx


def null_heuristic(state, problem):
    """
    A heuristic function that always returns 0. This is typically used as a baseline heuristic
    in search algorithms such as A*.
    """
    return 0



def maxPointAirDistHeuristic(state, problem):
    """
    Heuristic function that computes the maximum straight-line (air) distance from the current location
    to any unvisited source or destination.
    """
    current_location = state[0]
    remaining_sources, remaining_destinations = state[1], state[2]
    max_distance = 0
    for index, order in enumerate(problem.orders):
        # Check if the source has not been visited
        if not remaining_sources[index]:
            source_dist = problem.map_routes.air_distance(order.source, current_location)
            max_distance = max(max_distance, source_dist)
        # Check if the destination has not been visited
        if not remaining_destinations[index]:
            destination_dist = problem.map_routes.air_distance(
                order.destination, current_location)
            max_distance = max(max_distance, destination_dist)
    return max_distance



def sumAirDistHeuristic(state, problem):
    """
    Heuristic function that computes the sum of the minimum distances required to visit all unvisited
    sources and destinations starting from the current location.
    """
    places = (state[1], state[2])
    orders = problem.orders
    remaining_places = []
    for index, order in enumerate(orders):
        if not places[0][index] and order.source != state[0]:
            remaining_places.append(order.source)
        if not places[1][index] and order.destination != state[0]:
            remaining_places.append(order.destination)

    cur_location = state[0]
    cur_min = cur_location
    path_length = 0
    while len(remaining_places) != 0:
        cur_min_dist = float('inf')
        for place in remaining_places:
            distance = problem.map_routes.air_distance(cur_location, place)
            if cur_min_dist > distance:
                cur_min_dist = distance
                cur_min = place
        remaining_places.remove(cur_min)
        path_length += cur_min_dist
        cur_location = cur_min
    return path_length




def mstAirDistHeuristic(state, problem):
    """
    Heuristic function that computes the weight of the Minimum Spanning Tree (MST) for the remaining
    unvisited sources and destinations using air distances.
     """
    places = (state[1], state[2])
    orders = problem.orders
    remaining_places = []
    for index, order in enumerate(orders):
        if not places[0][index]:
            remaining_places.append(order.source)
        if not places[1][index]:
            remaining_places.append(order.destination)
    graph = nx.Graph()
    edges_weighted = {(p1, p2,
                       problem.map_routes.air_distance(p1, p2))
                      for p1 in remaining_places
                      for p2 in remaining_places
                      if p1 != p2}

    for edge in edges_weighted:
        graph.add_edge(edge[0], edge[1], weight=edge[2])

    mst = nx.tree.minimum_spanning_tree(graph)
    return mst.size(weight='weight')