# coding: utf-8
from __future__ import division

import time
import math
import random
import itertools
import numpy as np
from parser import parse_cvrp


# -----------------------------------------------------------------------------
# CONSTRUCTIVE METHODS FOR CVRP 
# -----------------------------------------------------------------------------
# Clark and Wright savings algorithm 
def clark_wright(graph):
    savings = []
    routes = []
    dimension = graph.get_dimension()
# -----------------------------------------------------------------------------
# compute sanvings as s[i][j] = dist[i][0] + dist[j][0] - dist[i][j]
# each saving is a tuple (saving, i, j), where i, j are refering 
# to the nodes with the associated saving
    for i in range(dimension):
        for j in range(i+1, dimension):
            payload = graph.get_distance(i, 0) + \
                    graph.get_distance(0, j) - \
                    graph.get_distance(i, j)
            savings.append((float(payload), i, j))
# -----------------------------------------------------------------------------
# sort saving in descending order
    savings.sort(key=lambda x: x[0], reverse=True)
# -----------------------------------------------------------------------------
# initialize routes
# zeros at the beginning and the end of the route are implicit
    for x in range(1, dimension):
        routes.append([x])
# -----------------------------------------------------------------------------
# merge routes if feasible. This means we don't exceed capacity
    for saving in savings:
        i = saving[1]
        j = saving[2]
        route_1 = None
        route_2 = None
        # ---------------------------------------------------------------------
        # search the routes that has as first node and/or last element,
        # except the depot, i and j
        for k in range(len(routes)):
            # route (0, i, ...)
            if i == routes[k][0]:
                route_1 = routes[0]
            # route (..., j, 0)
            if j == routes[k][len(routes[k])-1]:
                route_2 = routes[k]
            # -----------------------------------------------------------------
            # if the selected ruote are valid for the merge, means:
            # routes are different
            # routes aren't none
            # merging the routes would not exceed the capacity of the cvrp
            if route_1 is not None and route_2 is not None and route_1 != route_2 and \
             compute_load(graph, route_1, route_2) <= graph.get_capacity():
                    # print route_1, route_2, len(route_1) + len(route_2), graph.get_capacity()
                    new_route = np.append(route_1, route_2)
                    cost_new_route = sum([graph.get_distance(new_route[u], new_route[u+1])
                                        for u in range(len(new_route)-1)])
                    routes.remove(route_1)
                    
                    routes.remove(route_2)
                    routes.append(list(new_route))
                    # ---------------------------------------------------------
                    # update the savings with the new saving
                    savings.remove(saving)
                    savings.append((float(graph.get_distance(i, 0) +
                                        graph.get_distance(0, j) -
                                        cost_new_route), i, j))
                    savings.sort(key=lambda x: x[0], reverse=True)
                    break
# -----------------------------------------------------------------------------
# compute total cost of the cvrp
    tot_cost = 0
    for route in routes:
        for i in range(len(route)-1):
            tot_cost += graph.get_distance(route[i], route[i+1])
        tot_cost += graph.get_distance(0, route[0])
        tot_cost += graph.get_distance(0, route[len(route)-1])

    return routes, tot_cost


def compute_load(graph, route_1, route_2):
    load = 0
    for i in route_1:
        load += graph.get_demand(i)
    for i in route_2:
        load += graph.get_demand(i)
    return load



# -----------------------------------------------------------------------------
# 2-PHASE ALGORITHM FOR CVRP
# -----------------------------------------------------------------------------
# Route-First, Cluster-Second algorithm
# -----------------------------------------------------------------------------
# 2-approximate algorithm for tsp problem. 
# This algoritm takes as approximation of solution a depth walk over a MST
def tsp(graph, s, n):
    mst = prim(graph, s, n)
    tsp_tour = depth_visit(mst, 0, [])
    return tsp_tour 


