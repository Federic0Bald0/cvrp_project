# coding: utf-8
import os
import numpy as np
from math import acos, cos, sqrt, pi
from Graph import Graph
from collections import deque


def parse_cvrp(path):

    with open(path, 'r') as f:
        return build_graph(f)


def build_graph(tspfile):

    g = Graph()

    for line in tspfile:
        words = deque(line.split())
        keyword = words.popleft().strip(": ")
        if keyword == "NAME":
            g.set_name(" ".join(words).strip(": "))
        if keyword == "CAPACITY":
            g.set_capacity(int(" ".join(words).strip(": ")))
        if keyword == "TYPE":
            if "CVRP" != " ".join(words).strip(": "):
                print "Format error"
                return
        if keyword == "DIMENSION":
            dimension = int(" ".join(words).strip(": "))
            g.set_dimension(dimension)
        if keyword == "EDGE_WEIGHT_TYPE":
            w_type = " ".join(words).strip(": ")
        if keyword == "EDGE_WEIGHT_FORMAT":
            w_format = " ".join(words).strip(": ")
        if keyword == "NODE_COORD_TYPE":
            n_c_type = " ".join(words).strip(": ")
        if keyword == "NODE_COORD_SECTION":
            if w_type == "EUC_2D":
                parse_euc2d(g, tspfile)
            if w_type == "GEO":
                parse_geo(g, tspfile)
        if keyword == "EDGE_WEIGHT_SECTION":
            if w_type == "EXPLICIT":
                parse_w_matrix(g, w_format, tspfile)
        if keyword == "EOF":
            break
    return g


def parse_euc2d(graph, tspfile):

    dimension = graph.get_dimension()
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
    # creating vertex
    for i in range(dimension):
        p = temp_vertex[i]
        for j in range(dimension):
            if i != j:
                q = temp_vertex[j]
                dist = sqrt(((p[0] - q[0])**2) + (p[1] - q[1])**2)
                graph.add_edge(i, j, dist)


def parse_w_matrix(graph, format, tspfile):

    dimension = graph.get_dimension()
    matrix_temp = []
    for line in tspfile:
        words = deque(line.split())
        keyword = words.popleft().strip(": ")
        if keyword == "DEMAND_SECTION" or \
           keyword == "DISPLAY_DATA_SECTION":
            break
        row = [float(el) for el in line.split()]
        matrix_temp += row
    matrix_temp = np.array(matrix_temp)
    matrix = np.zeros((dimension, dimension))
    if format == "FULL_MATRIX":
        matrix = matrix_temp.reshape((dimension, dimension))

    elif format == "LOWER_DIAG_ROW":
        indices = np.tril_indices(dimension)
        matrix[indices] = matrix_temp

    elif format == "UPPER_ROW":
        indices = np.triu_indices(dimension, 1)
        matrix[indices] = matrix_temp

    for i in range(dimension):
            for j in range(dimension):
                graph.add_edge(i, j, float(matrix[i][j]))


def parse_geo(graph, tspfile):

    dimension = graph.get_dimension()
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
    # creating vertex
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
            graph.add_edge(i, j, dij)


# if __name__ == "__main__":

#     files = os.listdir('./cvrp')
#     for f in files:
#         print f
#         parse_cvrp("./cvrp/" + f)