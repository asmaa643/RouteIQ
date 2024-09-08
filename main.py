import csv
import time
from CONSTANTS import *
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from delivery_problem import DeliveryProblem, DeliveryCapacityProblem
from planning_problem import max_level, PlanningProblem, null_heuristic
import preprocess_search
from plots import compare, capacity_results
from preprocess_planning import create_domain_problem_files
from search import *
from heuristics import maxPointAirDistHeuristic
from search import a_star_search_planning


"""
This script compares the performance of different search algorithms and heuristics 
in solving a delivery problem with multiple orders. It utilizes A* search and planning 
algorithms to find optimal delivery paths, based on various heuristics such as air distances 
and minimum spanning tree calculations.
"""

def show_path(path):
    """
        Displays the path of moves taken.
    """
    to_show = START_LOCATION
    for move in path:
        to_show += " -> " + move[1]
    print(to_show)


def create_A_search_problems(commands):
    """
        Prepares the A* search problems based on input commands.
    """
    map_routes, matrix, orders, points = read_input_files(commands)
    routes_ = preprocess_search.add_air_distances(map_routes, points, matrix)
    problems_ = []
    for i in range(len(orders)):
        start_state = (
            START_LOCATION, [False for _ in orders[:i + 1]],
            [False for _ in orders[:i + 1]])
        problems_.append(DeliveryProblem(start_state, orders[:i + 1], routes_))
    return problems_, routes_


def read_input_files(commands):
    map_file = open(commands[0], "r")
    data = list(map_file)
    map_routes = preprocess_search.get_map_routes(data)
    map_file.close()
    orders_file = open(commands[2], "r")
    orders = preprocess_search.get_orders_list(orders_file)
    orders_file.close()
    file_path = commands[1]  # Update with your file path
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    points = data[0][1:]  # The header row, without the first column
    matrix = [' '.join(row[1:]) for row in data[1:]]
    return map_routes, matrix, orders, points


def create_capacity_A_search_problems(commands):
    """
        Prepares the A* search problems based on input commands.
    """
    map_routes, matrix, orders, points = read_input_files(commands)
    routes_ = preprocess_search.add_air_distances(map_routes, points, matrix)
    problems_ = []
    for i in range(len(orders)):
        problems_.append([])
        start_state = (
            START_LOCATION, [False for _ in orders[:i + 1]],
            [False for _ in orders[:i + 1]])
        for j in range(8):
            (problems_[-1]).append(
                DeliveryCapacityProblem(start_state, orders[:i + 1], routes_, j + 1))
    return problems_, routes_


def create_planning_problem(commands):
    """
        Prepares planning problems for comparison.
    """
    map_file = open(commands[0], "r")
    data = list(map_file)
    orders_file = open(commands[2], "r")
    orders = list(orders_file)
    problems_ = []
    for i in range(len(orders)):
        create_domain_problem_files(commands[2], data, orders[:i + 1])
        domain = DOMAIN + commands[2]
        problem = PROBLEM + commands[2]
        problems_.append(PlanningProblem(domain, problem))
    map_file.close()
    orders_file.close()
    return problems_

def run_num_orders(search, planning, num, routes, capacity, choice):
    """
        Runs the search and planning algorithms for a specific number of orders.
    """
    print(ORDERS_LIST,)
    for order in (search[num - 1]).orders:
        print("(", order.source, ",", order.destination, ")",)
    choice(search, planning, num, routes, capacity)


def a_star_plan(search, planning, num, routes, capacity):
    searcher = AStarSearch()
    search_problem = search[num - 1]
    if capacity != -1:
        search_problem = DeliveryCapacityProblem(
            search_problem.start_state, search_problem.orders,
            search_problem.map_routes, capacity)
    start_time = time.time()
    optimal_path, total_cost = searcher.a_star(search_problem,
                                               heuristic=maxPointAirDistHeuristic)
    end_time = time.time()
    elapsed_time = (end_time - start_time)
    print(A_STAR_PATH, total_cost, "in %.2f seconds" % elapsed_time, PATH)
    show_path(optimal_path)

def planning_plan(search, planning, num, routes, capacity):
    planning_problem = planning[num - 1]
    start_time = time.time()
    if num > 6:
        plan = a_star_search_planning(planning_problem, null_heuristic)
    else:
        plan = a_star_search_planning(planning_problem, max_level)
    end_time = time.time()
    elapsed_time = (end_time - start_time)
    check_plan(elapsed_time, plan, routes)

def check_plan(elapsed_time, plan, routes):
    if plan is not None:
        plan_ = START_LOCATION
        total = 0
        for act in plan:
            print(act.get_name())
            if "Move" in act.get_name():
                w = act.get_name().split("_")
                p1, p2 = w[1], w[3]
                total += routes.get_distance(p1, p2)
                plan_ += " -> " + p2
        print(PLAN_FOUND % (len(plan), total, elapsed_time))
        print(PLANNING_PATH)
        print(plan_)
    else:
        print(PLAN_NOT_FOUND % elapsed_time)


