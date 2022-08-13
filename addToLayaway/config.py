from flask.json import JSONEncoder
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, Blueprint
from bson import json_util, ObjectId
import os

class MongoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)

load_dotenv()

def createApp():

    app = Flask(__name__)
    CORS(app)
    app.json_encoder = MongoJSONEncoder
    
    username = os.getenv('MONGODB_USERNAME')
    password = os.getenv('MONGODB_PASSWORD')
    hostname = os.getenv('MONGODB_HOSTNAME')
    app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@{hostname}/?retryWrites=true&w=majority"

    return app
