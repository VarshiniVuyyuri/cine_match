import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import json
import random

# --- App & Database Configuration ---

app = Flask(__name__)
# Get the absolute path of the directory where the script is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cinematch.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_super_secret_key'  # Needed for flash messages

db = SQLAlchemy(app)