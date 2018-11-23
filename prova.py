import numpy as np
import itertools
import random
import math
import sys
from parser import parse_cvrp
from Graph import Graph


def held_karp(map):
    """
    Implementation of Held-Karp, an algorithm that solves the Traveling
    Salesman Problem using dynamic programming with memoization.
    Parameters:
        dists: distance matrix
    Returns:
        A tuple, (cost, path).
    """
    n = map.get_dimension()

    # Maps each subset of the nodes to the cost to reach that subset, as well
    # as what node it passed before reaching this subset.
    # Node subsets are represented as set bits.
    C = {}

    # Set transition cost from initial state
    for k in range(1, n):
        C[(1 << k, k)] = (map.get_distance(k, 1), 0)

    # Iterate subsets of increasing length and store intermediate results
    # in classic dynamic programming manner
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            # Set bits for all nodes in this subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + map.get_distance(m, k), m))
                C[(bits, k)] = min(res)
    # We're interested in all bits but the least significant (the start state)
    bits = (2**n - 1) - 1

    # Calculate optimal cost
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + map.get_distance(k, 1), k))
    opt, parent = min(res)

    # Backtrack to find full path
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    # Add implicit start state
    path.append(0)

    return opt, list(reversed(path))


def get_cost_tsp_path(map, u, v, tsp_path):
    i = tsp_path.index(u)
    j = tsp_path.index(v)
    if i > j:
        l = j
        u = i
    else:
        l = i
        u = j
    k = 0
    while k != l:
        k += 1
    path_cost = 0
    while k >= l and k < u:
        path_cost += map.get_distance(k, k+1)
        k += 1
    return path_cost


def shortest_path(map, tsp_path):
    dimension = map.get_dimension()
    capacity = map.get_capacity()
    d = [float('inf')] * dimension
    pi = [None] * dimension
    depot = 0
    routes = []
    cost = 0
    distances = np.zeros(shape=(dimension, dimension))
    for i in range(len(tsp_path)):
        for j in range(i, len(tsp_path)):
            if i != j:
                u = tsp_path[i]
                v = tsp_path[j]
                distance_u_v = get_cost_tsp_path(map, u, v, tsp_path)
                distance = distance_u_v + map.get_distance(0, u) + map.get_distance(0, v)
                distances[u][v] = distance
    d[0] = 0
    for i in range(dimension):
        j = i
        load = 0
        while True:
            cost = distances[i][j] 
            if load <= capacity and d[i] + cost < d[j]:
                d[j] = d[i] + cost
                pi[j] = i 
            j = j + 1
            load += 1

            if j >= dimension or load > capacity:
                break
    return d, pi


def split(pi, tsp_path):
    routes = []
    j = len(pi) - 1
    while True:
        route = []
        print
        for k in range(pi[j], j):
            route.append(tsp_path[k])
        routes.append(route)
        j = pi[j]
        if j == 0:
            break
    return routes
    


map = parse_cvrp('cvrp/ulysses-n22-k4.vrp')
# opt, path = held_karp(map)
# path.remove(0)
# print path
d, pi = shortest_path(map, [16, 3, 17, 7, 12, 13, 14, 4, 10, 8, 9, 19, 20, 18, 6, 5, 11, 15, 21, 2, 1])
routes = split(pi, [16, 3, 17, 7, 12, 13, 14, 4, 10, 8, 9, 19, 20, 18, 6, 5, 11, 15, 21, 2, 1])
print routes