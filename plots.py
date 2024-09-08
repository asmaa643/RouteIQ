import time

import numpy as np
from matplotlib import pyplot as plt
from planning_problem import max_level, PlanningProblem, level_sum, \
    null_heuristic
from search import *
from heuristics import maxPointAirDistHeuristic, \
    sumAirDistHeuristic, mstAirDistHeuristic
from search import a_star_search_planning


n_groups = 6
index = np.arange(n_groups)
bar_width = 0.1


def compare(problems_, probs_, routes):
    """
        Compares the performance of A* search and planning.
    """
    ############################### A* search ############################
    searcher = AStarSearch()
    a_star_max_times = []
    a_star_max_costs = []
    a_star_max_nodes = []
    a_star_results(a_star_max_costs, a_star_max_times, problems_, searcher,
                   a_star_max_nodes)
    ############################### BFS search ############################
    bfs_times = []
    bfs_costs = []
    bfs_nodes = []
    bfs_results(bfs_costs, bfs_nodes, bfs_times, problems_)
    ############################### DFS search ############################
    dfs_times = []
    dfs_costs = []
    dfs_nodes = []
    dfs_results(dfs_costs, dfs_nodes, dfs_times, problems_)
    ############################### Planning-max ############################
    planning_times_max = []
    planning_costs_max = []
    planning_nodes_max = []
    planning_results(planning_costs_max, planning_nodes_max,
                     planning_times_max,
                     probs_, routes, max_level)

    ############################### Planning-levelSum ########################
    planning_times_level = []
    planning_costs_level = []
    planning_nodes_level = []
    planning_results(planning_costs_level, planning_nodes_level,
                     planning_times_level,
                     probs_, routes, level_sum)
    ############################### Planning-zero ############################
    planning_times_zero = []
    planning_costs_zero = []
    planning_nodes_zero = []
    planning_results(planning_costs_zero, planning_nodes_zero,
                     planning_times_zero,
                     probs_, routes, null_heuristic)
    ############################ Comparing A* ###############################
    mst_nodes = []
    sum_nodes = []
    mst_costs = []
    sum_costs = []
    mst_times = []
    sum_times = []
    a_star_compare_results(a_star_max_costs, problems_, searcher, mst_costs,
                           sum_costs, mst_nodes, sum_nodes, mst_times,
                           sum_times)
    print("Comparing A* heuristics: Done.")

    ############################ Comparing Planning ##########################
    planning_compare(planning_costs_level, planning_costs_max,
                     planning_costs_zero)
    print("Comparing planning heuristics: Done.")
    ################################ Nodes ##################################
    a_star_planning(a_star_max_times, planning_times_max, planning_times_level,
                    planning_times_zero, dfs_times, bfs_times, mst_times,
                    sum_times, "times")
    print("Comparing Runtime: Done.")
    a_star_planning(a_star_max_costs, planning_costs_max, planning_costs_level,
                    planning_costs_zero, dfs_costs, bfs_costs, mst_costs,
                    sum_costs, "costs")
    print("Comparing costs: Done.")
    a_star_planning(a_star_max_nodes, planning_nodes_max, planning_nodes_level,
                    planning_nodes_zero, dfs_nodes, bfs_nodes, mst_nodes,
                    sum_nodes, "expanded nodes")
    print("Comparing expanded nodes: Done.")


def planning_compare(planning_costs_level, planning_costs_max,
                     planning_costs_zero):
    plt.figure(figsize=(10, 6))
    plt.xlabel('Orders number')
    plt.ylabel("Planning costs")
    plt.title("Planning search heuristics costs")
    plt.bar(index, planning_costs_max, 0.2, color='r',
            label='maxPlanning')
    plt.bar(index + 0.2, planning_costs_level, 0.2, color='c',
            label='levelSumPlanning')
    plt.bar(index + 0.2 * 2, planning_costs_zero, 0.2, color='m',
            label='zeroPlanning')
    plt.xticks(index + 0.2 * 2 / 2, range(1, n_groups + 1))
    plt.legend()
    plt.savefig("planning_costs.png", format='png',
                bbox_inches='tight')
    plt.show()


def dfs_results(dfs_costs, dfs_nodes, dfs_times, problems_):
    for i, problem in enumerate(problems_):
        if i == 6: break
        print("Run dfs over", i + 1, "orders")
        start_time = time.time()
        path, cost = depth_first_search(problem)
        end_time = time.time()
        # Calculate elapsed time in seconds and append to the list
        elapsed_time = (end_time - start_time)
        dfs_times.append(elapsed_time)
        dfs_costs.append(cost)
        dfs_nodes.append(problem.expanded)


def bfs_results(bfs_costs, bfs_nodes, bfs_times, problems_):
    for i, problem in enumerate(problems_):
        if i == 6: break
        print("Run bfs over", i + 1, "orders")
        # print([(order.source, order.destination) for order in problem.orders])

        start_time = time.time()

        path, cost = breadth_first_search(problem)
        end_time = time.time()

        # Calculate elapsed time in seconds and append to the list
        elapsed_time = (end_time - start_time)
        bfs_times.append(elapsed_time)
        bfs_costs.append(cost)
        bfs_nodes.append(problem.expanded)


