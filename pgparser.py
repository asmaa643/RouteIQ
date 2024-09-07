from proposition import Proposition


class PgParser:
    """
     A utility class for parsing the domain and problem files used in automated planning.
    """

    def __init__(self, domain_file, problem_file):
        """
         Constructor to initialize the parser with domain and problem files.
        """
        self.domain_file = domain_file
        self.problem_file = problem_file

    def parse_actions_and_propositions(self):
        """
            Parses the domain file specified by self.domain_file to extract Proposition and Action objects.
            Updates actions with the corresponding Proposition instances for their preconditions, add effects,
            and delete effects.
        """
        propositions = []
        f = open(self.domain_file, 'r')
        _ = f.readline()
        proposition_line = f.readline()
        words = [word.rstrip() for word in proposition_line.split(" ") if
                 len(word.rstrip()) > 0]
        for i in range(0, len(words)):
            propositions.append(Proposition(words[i]))
        actions = []
        f = open(self.domain_file, 'r')
        line = f.readline()
        while line != '':
            words = [word.rstrip() for word in line.split(" ") if
                     len(word.rstrip()) > 0]
            if words[0] == 'Name:':
                name = words[1]
                line = f.readline()
                precond = []
                add = []
                delete = []
                words = [word.rstrip() for word in line.split(" ") if
                         len(word.rstrip()) > 0]
                for i in range(1, len(words)):
                    precond.append(Proposition(words[i]))
                line = f.readline()
                words = [word.rstrip() for word in line.split(" ") if
                         len(word.rstrip()) > 0]
                for i in range(1, len(words)):
                    add.append(Proposition(words[i]))
                line = f.readline()
                words = [word.rstrip() for word in line.split(" ") if
                         len(word.rstrip()) > 0]
                for i in range(1, len(words)):
                    delete.append(Proposition(words[i]))
                act = Action(name, precond, add, delete)
                for prop in add:
                    self.find_prop_by_name(prop, propositions).add_producer(
                        act)
                actions.append(act)
            line = f.readline()

        for a in actions:
            new_pre = [p for p in propositions if
                       p.name in [q.name for q in a.pre]]
            new_add = [p for p in propositions if
                       p.name in [q.name for q in a.add]]
            new_delete = [p for p in propositions if
                          p.name in [q.name for q in a.delete]]
            a.pre = new_pre
            a.add = new_add
            a.delete = new_delete

        return [actions, propositions]

    @staticmethod
    def find_prop_by_name(name, propositions):
        for prop in propositions:
            if prop == name:
                return prop

    def parse_problem(self):
        """
            Parses the domain file specified by self.domain_file to extract Proposition and Action objects.
            Updates actions with the corresponding Proposition instances for their preconditions, add effects,
            and delete effects.
            """
        init = []
        goal = []
        f = open(self.problem_file, 'r')
        line = f.readline()
        words = [word.rstrip() for word in line.split(" ") if
                 len(word.rstrip()) > 0]
        for i in range(2, len(words)):
            init.append(Proposition(words[i]))
        line = f.readline()
        words = [word.rstrip() for word in line.split(" ") if
                 len(word.rstrip()) > 0]
        for i in range(2, len(words)):
            goal.append(Proposition(words[i]))
        return init, goal


class Action(object):
    """
    The action class is used to define operators.
    Each action has a list of preconditions, an "add list" of positive effects,
    a "delete list" for negative effects, and the name of the action.
    Two actions are considered equal if they have the same name.
    """

    def __init__(self, name, pre, add, delete, is_noop=False):
        """
        Constructor to initialize an action with its name, preconditions, add effects, and delete effects.
        """
        self.pre = pre  # list of the precondition propositions
        self.add = add  # list of the propositions that will be added after applying the action
        self.delete = delete  # list of the propositions that will be deleted after applying the action
        self.name = name  # the name of the action as string
        self.noOp = is_noop  # true if the action is a noOp

    def get_pre(self):
        """
        Returns the list of preconditions
        """
        return self.pre

    def get_add(self):
        """
        Returns the list of propositions to be added.
        """
        return self.add

    def get_delete(self):
        """
        Returns the list of propositions to be deleted.
        """
        return self.delete

    def get_name(self):
        """
         Returns the name of the action.
        """
        return self.name

    def is_pre_cond(self, prop):
        """
         Checks if a proposition is a precondition for the action.
        """
        return prop in self.pre

    def is_pos_effect(self, prop):
        """
        Checks if a proposition is a positive effect of the action.
        """
        return prop in self.add

    def is_neg_effect(self, prop):
        """
        Checks if a proposition is a negative effect of the action.
        """
        return prop in self.delete

    def all_preconds_in_list(self, propositions):
        """
       Checks if all preconditions of the action are in a given list of propositions.
        """
        for pre in self.pre:
            if pre not in propositions:
                return False
        return True

    def is_noop(self):
        """
        Returns whether the action is a no-op.
        """
        return self.noOp

    def __eq__(self, other):
        """
         Checks if two actions are equal based on their names.
        """
        return (isinstance(other, self.__class__)
                and self.name == other.name)

    def __str__(self):
        """
        Returns the string representation of the action (its name).
        """
        return self.name

    def __ne__(self, other):
        """
        Checks if two actions are not equal.
        """
        return not self.__eq__(other)

    def __lt__(self, other):
        """
        Compares two actions based on their names.
        """
        return self.name < other.name

    def __hash__(self):
        """
        Returns the hash of the action's name.
        """
        return hash(self.name)
