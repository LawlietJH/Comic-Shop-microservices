from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask
import hashlib

load_dotenv()

def createApp():
    
    app = Flask(__name__)
    CORS(app)

    return app
