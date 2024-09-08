
class DeliveryProblem:
    def __init__(self, start_state, orders, map_routes):
        """
        Initializes the delivery problem with the start state, orders, and map routes.
        """
        self.start_state = start_state
        self.orders = orders
        self.map_routes = map_routes
        self.expanded = 0

    def get_start_state(self):
        return self.start_state

    def is_goal_state(self, state):
        _, pickup, delivered = state
        return all(delivered)

    def get_successors(self, state):
        current_location, pickup, delivered = state
        successors = []
        self.expanded = self.expanded + 1
        legal_moves = self.map_routes.get_legal_moves(current_location)
        for move in legal_moves:
            new_pickup = pickup.copy()
            new_delivered = delivered.copy()
            for index, order in enumerate(self.orders):
                if move == order.source and not new_pickup[index]:
                    new_pickup[index] = True
                elif move == order.destination and new_pickup[index] and not \
                        new_delivered[index]:
                    new_delivered[index] = True

            successors.append(((move, new_pickup, new_delivered),
                               (current_location, move),
                               self.map_routes.get_distance(current_location,
                                                            move)))

        return successors

    def get_cost_of_actions(self, actions):
        total_cost = 0
        for i in range(len(actions)):
            total_cost += self.map_routes.get_distance(actions[i][0],
                                                       actions[i][1])
        return total_cost

class DeliveryCapacityProblem(DeliveryProblem):
    def __init__(self, start_state, orders, map_routes, deliveriesNum):
        super().__init__(start_state, orders,map_routes)
        self.deliveriesNum = deliveriesNum

    def get_successors(self, state):
        current_location, pickup, delivered = state
        successors = []
        self.expanded = self.expanded + 1
        legal_moves = self.map_routes.get_legal_moves(current_location)
        for move in legal_moves:
            new_pickup = pickup.copy()
            new_delivered = delivered.copy()
            for index, order in enumerate(self.orders):
                cur_delivered = new_delivered.count(True)
                cur_pickup = new_pickup.count(True)
                c = cur_pickup - cur_delivered
                if move == order.source and not new_pickup[index] and c < self.deliveriesNum:
                    new_pickup[index] = True
                elif move == order.destination and new_pickup[index] and not \
                        new_delivered[index]:
                    new_delivered[index] = True

            successors.append(((move, new_pickup, new_delivered),
                               (current_location, move),
                               self.map_routes.get_distance(current_location,
                                                            move)))

        return successors