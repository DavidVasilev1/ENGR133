# import that Node class, used in the graph
from flask_api.model.node import Node

# creating the weighted graph class, which contains all nodes in the map
class WeightedGraph:
    # initialize the class
    def __init__(self):
        # creates a dictionary of all the nodes in the instance of the graph
        self.nodes = {}

    # add nodes by id to the graph
    def add_node(self, id):
        # check to see if the node is assigned an id
        if id not in self.nodes:
            # if the node is not assigned an id, then create a new node object to document the node
            self.nodes[id] = Node(id)

    # add an edge between the nodes with a specific weight
    def add_edge(self, from_node, to_node, weight=1):
        # if the start node is not in the node dictionary
        if from_node not in self.nodes:
            # add a new node which is going to be the start node
            self.add_node(from_node)
        # check to see if the end node is added
        if to_node not in self.nodes:
            # if the new node is not added, then add it to the instance
            self.add_node(to_node)
        # for the start node, add the neighbors as the end nodes and the weight between each end node
        self.nodes[from_node].add_neighbor(self.nodes[to_node], weight)