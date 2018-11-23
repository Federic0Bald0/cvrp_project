# coding: utf-8
import os
import numpy as np
from math import acos, cos, sqrt, pi, ceil
from Graph import Graph
from collections import deque


def parse_demand(graph, path):
    with open(path, 'r') as f:
        for line in f:
            words = line.split()
            if words[0] == "DEMAND_SECTION":
                demands = build_demand(f, graph.get_dimension())
                graph.set_demand(demands)
            if words[0] == "EOF":  
                return graph
            
def build_demand(tspfile, dimension):
    demands = [0] * dimension
    for i, line in enumerate(tspfile):
        demand = line.split()
        if i < dimension:  
            demands[int(demand[0])-1] = int(demand[1])
        else:
            return demands



def parse_cvrp(path):

    with open(path, 'r') as f:
        return build_graph(f)


def build_graph(tspfile):
    # build the graph that will be used by the cvrp algorithms
    graph = Graph()
    # -------------------------------------------------------------------------
    # parse the vrp file
    for line in tspfile:
        words = deque(line.split())
        keyword = words.popleft().strip(": ")
        # if keyword == "NAME":
        #     g.set_name(" ".join(words).strip(": "))
        if keyword == "CAPACITY":
            graph.set_capacity(int(" ".join(words).strip(": ")))
        if keyword == "TYPE":
            if "CVRP" != " ".join(words).strip(": "):
                print "Format error"
                return
        if keyword == "DIMENSION":
            dimension = int(" ".join(words).strip(": "))
            graph.set_dimension(dimension)
        if keyword == "EDGE_WEIGHT_TYPE":
            w_type = " ".join(words).strip(": ")
        if keyword == "EDGE_WEIGHT_FORMAT":
            w_format = " ".join(words).strip(": ")
        if keyword == "NODE_COORD_TYPE":
            n_c_type = " ".join(words).strip(": ")
        if keyword == "NODE_COORD_SECTION":
            if w_type == "EUC_2D":
                dist_matrix =parse_euc2d(dimension, graph, tspfile)
            if w_type == "GEO":
                dist_matrix = parse_geo(dimension, graph, tspfile)
        if keyword == "EDGE_WEIGHT_SECTION":
            if w_type == "EXPLICIT":
                dist_matrix = parse_w_matrix(dimension, graph, w_format, tspfile)
        if keyword == "EOF":
            break
    # -------------------------------------------------------------------------
    # building the graph using the distances matrix
    for i in range(dimension):
            for j in range(dimension):
                graph.add_edge(i, j, float(dist_matrix[i][j]))
    return graph


def parse_euc2d(dimension, graph, tspfile):
    # -------------------------------------------------------------------------
    # for each vertex store its value in x and y 
    temp_vertex = [None] * dimension
    i = 1
    for line in tspfile:
        words = deque(line.split())
        vertex_name = words.popleft()
        if vertex_name == str(i):
            x = float(words.popleft())
            y = float(words.popleft())
            temp_vertex[int(vertex_name)-1] = [x, y]
            i += 1
        else:
            break
    # -------------------------------------------------------------------------
    # store in the matrix the distances between nodes
    dist_matrix = np.zeros((dimension, dimension))
    for i in range(dimension):
        p = temp_vertex[i]
        for j in range(dimension):
            if i != j:
                q = temp_vertex[j]
                xd = p[0] - q[0]
                yd = p[1] - q[1]
                dist = ceil(sqrt( xd*xd + yd*yd))
                dist_matrix[i][j] = dist
    return dist_matrix


def parse_w_matrix(dimension, graph, format, tspfile):
    # -------------------------------------------------------------------------
    # build a vectoer considering all elements of the distance matrix, 
    # regardless of the matrix structuture
    vector_temp = []
    for line in tspfile:
        words = deque(line.split())
        keyword = words.popleft().strip(": ")
    # -------------------------------------------------------------------------
    # distance section is finished
        if keyword == "DISPLAY_DATA_SECTION" or keyword == "DEMAND_SECTION":
            break
        vector_temp += [float(el) for el in line.split()]
    dist_matrix = np.zeros((dimension, dimension))
    # -------------------------------------------------------------------------
    # the parsing process is the same for lower triangular matrix of full
    # matrix, while it is different in the case of upper triangular matrix
    if format == "LOWER_DIAG_ROW" or format == "FULL_MATRIX":
        i = 0 
        column = 0
        row = 0
        while i < (dimension*dimension + dimension)/2 -1: 
            dist_matrix[row][column] = vector_temp[i] 
            dist_matrix[column][row] = vector_temp[i]
            if row == column:
                row += 1
                column = 0
            else:
                column += 1
            i += 1
    elif format == "UPPER_ROW":
        row = 0
        column = 0
        diag = 0
        i = 0
        while i < (dimension*dimension - dimension)/2 -1: 
            dist_matrix[row][column] = vector_temp[i] 
            dist_matrix[column][row] = vector_temp[i]
            if column == dimension - 1:
                diag += 1
                column = diag + 1
                row += 1
            else:
                column +=1 
            i += 1
    return dist_matrix
    

def parse_geo(dimension, graph, tspfile):
    # -------------------------------------------------------------------------
    # for each vertex store its value in x and y 
    temp_vertex = [None] * dimension
    i = 1
    for line in tspfile:
        words = deque(line.split())
        vertex_name = words.popleft()
        if vertex_name == str(i):
            x = float(words.popleft())
            y = float(words.popleft())
            temp_vertex[int(vertex_name)-1] = [x, y]
            i += 1
        else:
            break
    # -------------------------------------------------------------------------
    # compute the geographical distances 
    dist_matrix = np.zeros((dimension, dimension))
    for i in range(dimension):
        p = temp_vertex[i]
        deg = int(p[0])
        min = p[0] - deg
        latitude_p = pi * (deg + 0.5 * min / 0.3) / 180.0
        deg = int(p[1])
        min = p[1] - deg
        longitude_p = pi * (deg + 0.5 * min / 0.3) / 180.0
        for j in range(dimension):
            q = temp_vertex[j]
            deg = int(q[0])
            min = q[0] - deg
            latitude_q = pi * (deg + 0.5 * min / 0.3) / 180.0
            deg = int(q[1])
            min = q[1] - deg
            longitude_q = pi * (deg + 0.5 * min / 0.3) / 180.0

            RRR = 6378.388
            q1 = cos(longitude_p - longitude_q)
            q2 = cos(latitude_p - latitude_q)
            q3 = cos(latitude_p + latitude_q)
            dij = int(RRR * acos(0.5 * ((0.1 + q1) * q2 - (1.0 - q1) * q3)) +
                      1.0)
            dist_matrix[i][j] = dij
    return dist_matrix


# if __name__ == "__main__":

#     files = os.listdir('./cvrp')
#     for f in files:
#         g = parse_cvrp("./cvrp/" + f)
#         print g.adj_matrix
#         print parse_demand(g, "./cvrp/" + f).demands
