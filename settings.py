from flask import Flask
app = Flask(__name__)
import os

file_path = os.path.abspath(os.getcwd())+"\database.db"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