def prim(graph, s, n):
    key = [float('inf')] * n # distances
    pi = [None] * n # predecessors
    key[s] = 0
    mst_set = [False] * n # nodes in the minimum path
    for i in range(n):
        u = min_key(key, mst_set, n)
        mst_set[u] = True
        for v in range(n):       
            if graph.get_distance(u, v) < key[v] and mst_set[v] == False:
                key[v] = graph.get_distance(u, v)
                pi[v] = u
    mst = [(v, pi[v], key[v]) for v in range(1, n)]
    return mst


def min_key(key, mst_set, n): 
  
    min = float('inf')
    min_index = None
    for v in range(n): 
        if key[v] < min and mst_set[v] == False: 
            min = key[v] 
            min_index = v 

    return min_index 
    

def depth_visit(mst, s, visit):
    visit.append(s)
    neigh = [x[0] for x in mst if x[1] == s]
    for city in neigh:
        depth_visit(mst, city, visit)
    return visit


def bellman_split(graph, tsp_path):
    dimension = graph.get_dimension()
    capacity = graph.get_capacity()
    d = [float('inf')] * dimension # distances
    pi = [None] * dimension # predecessor
    d[0] = 0
    pi[0] = 0
    for t in range(dimension):
        load = 0
        i = t + 1
        while i < dimension and load + graph.get_demand(i) <= capacity:
            load += graph.get_demand(i)
            if i == t + 1:
                cost = graph.get_distance(0, tsp_path[i])
            else:
                cost += graph.get_distance(tsp_path[i-1], tsp_path[i])
            if d[tsp_path[t]] + cost + graph.get_distance(tsp_path[i], 0) < d[tsp_path[i]]:
                d[tsp_path[i]] = d[tsp_path[t]] + cost + graph.get_distance(tsp_path[i], 0)
                pi[tsp_path[i]] = tsp_path[t]
            i += 1
    return d, pi


# def split(graph, tsp_path):
#     dimension = graph.get_dimension()
#     capacity = graph.get_capacity()
#     d = [float('inf')] * dimension # distances
#     pi = [None] * dimension # predecessor
#     d[0] = 0
#     pi[0] = 0
#     for i in range(1, dimension):
#         j = i
#         load = 0
#         while True:
#             load += graph.get_demand(j)
#             if i == j:
#                 cost = graph.get_distance(0, tsp_path[i]) + \
#                        graph.get_distance(0, tsp_path[i])
#             else:
#                 cost = cost - graph.get_distance(tsp_path[j-1], 0) + \
#                        graph.get_distance(tsp_path[j-1], tsp_path[j]) + \
#                        graph.get_distance(0, tsp_path[j])
#             if load <= capacity and d[tsp_path[i-1]] + cost < d[tsp_path[j]]:
#                 d[tsp_path[j]] = d[tsp_path[i-1]] + cost
#                 pi[tsp_path[j]] = tsp_path[i-1]
#             j += 1
#             if j >= dimension or load > capacity:
#                 break
#     return d, pi


def extract(dimension, d, pi):
    routes = []
    j = dimension - 1
    preds = list(set(pi))
    for p in preds:
        route = []
        for i in range(1, len(pi)):
            if p == pi[i]:
                route.append(i)
        routes.append(route)
    tot_cost = 0
    for route in routes:
        tot_cost += d[route[len(route)-1]]
    return routes, tot_cost


# def extract(dimension, d, pi, tsp_path):
#     routes = []
#     print pi
#     print tsp_path
#     j = dimension - 1
#     while True:
#         route = []
#         for k in range(pi[j]+1, j):
#             route.append(k)
#         if route:
#             routes.append(route)
#         j = pi[j]
#         if j == 0:
#             break
#     tot_cost = 0
#     for route in routes:
#         tot_cost += d[route[len(route)-1]]
#     return routes, tot_cost


def route_first_cluster_second(graph):
    tsp_tour = tsp(graph, 0, graph.get_dimension())
    d, pi = bellman_split(graph, tsp_tour)
    routes, cost = extract(graph.get_dimension(), d, pi, tsp_tour)
    return routes, cost


    