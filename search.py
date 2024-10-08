import heapq
import util

class AStarSearch:
    @staticmethod
    def a_star(problem, heuristic):
        open_set = []
        start_state = problem.get_start_state()

        # Convert the start_state to a hashable type (tuple of tuples)
        start_state_hashed = tuple(
            tuple(x) if isinstance(x, list) else x for x in start_state)
        g_costs = {start_state_hashed: 0}
        heapq.heappush(open_set,
                       (heuristic(start_state, problem), start_state, []))

        closed_set = []

        while open_set:
            f_cost, current_state, path = heapq.heappop(open_set)

            # Convert the current_state to a hashable type
            current_state_hashed = tuple(
                tuple(x) if isinstance(x, list) else x for x in current_state)

            if problem.is_goal_state(current_state):
                return path, g_costs[current_state_hashed]

            if current_state_hashed in closed_set:
                continue

            closed_set.append(current_state_hashed)

            for successor, action, step_cost in problem.get_successors(
                    current_state):
                # Convert the successor to a hashable type
                successor_hashed = tuple(
                    tuple(x) if isinstance(x, list) else x for x in successor)
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


def depth_first_search(problem):
    """
    Performs Depth First Search to explore the deepest nodes in the search tree first.

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
    visited_nodes = list()  # Using a set for faster lookups
    fringe = util.Stack()
    first_state = problem.get_start_state()
    fringe.push(
        [first_state, [], 0])  # The stack stores tuples of (state, path, cost)

    while not fringe.isEmpty():
        current_node = fringe.pop()
        cur_state = current_node[0]
        cur_actions = current_node[1]
        cur_cost = current_node[2]

        if problem.is_goal_state(cur_state):
            return (
                cur_actions,
                cur_cost)  # Return the path and the cost as a tuple

        if cur_state in visited_nodes:
            continue

        visited_nodes.append(cur_state)
        children = problem.get_successors(cur_state)

        for child in children:
            child_state = child[0]
            child_action = child[1]
            child_cost = child[2]
            if child_state not in visited_nodes:
                new_actions = cur_actions + [child_action]
                new_cost = cur_cost + child_cost
                fringe.push([child_state, new_actions, new_cost])

    return ([], 0)  # If no solution found, return an empty path and zero cost


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    visited_nodes = list()
    fringe = util.Queue()
    first_state = problem.get_start_state()
    fringe.push(
        [first_state, [], 0])  # The stack stores tuples of (state, path, cost)

    while not fringe.isEmpty():
        current_node = fringe.pop()
        cur_state = current_node[0]
        cur_actions = current_node[1]
        cur_cost = current_node[2]

        if problem.is_goal_state(cur_state):
            return (
                cur_actions,
                cur_cost)  # Return the path and the cost as a tuple

        if cur_state in visited_nodes:
            continue

        visited_nodes.append(cur_state)
        children = problem.get_successors(cur_state)

        for child in children:
            child_state = child[0]
            child_action = child[1]
            child_cost = child[2]
            if child_state not in visited_nodes:
                new_actions = cur_actions + [child_action]
                new_cost = cur_cost + child_cost
                fringe.push([child_state, new_actions, new_cost])

    return ([], 0)


######################### Search Planning ##########################


class Node:
    """A node in a search tree."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        if parent:
            self.path_cost = parent.path_cost + path_cost
            self.depth = parent.depth + 1
        else:
            self.path_cost = path_cost
            self.depth = 0

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def nodePath(self):
        """Create a list of nodes from the root to this node."""
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        result.reverse()
        return result

    def path(self):
        """
        Create a path of actions from the start to the current state
        """
        actions = []
        currnode = self
        while currnode.parent:
            actions.append(currnode.action)
            currnode = currnode.parent
        actions.reverse()
        return actions

    def expand(self, problem):
        """Return a list of nodes reachable from this node."""
        return [Node(next, self, act, cost)
                for (next, act, cost) in problem.get_successors(self.state)]


REVERSE_PUSH = False


def graphSearch(problem, fringe):
    """Search through the successors of a problem to find a goal."""
    startstate = problem.get_start_state()
    fringe.push(Node(problem.get_start_state()))
    try:
        startstate.__hash__()
        visited = set()
    except:
        visited = list()

    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.is_goal_state(node.state):
            return node.path()
        try:
            inVisited = node.state in visited
        except:
            visited = list(visited)
            inVisited = node.state in visited

        if not inVisited:
            if isinstance(visited, list):
                visited.append(node.state)
            else:
                visited.add(node.state)
            nextNodes = node.expand(problem)
            if REVERSE_PUSH: nextNodes.reverse()
            for nextnode in nextNodes:
                fringe.push(nextnode)
    return None


def nullHeuristic(state, problem=None):
    """
    This heuristic is trivial.
    """
    return 0


def a_star_search_planning(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    return graphSearch(problem,
                       util.PriorityQueueWithFunction(
                           lambda node: node.path_cost + heuristic(node.state,
                                                                   problem)))
