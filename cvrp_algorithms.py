# coding: utf-8

import time
from parser import parse_cvrp
import numpy as np


def clarke_wright_cvrp(map):
    savings = []
    routes = []
    dimension = map.get_dimension()
    savings = []
    for i in range(dimension):
        for j in range(i+1, dimension):

            payload = map.get_value(i, 0) + \
                      map.get_value(0, j) - \
                      map.get_value(i, j)
            savings.append((float(payload), i, j))
    savings.sort(key=lambda x: x[0])
    for x in range(1, dimension):
        routes.append([0, x, 0])
    for saving in savings:
        i = saving[1]
        j = saving[2]
        route_1 = None
        route_2 = None
        for k in range(len(routes)):  # forse meglio un while ?
            if i == routes[k][1]:
                route_1 = routes[k]
            if j == routes[k][len(routes[k])-2]:
                route_2 = routes[k]
                cost = 0
                for u in range(len(route_2)-1):
                    cost += map.get_value(route_2[u], route_2[u+1])
                    print cost
            if route_1 is not None and route_2 is not None and \
               route_1 != route_2:
                new_route = np.append(np.delete(route_1, len(route_1)-1),
                                      np.delete(route_2, 0))
                if (len(route_1)-2) + (len(route_2)-2) <= map.get_capacity():
                    routes.remove(route_1)
                    routes.remove(route_2)
                    routes.append(list(new_route))
                    # update saving
                    savings.remove(saving)
                    savings.append((float(cost + map.get_value(i, 0)
                                    - map.get_value(i, j)), i, j))
                    savings.sort(key=lambda x: x[0])
                    break
    print routes
    tot_cost = 0
    for route in routes:
        for u in range(len(route)-1):
            tot_cost += map.get_value(route[u], route[u+1])
    print tot_cost

map = parse_cvrp('cvrp/bays-n29-k5.vrp')
clarke_wright_cvrp(map)