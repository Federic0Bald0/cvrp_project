# coding: utf-8
from __future__ import division


import time
import math
import random
import numpy as np
from parser import parse_cvrp


def clarke_wright_cvrp(map):
    savings = []
    routes = []
    dimension = map.get_dimension()
    # compute savings
    for i in range(1, dimension):
        for j in range(i+1, dimension):
            payload = map.get_value(i, 0) + \
                      map.get_value(0, j) - \
                      map.get_value(i, j)
            savings.append((float(payload), i, j))
    # sort saving in descending order
    savings.sort(key=lambda x: x[0], reverse=True)
    # initialize routes
    for x in range(1, dimension):
        routes.append([0, x, 0])
    # build new routes
    for saving in savings:
        i = saving[1]
        j = saving[2]
        route_1 = None
        route_2 = None
        for k in range(len(routes)):
            # route (0, i, ...)
            if i == routes[k][1]:
                route_1 = routes[k]
            # route (..., j, 0)
            if j == routes[k][len(routes[k])-2]:
                route_2 = routes[k]
            # if the selected ruote are valid for the merge
            if route_1 is not None and route_2 is not None and route_1 != route_2 and \
               (len(route_1)-2) + (len(route_2)-2) <= map.get_capacity():
                    new_route = np.append(np.delete(route_1, len(route_1)-1),
                                          np.delete(route_2, 0))
                    cost_new_route = sum([map.get_value(new_route[u], new_route[u+1])
                                          for u in range(1, len(new_route)-2)])
                    routes.remove(route_1)
                    routes.remove(route_2)
                    routes.append(list(new_route))
                    # update saving
                    savings.remove(saving)
                    savings.append((float(map.get_value(i, 0) +
                                          map.get_value(0, j) -
                                          cost_new_route), i, j))
                    savings.sort(key=lambda x: x[0], reverse=True)
                    break
    tot_cost = 0
    for route in routes:
        for i in range(len(route)-1):
            tot_cost += map.get_value(route[i], route[i+1])
    return routes, tot_cost


# def fisher_jaicumar(map):
#     dimension = map.get_dimension()
#     capacity = map.get_capacity()
#     k = int(math.ceil(dimension / capacity))
#     centroids = []
#     # choose random centers for clusters
#     for i in range(k):
#         # 1 is not included since is the depot
#         centroid = random.randint(2, dimension)
#         centroids.append(centroid)
#     clusters = {}
#     # init clusters
#     for centroid in centroids:
#         clusters[str(centroid)] = [centroid]
#     # compute distances between vertex and depot
#     distances = np.zeros(shape=(k, dimension-1))
#     for centroid in centroids:
#         for i in range(1, dimension-1):
#             if i != centroid:
#                 distance = (map.get_value(0, i) +
#                             map.get_value(i, centroid) +
#                             map.get_value(centroid, 0)) - \
#                             (map.get_value(0, centroid) +
#                             map.get_value(centroid, 0))
#                 j = centroids.index(centroid)
#                 distances[j][i] = distance
#     for i in range(len(centroids)):
#         for centroid in centroids:
#             distances[i][centroid] = -1

#     print distances
#     clusters = generalize_assignment(map, clusters, centroids, distances)
#     print clusters
#     routes = []
#     # tsp for each cluster
#     for centroid in centroids:
#         routes += held_karp(map, clusters[str(centroid)])
#     return routes


# def held_karp(map, cluster):
#     hk_visit(map, 1, cluster)


# def hk_visit(map, s, vertex):
#     if len(vertex) == 1 and vertex[0] == s:
#         return map.get_value(1, s), [(0, s)]
#     else:
#         mindist = -1 # infinite
#         route = [] # useless
#         for v in vertex:
#             dist, temp_route = hk_visit(map, v, vertex.remove(v))
#             if dist + map.get_value(s, v):
#                 mindist = dist + map.get_value(s, v)
#                 route += temp_route
#         return mindist, route


