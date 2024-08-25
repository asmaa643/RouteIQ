from collections import defaultdict

class MapRoutes:
    def __init__(self, routes): #TODO: To add another matrix
        self.routes = dict()
        self.air_distances = dict()
        if routes is None:  # default
            # TODO: To fill distances
            self.routes[('#', 'A')] = 4.7
            self.routes[('#', '1')] = 0.8
            self.routes[('#', '2')] = 2.7
            self.routes[('A', 'B')] = 3.5
            self.routes[('5', 'B')] = 2.4
            self.routes[('B', 'C')] = 1
            self.routes[('C', 'D')] = 2
            self.routes[('C', 'E')] = 4
            self.routes[('5', 'E')] = 3.9
            self.routes[('3', 'D')] = 1.7
            self.routes[('D', 'E')] = 4
            self.routes[('4', 'E')] = 4.4
            self.routes[('1', '2')] = 1.4
            self.routes[('1', '3')] = 1.6
            self.routes[('2', '3')] = 1.7
            self.routes[('3', '4')] = 2.8
            self.routes[('A', 'F')] = 0.5
            self.routes[('B', 'F')] = 0.5

            self.routes[('A', '#')] = 4.7
            self.routes[('1', '#')] = 0.8
            self.routes[('2', '#')] = 2.7
            self.routes[('B', 'A')] = 3.5
            self.routes[('B', '5')] = 2.4
            self.routes[('C', 'B')] = 1
            self.routes[('D', 'C')] = 2
            self.routes[('E', 'C')] = 4
            self.routes[('E', '5')] = 3.9
            self.routes[('D', '3')] = 1.7
            self.routes[('E', 'D')] = 4
            self.routes[('E', '4')] = 4.4
            self.routes[('2', '1')] = 1.4
            self.routes[('3', '1')] = 1.6
            self.routes[('3', '2')] = 1.7
            self.routes[('4', '3')] = 2.8
            self.routes[('F', 'A')] = 0.5
            self.routes[('F', 'B')] = 0.5

            self.air_distances[('#', 'A')] = 2.5
            self.air_distances[('#', 'B')] = 3.8
            self.air_distances[('#', 'C')] = 3.3
            self.air_distances[('#', 'D')] = 2.65
            self.air_distances[('#', 'E')] = 4.4
            self.air_distances[('F', '#')] = 2.5
            self.air_distances[('#', 'F')] = 2.5
            self.air_distances[('#', '1')] = 0.5
            self.air_distances[('#', '2')] = 0.8
            self.air_distances[('#', '3')] = 1.8
            self.air_distances[('#', '4')] = 3.8
            self.air_distances[('#', '5')] = 5

            self.air_distances[('A', '#')] = 2.5
            self.air_distances[('A', 'B')] = 1.6
            self.air_distances[('A', 'C')] = 2
            self.air_distances[('A', 'D')] = 2.2
            self.air_distances[('A', 'E')] = 4.2
            self.air_distances[('A', 'F')] = 0.3
            self.air_distances[('A', '1')] = 2.7
            self.air_distances[('A', '2')] = 2.4
            self.air_distances[('A', '3')] = 2.9
            self.air_distances[('A', '4')] = 4.65
            self.air_distances[('A', '5')] = 3.45
            self.air_distances[('F', 'A')] = 0.3


            self.air_distances[('B', '#')] = 3.8
            self.air_distances[('B', 'A')] = 1.6
            self.air_distances[('B', 'C')] = 1
            self.air_distances[('B', 'D')] = 2.35
            self.air_distances[('B', 'E')] = 1
            self.air_distances[('B', 'F')] = 0.3
            self.air_distances[('F', 'B')] = 0.3
            self.air_distances[('B', '1')] = 4
            self.air_distances[('B', '2')] = 2.45
            self.air_distances[('B', '3')] = 3.3
            self.air_distances[('B', '4')] = 4.3
            self.air_distances[('B', '5')] = 1.6


            self.air_distances[('C', '#')] = 3.3
            self.air_distances[('C', 'A')] = 2
            self.air_distances[('C', 'B')] = 1
            self.air_distances[('C', 'D')] = 1.3
            self.air_distances[('C', 'E')] = 2.35
            self.air_distances[('C', 'F')] = 1.4
            self.air_distances[('F', 'C')] = 1.4
            self.air_distances[('C', '1')] = 2.8
            self.air_distances[('C', '2')] = 2.81
            self.air_distances[('C', '3')] = 2.4
            self.air_distances[('C', '4')] = 3.3
            self.air_distances[('C', '5')] = 1.7

            self.air_distances[('D', '#')] = 2.65
            self.air_distances[('D', 'A')] = 2.2
            self.air_distances[('D', 'B')] = 2.35
            self.air_distances[('D', 'C')] = 1.3
            self.air_distances[('D', 'E')] = 1.85
            self.air_distances[('D', 'F')] = 1.8
            self.air_distances[('F', 'D')] = 1.8
            self.air_distances[('D', '1')] = 1.9
            self.air_distances[('D', '2')] = 2
            self.air_distances[('D', '3')] = 1.2
            self.air_distances[('D', '4')] = 2
            self.air_distances[('D', '5')] = 2.7

            self.air_distances[('E', '#')] = 4.4
            self.air_distances[('E', 'A')] = 4.2
            self.air_distances[('E', 'B')] = 1
            self.air_distances[('E', 'C')] = 2.35
            self.air_distances[('E', 'D')] = 1.85
            self.air_distances[('E', 'F')] = 3
            self.air_distances[('F', 'E')] = 3
            self.air_distances[('E', '1')] = 2.75
            self.air_distances[('E', '2')] = 3.8
            self.air_distances[('E', '3')] = 2.75
            self.air_distances[('E', '4')] = 1.9
            self.air_distances[('E', '5')] = 2.36

            self.air_distances[('1', '#')] = 0.5
            self.air_distances[('1', 'A')] = 2.7
            self.air_distances[('1', 'B')] = 4
            self.air_distances[('1', 'C')] = 2.8
            self.air_distances[('1', 'D')] = 1.9
            self.air_distances[('1', 'E')] = 2.75
            self.air_distances[('1', 'F')] = 2.3
            self.air_distances[('F', '1')] = 2.3
            self.air_distances[('1', '2')] = 0.3
            self.air_distances[('1', '3')] = 1.2
            self.air_distances[('1', '4')] = 2.9
            self.air_distances[('1', '5')] = 4.5

            self.air_distances[('2', '#')] = 0.8
            self.air_distances[('2', 'A')] = 2.4
            self.air_distances[('2', 'B')] = 2.45
            self.air_distances[('2', 'C')] = 2.81
            self.air_distances[('2', 'D')] = 2
            self.air_distances[('2', 'E')] = 3.8
            self.air_distances[('2', 'F')] = 2.2
            self.air_distances[('F', '2')] = 2.2
            self.air_distances[('2', '1')] = 0.3
            self.air_distances[('2', '3')] = 0.92
            self.air_distances[('2', '4')] = 3.2
            self.air_distances[('2', '5')] = 4.4

            self.air_distances[('3', '#')] = 1.8
            self.air_distances[('3', 'A')] = 2.9
            self.air_distances[('3', 'B')] = 3.3
            self.air_distances[('3', 'C')] = 2.4
            self.air_distances[('3', 'D')] = 1.2
            self.air_distances[('3', 'E')] = 2.75
            self.air_distances[('3', 'F')] = 2.3
            self.air_distances[('F', '3')] = 2.3
            self.air_distances[('3', '1')] = 1.2
            self.air_distances[('3', '2')] = 0.92
            self.air_distances[('3', '4')] = 2
            self.air_distances[('3', '5')] = 3.9

            self.air_distances[('4', '#')] = 3.8
            self.air_distances[('4', 'A')] = 4.65
            self.air_distances[('4', 'B')] = 4.3
            self.air_distances[('4', 'C')] = 3.3
            self.air_distances[('4', 'D')] = 2
            self.air_distances[('4', 'E')] = 1.9
            self.air_distances[('4', 'F')] = 3.9
            self.air_distances[('F', '4')] = 3.9
            self.air_distances[('4', '1')] = 2.9
            self.air_distances[('4', '2')] = 3.2
            self.air_distances[('4', '3')] = 2
            self.air_distances[('4', '5')] = 4

            self.air_distances[('5', '#')] = 5
            self.air_distances[('5', 'A')] = 3.45
            self.air_distances[('5', 'B')] = 1.6
            self.air_distances[('5', 'C')] = 1.7
            self.air_distances[('5', 'D')] = 2.7
            self.air_distances[('5', 'E')] = 2.36
            self.air_distances[('5', 'F')] = 3
            self.air_distances[('F', '5')] = 3
            self.air_distances[('5', '1')] = 4.5
            self.air_distances[('5', '2')] = 4.4
            self.air_distances[('5', '3')] = 3.9
            self.air_distances[('5', '4')] = 4

        else:
            for p1, p2, d in routes:
                if p1 == '#':
                    self.routes[('#', p2)] = d
                elif p2 == '#':
                    self.routes[('#', p1)] = d
                else:
                    self.routes[(min(p1, p2), max(p1, p2))] = d


    def air_distance(self, p1, p2):
        return self.air_distances[(p1, p2)]

    def get_distance(self, point1, point2):
        if (point1, point2) in self.routes:
            return self.routes[(point1, point2)]
        elif (point2, point1) in self.routes:
            return self.routes[(point2, point1)]
        raise ValueError("Move is not allowed")
        # return float('inf')

    def get_legal_moves(self, p):
        legal_moves = []
        for p1, p2 in self.routes:
            if p == p1:
                legal_moves.append(p2)
            # elif p == p2:
            #     legal_moves.append(p1)
        return legal_moves


