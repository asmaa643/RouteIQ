class MapRoutes:
    """
      A class to represent a map with routes and air distances between points.
      """

    def __init__(self, routes):  # TODO: To add another matrix
        """
        Initializes the MapRoutes with empty dictionaries for routes and air distances.
        """
        self.routes = dict()
        self.air_distances = dict()

    def add_route(self, p1, p2, dist):
        """
        Adds a route between two points with a specified distance.
        """
        self.routes[(min(p1, p2), max(p1, p2))] = dist

    def add_air_distance(self, p1, p2, dist):
        """
        Adds a straight-line (air) distance between two points.
        """
        self.air_distances[(p1, p2)] = dist

    def air_distance(self, p1, p2):
        """
        Returns the straight-line (air) distance between two points.
        """
        return self.air_distances[(p1, p2)]

    def get_distance(self, p1, p2):
        """
        Returns the distance between two points on the map, considering it as an undirected graph.
        """
        return self.routes[(min(p1, p2), max(p1, p2))]

    def get_legal_moves(self, p):
        """
        Returns a list of all legal moves (adjacent points) from a given point.
        """
        legal_moves = []
        for p1, p2 in self.routes:
            if p == p1:
                legal_moves.append(p2)
            elif p == p2:
                legal_moves.append(p1)
        return legal_moves
