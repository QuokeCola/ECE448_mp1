# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)
import math

visited_queue = []


def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
    route_queue = []
    stack = [maze.getStart()]
    result = bfs_search_func(maze, [maze.getStart()], [stack])
    # TODO: Write your code here
    # return path, num_states_explored
    return result[1], 0


def bfs_search_func(maze, fathers, search_queues):
    global visited_queue
    next_search_queue = []
    next_fathers = []
    for search_queue in search_queues:
        for point in search_queue:
            if not (point in visited_queue):
                if maze.isObjective(point[0], point[1]):
                    route = [point]
                    route.insert(0, fathers[search_queues.index(search_queue)])
                    return [True, route]
                visited_queue.append(point)
                next_search_queue.append(maze.getNeighbors(point[0], point[1]))
                next_fathers.append(point)
    result = bfs_search_func(maze, next_fathers, next_search_queue)
    if result[0]:
        for search_queue in search_queues:
            if search_queue.__contains__(result[1][0]):
                result[1].insert(0, fathers[search_queues.index(search_queue)])
                return result


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    result = dfs_search_func(maze, [], maze.getStart())

    return result[1], 0


def dfs_search_func(maze, finalized_queue_, start_point):
    global visited_queue
    neighbors = maze.getNeighbors(start_point[0], start_point[1])
    finalized_queue = finalized_queue_
    # Generate the new queue
    visited_queue.append(start_point)
    for point in neighbors:
        if not (point in visited_queue):
            # Go through the valid neighbors
            finalized_queue.append(point)
            if maze.isObjective(point[0], point[1]):
                finalized_queue.append(point)
                return [True, finalized_queue]
            result = dfs_search_func(maze, finalized_queue, point)
            if result[0]:
                return [True, result[1]]
            else:
                finalized_queue.remove(point)
                pass
    return [False]


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    result = greedy_search_func(maze, [], maze.getStart())
    print(result)
    return result[1], 0


def get_dist(point, objective, current_length):
    return abs(point[0] - objective[0]) + abs(point[1] - objective[1]) + current_length


def greedy_search_func(maze, finalized_queue_, start_point):
    global visited_queue
    objective = maze.getObjectives()
    objective = objective[0]
    neighbors = maze.getNeighbors(start_point[0], start_point[1])
    searched_queue = []
    for point in neighbors:
        searched_queue.append({"point": point, "dist": get_dist(point, objective, 0)})
    searched_queue = sorted(searched_queue, key=lambda i: i['dist'])

    finalized_queue = finalized_queue_
    # Generate the new queue
    visited_queue.append(start_point)
    for point in searched_queue:
        if not (point["point"] in visited_queue):
            # Go through the valid neighbors
            finalized_queue.append(point["point"])
            if maze.isObjective(point["point"][0], point["point"][1]):
                finalized_queue.append(point["point"])
                return [True, finalized_queue]
            result = greedy_search_func(maze, finalized_queue, point["point"])
            if result[0]:
                return [True, result[1]]
            else:
                finalized_queue.remove(point["point"])
                pass
    return [False]


def astar(maze):
    result = astar_search_func(maze, [], maze.getStart())
    # return path, num_states_explored
    return result[1], 0


def get_astar_dist(point, objective, current_length):
    return math.sqrt((point[0] - objective[0])**2 + abs(point[1] - objective[1])**2) + current_length


def astar_search_func(maze, finalized_queue_, start_point):
    global visited_queue
    objective = maze.getObjectives()
    objective = objective[0]
    neighbors = maze.getNeighbors(start_point[0], start_point[1])
    searched_queue = []
    for point in neighbors:
        searched_queue.append({"point": point, "dist": get_astar_dist(point, objective, len(finalized_queue_))})
    searched_queue = sorted(searched_queue, key=lambda i: i['dist'])

    finalized_queue = finalized_queue_
    # Generate the new queue
    visited_queue.append(start_point)
    for point in searched_queue:
        if not (point["point"] in visited_queue):
            # Go through the valid neighbors
            finalized_queue.append(point["point"])
            if maze.isObjective(point["point"][0], point["point"][1]):
                finalized_queue.append(point["point"])
                return [True, finalized_queue]
            result = astar_search_func(maze, finalized_queue, point["point"])
            if result[0]:
                return [True, result[1]]
            else:
                finalized_queue.remove(point["point"])
                pass
    return [False]
