# coding: utf-8

import numpy as np

class Graph:

    def __init__(self):
        self.name = None
        self.dimension = 0
        self.adj_matrix = None
        self.capacity = None # represents the loading capacity in cvpr

    def set_capacity(self, capacity):
        self.capacity = capacity

    def get_capacity(self):
        return self.capacity

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_dimension(self, dimension):
        self.dimension = dimension
        self.adj_matrix = np.zeros(shape=(self.dimension, self.dimension))

    def get_dimension(self):
        return self.dimension
            
    def add_edge(self, vertex_from, vertex_to, weight):
        self.adj_matrix[vertex_from][vertex_to] = weight
        self.adj_matrix[vertex_to][vertex_from] = weight
                
   
                        