# def knapsak0_1(distances, cluster, capacity, centroids):
#     for i in range(len(centroids)):
#         centroid = centroids[i]
#         for j in range(len(distances[0])):
#             if len(cluster) < capacity:
#                 min_dist = min_not_neg(distances[i])
#                 vertex = list(np.where(distances[i]==min_dist))[0]
#                 print min_dist, vertex
#                 cluster.append(vertex[0])
#                 # this vertex is assigned, hence it
#                 # can not be use again
#                 for k in range(len(centroids)):
#                     distances[k][vertex] = -1
#             else:
#                 break
#     return cluster, distances


# def generalize_assignment(map, clusters, centroids, distances):
#     for centroid in centroids:
#         clusters[str(centroid)], distances = knapsak0_1(distances, clusters[str(centroid)], map.get_capacity(), centroids)
#         print distances
#     return clusters


# def min_not_neg(l):
#     ris = None
#     for i in range(len(l)):
#         if (ris == None or l[i] < ris) and (l[i] != -1):
#             ris = l[i]
#     return ris

# we choose the minimum distance and we assign it to the corresponding
# cluster if its capacity it is not reached
# def generalize_assignment(map, distances, centroids, clusters):
#     dimension = map.get_dimension()
#     k = len(centroids) * dimension
#     # max_temp = 0
#     # for i in range(len(centroids)-1):
#     #         for j in range(dimension-1):
#     #             if max_temp < distances[i][j]:
#     #                     max_temp = distances[i][j]
#     while k != 0:
#         i_temp = 1
#         j_temp = 1
#         min_temp = distances[i_temp][j_temp]
#         for i in range(len(centroids)-1):
#             for j in range(dimension-1):
#                 if distances[i][j] != -1:
#                     if min_temp > distances[i][j]:
#                         min_temp = distances[i][j]
#                         i_temp = i
#                         j_temp = j
#         distances[i_temp][j_temp] = -1
#         while len(clusters[str(centroids[i_temp])]) > map.get_capacity():
#             temp = distances[:, j_temp]
#             k = 0
#             while k == i_temp and k < len(centroids):
#                 k += 1
#             min_temp =
#             for j in range(len(centroids)):
#                 if distances[i][j] != -1:
#                     if min_temp > distances[i_temp][j]:
#                         min_temp = distances[i_temp][j]
#                         j_temp = j
#         if j_temp != -1 and not j_temp in clusters[str(centroids[i_temp])] :
#             clusters[str(centroids[i_temp])].append(j_temp)
#         k = k - 1
#     print clusters
#     return clusters

# def held_karp(map):
#     S = set[range(map.get_dimension())]
#     d, pi = hk_visit(map, 0, S)


# def hk_visit(map, v, S, d, pi):
#     l = []
#     if len(S) == 1 and S[0] == v:
#         l.append([v, S, map.get_value(0, v), 0))
#         return l
#     else:
#         l_S = [u if u[1] == S u in l]
#         for u in l_S:
#             if u[2] is None:
#                 mindist = None
#                 minprec = None
#                 for w in S.remove(v):
#                     l_S = hk_visit(w, S)
#                     if (cost_path(w, l_S, S) + map.get_value(u, v) < mindist or
#                             mindist is None):
#                                 mindist = cost_path(w, l_S, S) + map.get_value(u, v)
#                                 minprec = u
#                     d[v, ]
#         return l

# def cost_path(w, l_S, s):
#     cost = 0
#     for i in range(len(S)-1):
#         cost += d[pi[i]][p[i+1]]
#     return cost



map = parse_cvrp('cvrp/bays-n29-k5.vrp')
clarke_wright_cvrp(map)

def held_karp(map):
    dimension = map.get_dimension()
    n = (dimension * dimension)/2 - dimension
    # Maps each subset of the nodes to the cost to reach that subset, as well
    # as what node it passed before reaching this subset.
    # Node subsets are represented as set bits.
    C = {}
    # Set transition cost from initial state
    for k in range(1, n):
        C[(1 << k, k)] = (map.get_value(0, k), 0)

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
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    # We're interested in all bits but the least significant (the start state)
    bits = (2**n - 1) - 1

    # Calculate optimal cost
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
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