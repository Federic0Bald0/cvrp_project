# coding: utf-8

class Vertex:

    def __init__(self, vertex, capacity):
        self.name = vertex
        self.neighbors = [] # represents edges
        self.capacity = capacity # represents the loading capacity in cvpr
        
    def add_neighbor(self, neighbor, weight):
        if isinstance(neighbor, Vertex):
            # since this is an undirected graph, if one neighbor is in the
            # neighbor list the current node must be in neighbor neighbors list 
            for vertex in self.neighbors:
                if vertex[0] == neighbor.name: # vertex already in the adj list
                    return 
            self.neighbors.append([neighbor.name, weight])
            neighbor.neighbors.append([self.name, weight])
            self.neighbors = sorted(self.neighbors)
            neighbor.neighbors = sorted(neighbor.neighbors)
        else:
            return False
        
    def add_neighbors(self, neighbors):
        for neighbor in neighbors:
            self.add_neighbor(neighbor[0], neighbor[1])
            # neighbor[1] = weight 
        
    def __repr__(self):
        return str(self.neighbors)


class Graph:

    def __init__(self):
        self.vertices = {}
    
    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex):
            self.vertices[vertex.name] = vertex.neighbors
 
    def add_vertices(self, vertices):
        for vertex in vertices:
            if isinstance(vertex, Vertex):
                self.vertices[vertex.name] = vertex.neighbors
            
    def add_edge(self, vertex_from, vertex_to, weight):
        if isinstance(vertex_from, Vertex) and isinstance(vertex_to, Vertex):
            vertex_from.add_neighbor(vertex_to, weight)
            vertex_to.add_neighbor(vertex_from, weight)
            self.vertices[vertex_from.name] = vertex_from.neighbors
            self.vertices[vertex_to.name] = vertex_to.neighbors
                
    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge[0],edge[1], edge[2])        
            # edge[1] = weight   
    
    def adjacencyList(self):
        if len(self.vertices) >= 1:
            return [str(key) + ":" + str(self.vertices[key]) for key in self.vertices.keys()]  
        else:
            return dict()
        
#     def adjacencyMatrix(self):
#         if len(self.vertices) >= 1:
#             vertices = sorted(g.vertices)
#             self.vertex_names = [vertex[0] for vertex in vertices]
#             self.vertex_indices = dict(zip(self.vertex_names, range(len(self.vertex_names)))) 
#             print self.vertex_indices
#             import numpy as np
#             self.adjacency_matrix = np.zeros(shape=(len(self.vertices),len(self.vertices)))
#             for i in range(len(self.vertex_names)):
#                 for j in range(i, len(self.vertices)):
#                     for el in g.vertices[self.vertex_names[i]]:
#                         print el[0]
#                         j = g.vertex_indices[el[0]]
#                         print vertices[j]
#                         self.adjacency_matrix[i,j] = vertices[j][1]
#             return self.adjacency_matrix
#         else:
#             return dict()              
                        
def graph(g):
    """ Function to print a graph as adjacency list and adjacency matrix. """
    return str(g.adjacencyList()) # + '\n') + '\n' + str(g.adjacencyMatrix())

###################################################################################

a = Vertex('A', 2)
b = Vertex('B', 3)
# c = Vertex('C', 4)
# d = Vertex('D', 5)
# e = Vertex('E', 6)

a.add_neighbors([[b,7]]) 
b.add_neighbors([[a,8]])
# c.add_neighbors([b,d,a,e])
# d.add_neighbor(c)
# e.add_neighbors([a,c])
        
g = Graph()
# print graph(g)
# print 
g.add_vertices([a,b])
# # g.add_edge(b,d)
print graph(g)