from flask import Flask
import os 


app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'app/static/upload'
from app import routes
