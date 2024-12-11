# import flask library for data management
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# defines the flask app that is going to run
app = Flask(__name__)
# defines what the database will be
dbURI = "sqlite:///sqlite.db"
# do not track modifications
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# setting the database uri
app.config["SQLALCHEMY_DATABASE_URI"] = dbURI
# only used for dotenv in case we need secure communication
app.config["SECRET_KEY"] = "SECRET_KEY"
# sets the database of the app
db = SQLAlchemy(app)
# binding the database with the app
Migrate(app, db)

# set specifications for storing images
# setting the max size of images
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
# setting specific types of images
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".gif"]
# setting image storage locations
app.config["UPLOAD_FOLDER"] = "volumes/uploads/"
