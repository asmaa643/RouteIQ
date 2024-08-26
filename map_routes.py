class MapRoutes:
    def __init__(self, routes): #TODO: To add another matrix
        self.routes = dict()
        self.air_distances = dict()


    def add_route(self, p1, p2, dist):
        self.routes[(min(p1, p2), max(p1, p2))] = dist

    def add_air_distance(self, p1, p2, dist):
        self.air_distances[(p1, p2)] = dist

    def air_distance(self, p1, p2):
        return self.air_distances[(p1, p2)]

    def get_distance(self, p1, p2):
        return self.routes[(min(p1, p2), max(p1, p2))]


    def get_legal_moves(self, p):
        legal_moves = []
        for p1, p2 in self.routes:
            if p == p1:
                legal_moves.append(p2)
            elif p == p2:
                legal_moves.append(p1)
        return legal_moves


