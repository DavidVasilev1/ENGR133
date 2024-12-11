# this is the node class, for there to be multiple instances of the nodes
class Node:
    # this function initializes what a node is, with it's id and distance attached to it
    def __init__(self, id, distance=float('inf')):
        # the id is set here for the instance of a node
        self.id = id
        # the distance is set to infinite for each instance initially
        self.distance = distance
        # a dictionary is created for the adjacent node instances to be added
        self.adjacents = {}

    # this function adds the neighbors to the nodes, with the weight being set to 0 initially
    def add_neighbor(self, neighbor, weight=0):
        # adjusting the instance's weight between the node and it's neighbor
        self.adjacents[neighbor] = weight

    # this gets the neighbors
    def get_neighbors(self):
        # this returns the keys of all the neighbors attached to the node
        return self.adjacents.keys()

    # get the weight of a node and it's neighbor
    def get_weight(self, neighbor):
        return self.adjacents[neighbor]