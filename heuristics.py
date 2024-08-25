import networkx as nx


def null_heuristic(state, problem):
    return 0


def maxPointAirDistHeuristic(state, problem):
    remaining_places = (state[1], state[2])
    distances = []
    for index, order in enumerate(problem.orders):
        if not remaining_places[0][index] and order.source != state[0]:
            distances.append(problem.map_routes.air_distance(order.source, state[0]))
            # print('hellooooooooooooooooooo')
        if not remaining_places[1][index] and order.destination != state[0]:
            distances.append(problem.map_routes.air_distance(order.destination, state[0]))
    return max(distances) if distances else 0


def sumAirDistHeuristic(state, problem):
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