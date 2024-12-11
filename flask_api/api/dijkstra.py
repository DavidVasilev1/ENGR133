# import the heap library to use a heap in sorting the order in which the path is found (processing efficiency)
import heapq

# main dijkstra algorithm taking in the graph, the start and end to find the shortest path
def dijkstra(graph, start_id, end_id):
    # for each node in the graph
    for node in graph.nodes.values():
        # set the distance as infinite
        node.distance = float('inf')
        # set the previous node as none
        node.previous = None

    # set the start node as the node with the start id requested
    start_node = graph.nodes[start_id]
    # set the start node distance as 0
    start_node.distance = 0
    
    # initialize the priority queue as a list of tuples (each has a distance and a relative node id, in this case the start node)
    # helps put the lower distances in priority to make sure that they are calculated in order of highest efficiency
    # this essentially is how we document each separate path and get which one is the shortest distance
    priority_queue = [(0, start_node.id)]

    # process the nodes in the order until the queue is empty or until it is reached the target node
    while priority_queue:
        # pop the node with the smallest distance and get the current id that it is on
        current_distance, current_node_id = heapq.heappop(priority_queue)
        # get the current node id from the current node object
        current_node = graph.nodes[current_node_id]

        # if the current node id is equal to the end id, then end the loop
        if current_node_id == end_id:
            break

        # if the current distance is greater than a distance that is already found
        if current_distance > current_node.distance:
            # skip processing this path and this node
            continue
        
        # for each of the neighbors in the current node object
        for neighbor in current_node.get_neighbors():
            # get the weight between each of the neighbors
            weight = current_node.get_weight(neighbor)
            # if the weight is equal to 10000
            if weight == 10000:
                # skip processing
                continue
            
            # set the distance of this path to the current distance plus the weight of the new segment of the possible path
            distance = current_distance + weight
            
            # if the distance is smaller than the distance of the neighbor
            if distance < neighbor.distance:
                # set the neighbor distance to the current distance
                neighbor.distance = distance
                # update the previous neighbor to the current node, using this later to reconstruct the path
                neighbor.previous = current_node
                # push the neighbor to the priority queue with the updated distance
                heapq.heappush(priority_queue, (distance, neighbor.id))

    # initialize the path array
    path = []
    # set the current node to the end node
    current_node = graph.nodes[end_id]
    
    # while we are on the current node, follow from the end node to the start node 
    while current_node:
        # append the current node id + 1 for proper id display to the path array
        path.append(current_node.id + 1)
        # set the current node to the previous node in the queue
        current_node = current_node.previous

    # reverse the path
    path.reverse()
    # return the distances for each node in the path as well as the path itself
    return {node.id + 1: node.distance for node in graph.nodes.values()}, path