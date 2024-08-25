import heapq
from tracemalloc import Statistic

from direct.task.Task import pickup

import util


class DeliveryProblem:
    def __init__(self, start_state, orders, map_routes):
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
                if move == order.source:
                    new_pickup[index] = True
                    # order.mark_as_pickup()
                elif move == order.destination and new_pickup[index]:
                    # order.mark_as_delivered()
                    new_delivered[index] = True

            # if move in self.orders:
            #     index = self.orders.index(current_location, move)
            #     new_delivered[index] = True
            # elif (move, current_location) in self.orders:
            #     index = self.orders.index(current_location, move)
            #     new_delivered[index] = True

            successors.append(((move, new_pickup, new_delivered),(current_location, move), self.map_routes.get_distance(current_location,move)))

        return successors

        # for index, order in enumerate(self.orders):

            # if not delivered[index]:
            #     if current_location == order.source:
            #         new_delivered = delivered.copy()
            #         new_delivered[index] = True
            #         successor_state = (order.destination, new_delivered)
            #         step_cost = self.map_routes.get_distance(current_location, order.destination)
            #         successors.append((successor_state, order.destination, step_cost))
            #
            #     elif current_location != order.source:
            #         step_cost = self.map_routes.get_distance(current_location, order.source)
            #         successors.append(((order.source, delivered), order.source, step_cost))

        # return successors

    def get_cost_of_actions(self, actions):
        total_cost = 0
        for i in range(len(actions)):
            total_cost += self.map_routes.get_distance(actions[i][0], actions[i][1])
        return total_cost


def a_star_search(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    visited_nodes = list()
    fringe = util.PriorityQueue()
    first_state = problem.get_start_state()
    fringe.push([first_state, [], 0], heuristic(problem.get_start_state(), problem))
    while not fringe.isEmpty():
        current_node = fringe.pop()
        cur_state = current_node[0]
        cur_actions = current_node[1]
        if problem.is_goal_state(cur_state):
            return cur_actions
        if cur_state in visited_nodes:
            continue
        visited_nodes.append(cur_state)
        children = problem.get_successors(cur_state)
        for child in children:
            if child[0] not in visited_nodes:
                child_action = cur_actions + [child[1]]
                cost_of_actions = problem.get_cost_of_actions(child_action)
                fringe.push([child[0], child_action, cost_of_actions],
                            cost_of_actions + heuristic(child[0], problem))
    return []

class AStarSearch:
    @staticmethod
    def a_star(problem, heuristic):
        open_set = []
        start_state = problem.get_start_state()

        # Convert the start_state to a hashable type (tuple of tuples)
        start_state_hashed = tuple(tuple(x) if isinstance(x, list) else x for x in start_state)
        g_costs = {start_state_hashed: 0}
        heapq.heappush(open_set, (heuristic(start_state, problem), start_state, []))

        closed_set = []

        while open_set:
            f_cost, current_state, path = heapq.heappop(open_set)

            # Convert the current_state to a hashable type
            current_state_hashed = tuple(tuple(x) if isinstance(x, list) else x for x in current_state)

            if problem.is_goal_state(current_state):
                return path, g_costs[current_state_hashed]

            if current_state_hashed in closed_set:
                continue

            closed_set.append(current_state_hashed)

            for successor, action, step_cost in problem.get_successors(current_state):
                # Convert the successor to a hashable type
                successor_hashed = tuple(tuple(x) if isinstance(x, list) else x for x in successor)
                new_g_cost = g_costs[current_state_hashed] + step_cost

                if successor_hashed in closed_set:
                    continue

                if new_g_cost < g_costs.get(successor_hashed, float('inf')):
                    g_costs[successor_hashed] = new_g_cost
                    h_cost = heuristic(successor, problem)
                    total_cost = new_g_cost + h_cost
                    new_path = path + [action]
                    heapq.heappush(open_set, (total_cost, successor, new_path))

        return None, float('inf')


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    visited_nodes = []
    fringe = util.PriorityQueue()
    first_state = problem.get_start_state()
    fringe.push([first_state, [], 0], 0)
    while not fringe.isEmpty():
        current_node = fringe.pop()
        cur_state = current_node[0]
        cur_actions = current_node[1]
        if problem.is_goal_state(cur_state):
            return cur_actions
        if cur_state in visited_nodes:
            continue
        visited_nodes.append(cur_state)
        children = problem.get_successors(cur_state)
        for child in children:
            if child[0] not in visited_nodes:
                child_action = cur_actions + [child[1]]
                cost_of_actions = problem.get_cost_of_actions(child_action)
                fringe.push([child[0],
                             child_action, cost_of_actions], cost_of_actions)
    return []


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    visited_nodes = []
    fringe = util.Stack()
    first_state = problem.get_start_state()
    fringe.push([first_state, [], 0])
    while not fringe.isEmpty():
        current_node = fringe.pop()
        cur_state = current_node[0]
        cur_actions = current_node[1]
        if problem.is_goal_state(cur_state):
            return cur_actions
        if cur_state in visited_nodes:
            continue
        visited_nodes.append(cur_state)
        children = problem.get_successors(cur_state)
        for child in children:
            if child[0] not in visited_nodes:
                child_action = cur_actions+[child[1]]
                fringe.push([child[0], child_action, problem.get_cost_of_actions(child_action)])
    return []