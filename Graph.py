# coding: utf-8

import numpy as np


# -----------------------------------------------------------------------------
# the graph is implemented keeping using adjacency matrix
# Since the cases considered are complete graphs the adjancency
# matrix was used for efficiency reasons
class Graph:
    """
    set_capacity: initialize capacity limit of the graph

    set_dimension: initialize the dimension of the graph

    get_capacity: returns capacity limit of the graph

    get_dimension: returns dimension of the graph

    set_demand: initialize the demand vector

    get_demand: returns the demand of a vertex

    get_distance: returns the distance between two nodes

    add_edge: assign an edge in the adj_matrix with its weight
              ,meaning the distance between two nodes. Since 
              the case we will consider are complete graph this 
              is a simmetric matrix
    """
    #-----------------------------------------------------------#
    # In order to use properly the graph at least the dimension #
    # must be set                                               #
    #-----------------------------------------------------------#
    def __init__(self):
        # self.name = None
        self.dimension = 0
        # self.adj_list = None
        self.demands = None
        self.adj_matrix = None
        self.capacity = None  # represents the loading capacity in cvpr

    def set_capacity(self, capacity):
        self.capacity = capacity

    def get_capacity(self):
        return self.capacity

    # def set_name(self, name):
    #     self.name = name

    # def get_name(self):
    #     return self.name

    def get_distance(self, i, j):  
        return self.adj_matrix[i][j]

    def set_dimension(self, dimension):
        self.dimension = dimension
        # self.adj_list = [[]] * dimension
        self.adj_matrix = np.zeros(shape=(self.dimension, self.dimension))

    def set_demand(self, demands):
        self.demands = demands
    
    def get_demand(self, i):
        return self.demands[i]

    def get_dimension(self):
        return self.dimension

    def add_edge(self, vertex_from, vertex_to, weight):
        # self.adj_list[vertex_from].append((vertex_to, weight))
        # self.adj_list[vertex_to].append((vertex_from, weight))
        self.adj_matrix[vertex_from][vertex_to] = weight
        self.adj_matrix[vertex_to][vertex_from] = weight

    # def get_neighbours(self, vertex):
    #     return self.adj_list[vertex]

    # def get_weight(self, vertex_from, vertex_to):
    #     weight = None
    #     for u in self.adj_list[vertex_from]:
    #         if u[0] == vertex_to:
    #             weight = u[1]
    #     return weight




