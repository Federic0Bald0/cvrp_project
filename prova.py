import numpy as np
import itertools
import random
import sys
from parser import parse_cvrp


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
        C[(1 << k, k)] = (map.get_value(k, 1), 0)

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
                    res.append((C[(prev, m)][0] + map.get_value(m, k), m))
                C[(bits, k)] = min(res)

    # We're interested in all bits but the least significant (the start state)
    bits = (2**n - 1) - 1

    # Calculate optimal cost
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + map.get_value(k, 1), k))
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
        path_cost += map.get_value(k, k+1)
        k += 1
    return path_cost


def dijkstra(map, tsp_path):
    dimension = map.get_dimension()
    capacity = map.get_capacity()
    routes = []
    cost = 0
    possible_path = []
    while (len(tsp_path)) >= capacity:
        for i in range(1, len(tsp_path)):
            j = i + capacity
            if j > len(tsp_path):
                j = j % capacity
                u = tsp_path[i]
                v = tsp_path[j]
                distance_u_v = get_cost_tsp_path(map, u, v, tsp_path)
                distance = distance_u_v + map.get_value(0, u) + map.get_value(0, v)
                possible_path.append((distance, [u, v]))
        possible_path.sort(key=lambda x: x[0], reverse=True)
        selected = possible_path.pop()
        cost += selected[0]
        routes.append(selected[1])
        remove_list = []
        for k in range(len(tsp_path)-1):
            if tsp_path[k] != u:
                continue
            elif tsp_path[k] == v:
                break
            else:
                remove_list.append(u)
                u = tsp_path[k+1]
        for i in remove_list:
            tsp_path.remove(i)

    return routes, cost



map = parse_cvrp('cvrp/ulysses-n16-k3.vrp')
opt, path = held_karp(map)
print path
print dijkstra(map, path)
