# coding: utf-8

import os
from parser import parse_cvrp
from cvrp_algorithms import clark_wright_cvrp

if __name__ == "__main__":

    files = os.listdir('./cvrp')
    for f in files:
        print f
        g = parse_cvrp("./cvrp/" + f)
        print g.adj_matrix
        clark_wright_cvrp(g)