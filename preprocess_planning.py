
def create_domain_problem_files(name, lines, problem_orders):
    """
        Creates domain and problem files based on provided data.

    """
    domain_file = open("domain"+name, 'w')
    problem_file = open("problem"+name, 'w')
    map_points = set()
    actions = list()
    pre = list()
    process_domain(actions, lines, map_points)
    dests = []
    problem_file.write("Initial state: @#")
    process_problem(actions, dests, pre, problem_file, problem_orders)
    problem_file.write("\nGoal state:")
    for d in dests:
        problem_file.write(d)
    domain_file.write("Propositions:\n")
    for point in map_points:
        domain_file.write("@" + point + " ")
    for p in pre:
        domain_file.write(p)
    domain_file.write("\nActions:")
    for action in actions:
        domain_file.write(action)


def process_problem(actions, dests, pre, problem_file, problem_orders):
    """
    Processes problem orders to generate actions and initial/goal states.
    """
    for line in problem_orders:
        src, dest = line.rstrip('\n').split("-")
        problem_file.write(" order@" + src)
        actions.append(
            "\nName: Pickup_Order_" + dest + "\npre: @" + src + " order@"
            + src + "\nadd: has_Order_" + dest + "\ndelete: order@" + src)
        dests.append(" deliver_order_" + dest)
        actions.append(
            "\nName: Deliver_Order_" + dest + "\npre: @" + dest + " has_Order_"
            + dest + "\nadd: deliver_order_" + dest + "\ndelete: has_Order_" + dest)
        pre.append(
            "order@" + src + " has_Order_" + dest + " deliver_order_" + dest + " ")


def process_domain(actions, lines, map_points):
    """
    Processes domain data to generate propositions and actions.
    """
    for line in lines:
        point, neighbors = line.rstrip('\n').split(":")
        map_points.add(point)
        if neighbors:
            for neighbor in neighbors.split("-"):
                inf = neighbor[1:-1]
                n, dist = inf.split(",")
                actions.append(
                    "\nName: Move_" + point + "_to_" + n + "\npre: @"
                    + point + "\nadd: @" + n + "\ndelete: @" + point)
                actions.append(
                    "\nName: Move_" + n + "_to_" + point + "\npre: @"
                    + n + "\nadd: @" + point + "\ndelete: @" + n)