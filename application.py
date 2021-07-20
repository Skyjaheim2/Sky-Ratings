import os
import requests
import hashlib
import smtplib
import json
from email.message import EmailMessage

from flask import Flask, session, render_template, request, redirect, jsonify
from functools import wraps
from dotenv import load_dotenv
from flask_session import Session
from sqlalchemy import and_
from models import *

import datetime
from datetime import date, timedelta, tzinfo, datetime
from pytz import timezone
from math import inf



# Check for environment variables
# load_dotenv()
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")
#
# if not os.getenv("EMAIL_ADDRESS"):
#     raise RuntimeError("EMAIL_ADDRESS is not set")
#
# if not os.getenv("EMAIL_PASSWORD"):
#     raise RuntimeError("EMAIL_PASSWORD is not set")
#
# # EMAIL
# EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = Flask(__name__)
app.config['TESTING'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SESSION_PERMANENT'] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
# The maximum number of items the session stores
# before it starts deleting some, default 500
app.config['SESSION_FILE_THRESHOLD'] = 500
db.init_app(app)

# ENABLE SESSION
Session(app)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/loginUser/<string:username>/<string:user_password>", methods=['POST'])
def loginUser(username, user_password):
    print(f"Username: {username}")
    print(f"User password: {user_password}")

    return "Received"

@app.route("/signUpUser/<string:userName>/<string:userEmail>/<string:userPassword>", methods=['POST'])
def signUpUser(userName, userEmail, userPassword):
    print(f"UserName: {userName}")
    print(f"User Password: {userPassword}")
    print(f"User Email: {userEmail}")

    return ""

# C:\Users\jahei\OneDrive\Documents\Hackathon-1