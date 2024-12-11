# import flask libraries
from flask import Flask
from flask_cors import CORS
from flask_api import app, db
# import the dijkstra api to run it when the program runs
from flask_api.api.dijkstra_api import api_bp

# set the blueprint of the api endpoints
app.register_blueprint(api_bp, url_prefix='/api')

# main function running the app
def main():
    # create the flask application
    with app.app_context():
        # create all databases
        db.create_all()
    # open port 8199 and run the app
    app.run(debug=True, host="0.0.0.0", port="8199")

# run the main function
if __name__ == "__main__":
    # start corse on the app
    cors = CORS(app)
    # run the main function
    main()
