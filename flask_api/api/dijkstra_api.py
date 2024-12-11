# importing flask libraries
from flask import Blueprint, request, jsonify
from flask_cors import CORS
# importing files like classes and functions
from flask_api.model.weighted_graph import WeightedGraph
from flask_api.api.dijkstra import dijkstra
# importing the database file
from .. import db
# importing the node maps class
from ..model.nodeMaps import NodeMap

# creating a blueprint 
api_bp = Blueprint('api', __name__)
# setting cors exceptions for accessing these endpoints, making requests not give cors error
CORS(api_bp, resources={r"/dijkstra": {"origins": "http://127.0.0.1:4000"}})
CORS(api_bp, resources={r"/map": {"origins": "http://127.0.0.1:4000"}})

# initializing weighted graph class, creating an instance
graph = WeightedGraph()

# endpoint for the dijkstra algorithm calculation to find the shortest path
# this is a post method, because the data is posted to this endpoint
@api_bp.route("/dijkstra", methods=["POST"])
# defining the function complete this request
def run_dijkstra():
    # setting the data that is part of the request as the json of that data
    data = request.json
    # initializing the individual data variables which are used in the calculation from the data received from the JSON request
    adj_list = data.get("adjacencyList")
    start_id = data.get("source")
    end_id = data.get("target")

    # if the data is empty, then return a 400 error
    if adj_list is None or start_id is None or end_id is None:
        return jsonify({"error": "Invalid input data"}), 400

    # setting the start and end indices as -1
    start_id -= 1
    end_id -= 1

    # clearing all nodes from the graph
    graph.nodes.clear()

    # iterate through each of the neighbors on the start node in the adj list
    for from_node, neighbors in enumerate(adj_list):
        # add the start node ot the graph as a node
        graph.add_node(from_node)
        # for each of the destination nodes and the weights between the start node and end node
        for to_node, weight in enumerate(neighbors):
            # if the edge weight between the nodes is not 0 or 10000
            if weight != 0 and weight != 10000:
                # add the edge to the graph as a start node, end node, and the weight between the two nodes
                graph.add_edge(from_node, to_node, weight)

    # id the start id or end id is not in the nodes on the graph
    if start_id not in graph.nodes or end_id not in graph.nodes:
        # return a 400 error that the node set as a start or end is not valid, 404 error meaning that it is a user error
        return jsonify({"error": "Invalid start or end node"}), 404

    # try to compute the shortest path
    try:
        # set the distances and the path calculated using the dijkstra function which inputs the graph, start and end id
        distances, path = dijkstra(graph, start_id, end_id)
        # print the distances for debugging in console
        print(distances)
        # return a json response of the path that is found
        return jsonify(path)
    # for errors with the server
    except Exception as e:
        # returns a internal server error if there is an error with the calculation
        return jsonify({"error": str(e)}), 500

# this route is used to post a map to the SQLite database using a post
@api_bp.route("/map", methods=["POST"])
# this is the function used to save a map to the database
def save_map():
    # the data is retrieved from the json
    data = request.json

    # if the data does not contain map or mapName
    if "map" not in data or "mapName" not in data:
        # return 400 user error on the data not containing those elements
        return jsonify({"message": "Missing 'map' or 'mapName' key in request data."}), 400

    # retrieve data from the data
    map_name = data["mapName"]
    node_map_value = data["map"]

    # create a node map which holds the map name and the actual map data
    node_map = NodeMap(map_name, node_map_value)

    # attempt to store data into the database
    try:
        # create a database session to add the node map into the database
        db.session.add(node_map)
        # commit the changes to the database
        db.session.commit()
        # send back a 201 response to show that the data is correct and processed right
        return jsonify(node_map.to_dict()), 201
    # checking for server errors
    except Exception as e:
        # undo changes to the database to previous version before operation
        db.session.rollback()
        # print that there was an error saving the map
        print(f"Error saving NodeMap: {e}")
        # return a 500 to the frontend to show internal server error
        return jsonify({"message": f"server error: {str(e)}"}), 500

# route to get all the maps from the database using the get request
@api_bp.route("/getMaps", methods=["GET"])
# function to handle this retrieval
def get_maps():
    # attempt to look through the database
    try:
        # set nodeMaps variable to be all node map objects found in the query of the database session
        nodeMaps = db.session.query(NodeMap).all()
        
        # create a list of all the node maps found
        nodeMaps_list = [
            # set this format for the JSON to be returned
            {
                # data contains the id, map name, and the node map data
                "id": node_map.id,
                "mapName": node_map._mapName,
                "nodeMap": node_map._nodeMap 
            }
            # do this for every map in the list of maps
            for node_map in nodeMaps
        ]
        
        # return a 200 successful query and return the data to the frontend
        return jsonify(nodeMaps_list), 200
    # check for internal server errors like the database missing the data
    except Exception as e:
        # error in getting the data
        print(f"Error retrieving NodeMaps: {e}")
        # return json as a 500 error as an internal server error
        return jsonify({"message": f"server error: {str(e)}"}), 500

# this route is used to find a specific map id and delete it from the database, as shown by the endpoint in which you request the id number
@api_bp.route("/deleteMap/<int:map_id>", methods=["DELETE"])
# this function receives the map id and deletes the map from the database
def delete_map(map_id):
    # try to delete the data
    try:
        # find the node map data using a filter to look for the map if in the database
        node_map = db.session.query(NodeMap).filter(NodeMap.id == map_id).first()
        
        # if the node map does not exist, return that the map is not found
        if node_map is None:
            # return 404 error to the frontend
            return jsonify({"message": "Map not found."}), 404
        
        # open a session for the database and delete the found node map
        db.session.delete(node_map)
        # commit the changes to the database
        db.session.commit()
        # return a successful deletion from the database as a 200
        return jsonify({"message": "Map deleted successfully."}), 200
    # look for errors in deleting the node map
    except Exception as e:
        # undo the changes that have been done to the database
        db.session.rollback()
        # log the error
        print(f"Error deleting NodeMap: {e}")
        # return a 500 internal server error to the frontend
        return jsonify({"message": f"server error: {str(e)}"}), 500