def a_star_planning(a_star, planning_max, planning_level, planning_zero, dfs,
                    bfs, mst, sum_, graph_name):
    plt.figure(figsize=(10, 6))
    plt.bar(index, a_star, bar_width, color='b',
            label='A* MAX')
    plt.xlabel('Orders number')
    plt.ylabel("Solution's " + graph_name)
    plt.title("Solutions' " + graph_name + " across different orders numbers")
    plt.bar(index + bar_width, mst, bar_width, color='g',
            label='A* MST')
    plt.bar(index + bar_width * 2, sum_, bar_width, color='silver',
            label='A* SUM')
    plt.bar(index + bar_width * 3, planning_max, bar_width, color='r',
            label='maxPlanning')
    plt.bar(index + bar_width * 4, planning_level, bar_width, color='c',
            label='levelSumPlanning')
    plt.bar(index + bar_width * 5, planning_zero, bar_width, color='m',
            label='zeroPlanning')
    plt.bar(index + bar_width * 6, bfs, bar_width, color='lime',
            label='BFS')
    plt.bar(index + bar_width * 7, dfs, bar_width, color='orange',
            label='DFS')
    # plt.show()
    plt.xticks(index + bar_width * 7 / 2, range(1, n_groups + 1))
    plt.legend()
    plt.savefig(graph_name + ".png", format='png',
                bbox_inches='tight')
    plt.show()


def a_star_compare_results(a_star_costs, problems_, searcher, mst_costs,
                           sum_costs, mst_nodes, sum_nodes, mst_times,
                           sum_times):
    for i, problem in enumerate(problems_):
        if i == 6: break
        print("Run mst over", i + 1)
        start_time = time.time()
        path, mst_cost = searcher.a_star(problem,
                                         heuristic=mstAirDistHeuristic)
        end_time = time.time()
        elapsed_time = (end_time - start_time)
        mst_times.append(elapsed_time)
        mst_costs.append(mst_cost)
        mst_nodes.append(problem.expanded)
        print("Run sum over", i + 1)
        start_time = time.time()
        path, sum_cost = searcher.a_star(problem,
                                         heuristic=sumAirDistHeuristic)
        end_time = time.time()
        elapsed_time = (end_time - start_time)
        sum_times.append(elapsed_time)
        sum_costs.append(sum_cost)
        sum_nodes.append(problem.expanded)

    plt.figure(figsize=(10, 6))
    plt.xlabel('Orders number')
    plt.ylabel("Heuristic costs")
    plt.title("A* Search heuristics costs")
    plt.bar(index, a_star_costs, 0.2, color='b',
            label='max')
    plt.bar(index + 0.2, mst_costs, 0.2, color='g',
            label='mst')
    plt.bar(index + 0.2 * 2, sum_costs, 0.2, color='silver',
            label='sum')

    plt.xticks(index + 0.2 * 2 / 2, range(1, n_groups + 1))
    plt.legend()
    plt.savefig("max_vs_mst_vs_sum.png", format='png',
                bbox_inches='tight')
    plt.show()


def planning_results(planning_costs, planning_nodes, planning_times,
                     probs_, routes, func):
    for i, prob in enumerate(probs_):
        if i == 6: break
        print("Run planning over", i + 1, "orders")
        start_time = time.time()
        plan = a_star_search_planning(prob, func)
        end_time = time.time()
        elapsed_time = (end_time - start_time)
        planning_times.append(elapsed_time)
        if plan is not None:
            total = 0
            for act in plan:
                if "Move" in act.get_name():
                    w = act.get_name().split("_")
                    p1, p2 = w[1], w[3]
                    total += routes.get_distance(p1, p2)
            planning_costs.append(total)
        planning_nodes.append(prob.expanded)


def a_star_results(a_star_costs, a_star_times, problems_, searcher,
                   a_star_nodes):
    for i, problem in enumerate(problems_):
        if i == 6: break
        print("Run a_star over", i + 1, "orders")
        start_time = time.time()
        optimal_path, total_cost = searcher.a_star(problem,
                                                   heuristic=maxPointAirDistHeuristic)
        end_time = time.time()
        # Calculate elapsed time in seconds and append to the list
        elapsed_time = (end_time - start_time)
        a_star_times.append(elapsed_time)
        a_star_costs.append(total_cost)
        a_star_nodes.append(problem.expanded)


def capacity_results(probs_):
    """
        Compares the performance of A* search and planning.
    """
    ############################### A* search ############################
    searcher = AStarSearch()
    a_star_con_times = []
    a_star_con_costs = []
    a_star_con_nodes = []
    for i, problem in enumerate(probs_):
        if i == 7: break
        print("Run a_star with capacity over", i + 1, "orders")
        a_star_con_times.append([])
        a_star_con_costs.append([])
        a_star_con_nodes.append([])
        for j in range(7):
            start_time = time.time()
            optimal_path, total_cost = searcher.a_star(problem[j],
                                                       heuristic=maxPointAirDistHeuristic)
            end_time = time.time()
            # Calculate elapsed time in seconds and append to the list
            elapsed_time = (end_time - start_time)
            a_star_con_times[-1].append(elapsed_time)
            a_star_con_costs[-1].append(total_cost)
            a_star_con_nodes[-1].append(problem[j].expanded)

    plt.figure(figsize=(10, 6))
    plt.xlabel('Orders number')
    plt.ylabel("cost")
    plt.title("capacity")
    plot_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    index_ = np.arange(7)
    for j in range(7):
        to_plot = []
        for i in range(7):
            to_plot.append(a_star_con_costs[i][j])
        plt.bar(index_ + bar_width * j, to_plot, bar_width,
                color=plot_colors[j],
                label=("capacity" + str(j + 1)))

    plt.xticks(index_ + bar_width * 6 / 2, range(1, 7 + 1))
    plt.legend()
    plt.savefig("constrained" + ".png", format='png',
                bbox_inches='tight')
    plt.show()