def user_problem(commands, capacity, choice, num=0):
    input(SHOW_MAP)
    show_map()
    user_orders = open(USERS_FILE, 'w')
    # Prompt the user for input after the image is closed
    print(INSTRUCTION)
    get_inputs(user_orders, num)
    user_orders.close()
    problems_, routes_ = create_A_search_problems([commands[0], commands[1], USERS_FILE])
    probs_ = create_planning_problem([commands[0], commands[1], USERS_FILE])
    if len(problems_) > 0:
        run_num_orders(problems_, probs_, 0, routes_, capacity, choice)
    else:
        print("No orders were entered.")


def show_map():
    plt.figure(figsize=(10, 6))
    # Load an image from a file
    img = mpimg.imread(MAP_JPG)  # Replace with your image file path
    # Display the image
    plt.imshow(img)
    plt.axis('off')  # Hide the axes
    plt.show(block=True)  # Ensures the window remains open


def get_inputs(user_orders, num):
    orders_list = []
    lst = True
    if num > 0:
        lst = False
    user_input = input(USER_INPUT)
    while num > 0 or (lst and user_input.lower() != DONE):
        num -= 1
        if '-' in user_input and user_input.count('-') == 1 and user_input[
            1] == '-':
            src, dest = user_input.split('-')
            if src not in SOURCES or dest not in DESTS:
                print(WRONG_FORMAT)
                user_input = input(USER_INPUT)
                num += 1
                continue
        else:
            print(WRONG_FORMAT)
            user_input = input(USER_INPUT)
            num += 1
            continue
        if user_input not in orders_list:
            user_orders.write(user_input + '\n')
            orders_list.append(user_input)
            if num > 0 or lst:
                user_input = input(USER_INPUT)
        else:
            user_input = input(REPEATED_INPUT)
            num += 1
            continue


def main():
    """
    Processes the command used to run the game from the command line.
    """
    from optparse import OptionParser
    usage_str = """
    USAGE:      python main.py <options>
    EXAMPLES:  --ordersNum=7 --capacity=3 --choice=a_star
    """
    parser = OptionParser(usage_str)
    parser.add_option('--map', dest='map_file',
                      help='the map file to read from', default='map.txt')
    parser.add_option('--orders', dest='orders_file',
                      help='the orders file to read from',
                      default='orders.txt')
    parser.add_option('--air', dest='air_distances_file',
                      help='the air distances file to read from',
                      default='air_distances.csv')
    parser.add_option('--ordersNum', dest='num',
                      type='int', nargs=1,
                      help='the number of default orders.', default=-1)
    parser.add_option('--capacity', dest='capacity',
                      type='int', nargs=1,
                      help='the capacity of the motorcycle.', default=-1)

    parser.add_option('--choice', dest='search_choice',
                      metavar='FUNC', help='search solution choice to use.',
                      type='choice',
                      choices=['a_star', 'planning'], default='a_star')
    parser.add_option('--user', dest='user', type='int',
                      help='run the program in user input mode', default=0)
    parser.add_option('--results', dest='results', type='int',
                      help='run the results code', default=0)

    options, _ = parser.parse_args()
    if options.num == -1 and options.user == 0 and options.results == 0:
        print("You didn't enter any choice!")
        exit(1)
    elif (options.num > -1 or options.user == 1) and options.results == 1:
        print(RESULTS_USAGE)
        exit(1)
    commands = [options.map_file, options.air_distances_file,options.orders_file]
    problems, routes = create_A_search_problems(commands)
    probs = create_planning_problem(commands)

    choices = {A_STAR: a_star_plan, PLANNING: planning_plan}

    if options.capacity != -1 and options.capacity <= 0:
        print(CAPACITY_USAGE)
        exit(1)
    elif options.capacity != -1 and options.search_choice == PLANNING:
        print(CAPACITY_NOT_SUPPORTED)
        exit(1)
    elif options.user == 1 and options.num == -1:
        user_problem(commands, options.capacity, choices[options.search_choice])
    elif options.user == 1 and options.num > -1:
        user_problem(commands, options.capacity, choices[options.search_choice],
                     options.num)
    elif options.user == 0 and options.num != -1:
        if options.num > 8 or options.num < 1:
            print(ORDERS_NUM_USAGE)
            exit(1)
        run_num_orders(problems, probs, options.num, routes, options.capacity,
                       choices[options.search_choice])
    elif options.results == 1:
        compare(problems, probs, routes)
        capacity_probs, _ = create_capacity_A_search_problems(commands)
        capacity_results(capacity_probs)
    else:
        raise Exception('unrecognized options')


if __name__ == '__main__':
    main()
