# coding: utf-8

import time 
import numpy
import os
from parser import parse_cvrp, parse_demand
from cvrp import clark_wright, route_first_cluster_second


if __name__ == "__main__":

    # optimal cost of the solution for istance
    cost = {
        'F-n135-k7.vrp': 1162,
        'F-n72-k4.vrp': 237, 
        'gr-n17-k3.vrp': 2685, 
        'gr-n21-k3.vrp': 3704,
        'hk-n48-k4.vrp': 14749,
        'gr-n48-k3.vrp': 5985,
        'att-n48-k4.vrp': 40002,
        'fri-n26-k3.vrp': 1353, 
        'bayg-n29-k4.vrp': 2050, 
        'ulysses-n16-k3.vrp': 30492,
        'F-n45-k4.vrp': 724,
        'ulysses-n22-k4.vrp': 40153,
        'gr-n24-k4.vrp': 2053,
        'swiss-n42-k5.vrp': 1668,
        'dantzig-n42-k4.vrp': 1142,
        'bays-n29-k5.vrp': 2963
    }
    # applies the two algorithm to each instance in the cvrp folder
    files = os.listdir('./cvrp')
    for f in files:
        print f
        g = parse_cvrp("./cvrp/" + f)
        g = parse_demand(g, "./cvrp/" + f)
        t0 = time.time() % 60
        routes, cost_app = clark_wright(g)
        t1 = time.time() % 60
        print routes, cost_app
        print (cost_app - cost[str(f)])/cost[str(f)]
        print t1 - t0
        t0 = time.time() % 60
        routes, cost_app = route_first_cluster_second(g)
        t1 = time.time() % 60
        print routes, cost_app
        print (cost_app - cost[str(f)])/cost[str(f)]
        print t1 - t0