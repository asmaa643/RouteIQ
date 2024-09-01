from proposition_layer import PropositionLayer
from plan_graph_level import PlanGraphLevel
from pgparser import PgParser, Action


class PlanningProblem:
    """
       Represents a planning problem based on a domain and problem file.
       Manages actions, propositions, initial state, and goal state.
    """

    def __init__(self, domain_file, problem_file):
        """
        Constructor
        """
        p = PgParser(domain_file, problem_file)
        self.actions, self.propositions = p.parse_actions_and_propositions()
        # list of all the actions and list of all the propositions

        initial_state, goal = p.parse_problem()
        # the initial state and the goal state are lists of propositions

        self.initialState = frozenset(initial_state)
        self.goal = frozenset(goal)

        self.create_noops()
        # creates noOps that are used to propagate existing propositions from one layer to the next

        PlanGraphLevel.set_actions(self.actions)
        PlanGraphLevel.set_props(self.propositions)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the initial state of the planning problem.
        """
        return self.initialState

    def is_goal_state(self, state):
        """
        Checks if the given state satisfies the goal state.
        """
        return not self.goal_state_not_in_prop_layer(state)

    def get_successors(self, state):
        """
        Returns a list of triples,
        (successor, action, step_cost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'step_cost' is the incremental
        cost of expanding to that successor, 1 in our case.
        """
        self.expanded += 1
        successors = []
        for action in self.actions:
            if action.is_noop() or not action.all_preconds_in_list(state):
                continue
            successor_state = set(state)
            for prop_to_delete in action.get_delete():
                successor_state.discard(prop_to_delete)
            for prop_to_add in action.get_add():
                successor_state.add(prop_to_add)
            successors.append((frozenset(successor_state), action, 1))
        return successors

    @staticmethod
    def get_cost_of_actions(actions):
        return len(actions)

    def goal_state_not_in_prop_layer(self, propositions):
        """
         Receives a list of propositions (propositions) and returns true
        if not all the goal propositions are in that list
        """
        for goal in self.goal:
            if goal not in propositions:
                return True
        return False

    def create_noops(self):
        """
        Creates the noOps that are used to propagate propositions from one layer to the next
        """
        for prop in self.propositions:
            name = prop.name
            precon = []
            add = []
            precon.append(prop)
            add.append(prop)
            delete = []
            act = Action(name, precon, add, delete, True)
            self.actions.append(act)


def max_level(state, planning_problem):
    """
    The heuristic value is the number of layers required to expand all goal propositions.
    """
    prop_layer_init = PropositionLayer()  # Create a new proposition layer
    for prop in state:
        prop_layer_init.add_proposition(
            prop)  # Update the proposition layer with the propositions of the state

    pg_init = PlanGraphLevel()  # Create a new plan graph level
    pg_init.set_proposition_layer(
        prop_layer_init)  # Update the new plan graph level with the proposition layer

    level = 0
    while not planning_problem.is_goal_state(
            pg_init.get_proposition_layer().get_propositions()):
        prev_props = pg_init.get_proposition_layer().get_propositions()  # Get current propositions

        pg_next = PlanGraphLevel()  # Create a new next level plan graph
        pg_next.expand_without_mutex(
            pg_init)  # Expand without computing mutex relations
        pg_init = pg_next  # Move to the next level
        level += 1

        current_props = pg_init.get_proposition_layer().get_propositions()  # Get new propositions
        if len(current_props) == len(prev_props):
            return float(
                'inf')  # If no changes, return infinity (goal not reachable)
    return level


def is_fixed(graph, level):
    """
    Checks if we have reached a fixed point,
    """
    if level == 0:
        return False
    return len(graph[level].get_proposition_layer().get_propositions()) == len(
        graph[level - 1].get_proposition_layer().get_propositions())


def null_heuristic(*args, **kwargs):
    return 0
