# import sqlalchemy library for sqlite database
from sqlalchemy import Column, Integer, String
# import the database to the file
from .. import db
# import the json library for web requests
import json

# create a new class, using a database mode for every new instance of this class
class NodeMap(db.Model):
    # this names the table
    __tablename__ = "nodeMaps"
    # this is used for the id column in the table, making this column be used as the primary key for searches
    id = Column(Integer, primary_key=True)
    # this is the column used for the map name
    _mapName = Column(String, primary_key=False)
    # this defines the node map column, which stores the maps for the graphs
    _nodeMap = Column(String)

    # initialize each instance of the entries in the tables
    def __init__(self, mapName, nodeMap):
        # this creates instances of the map names and the node maps
        self._mapName = mapName
        # creates a json dump to create an object into a json string
        self._nodeMap = json.dumps(nodeMap)

    # creates each instance into a dictionary usually used for loading the data
    def to_dict(self):
        # returns a dictionary of the data in the table
        return {"id": self.id, "nodeMap": json.loads(self._nodeMap)}
