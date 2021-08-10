import os
import requests
import hashlib
import smtplib
import json
from email.message import EmailMessage
from math import floor

from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session

from functools import wraps
from dotenv import load_dotenv

from sqlalchemy import and_
from models import *

import datetime
from datetime import date, timedelta, tzinfo, datetime
from pytz import timezone
from math import inf

from Methods import convertDateFormats



# Check for environment variables
load_dotenv()
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

if not os.getenv('TMDB_API_KEY'):
    raise RuntimeError("TMDB api key is not set")
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
app.config['SESSION_PERMANENT'] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
# The maximum number of items the session stores
# before it starts deleting some, default 500
app.config['SESSION_FILE_THRESHOLD'] = 500
db.init_app(app)

# ENABLE SESSION
Session(app)

# GET API KEY
TMDB_API_KEY = os.getenv('TMDB_API_KEY')


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/loginUser/<string:userName>/<string:userPassword>", methods=['POST', 'GET'])
def loginUser(userName, userPassword):
    userPassword = hash_password(userPassword)

    checkUser = User.query.filter(and_(User.name == userName, User.password == userPassword)).all()
    if len(checkUser) != 0:
        session['user_id'] = checkUser[0].id
        session['logged_in'] = True
        return "Logged In"
    else:
        if request.method == 'GET':
            return "Signed Up"
        return "Invalid Credentials"

@app.route("/signUpUser/<string:userName>/<string:userEmail>/<string:userPassword>", methods=['POST'])
def signUpUser(userName, userEmail, userPassword):
    userPassword = hash_password(userPassword)

    newUser = User(name=userName, email=userEmail, password=userPassword)

    if newUser.addUser() == -1:
        return "User Already Signed Up"
    else:
        return redirect(f"/loginUser/{userName}/{userPassword}")


@app.route("/movies", methods=['GET'])
def movies():
    return render_template("movies.html")

@app.route("/getTrendingMovies", methods=['GET'])
def getTrendingMovies():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
    response = requests.request("GET", url)
    if response.status_code == 200:
        JSON_DATA = json.loads(response.text)
        return jsonify(JSON_DATA)
    else:
        return "Something went wrong with the url"

@app.route("/getMovies/<string:sort>/<string:numMoviesToGet>", methods=['GET'])
def getMovies(sort, numMoviesToGet):
    """
    Error Codes: -1: Something went wrong with thr url
                 -2: Invalid sort
    """
    if not numMoviesToGet.isdigit():
        return '-3'

    numMoviesToGet = int(numMoviesToGet)
    pageNumber = floor(numMoviesToGet/10)
    if pageNumber == 0:
        pageNumber = 1
    if numMoviesToGet <= 20:
        pageNumber = 1

    # print(pageNumber)
    supportedSorts = ['popular', 'latest', 'top_rated', 'now_playing', 'upcoming']
    if sort not in supportedSorts:
        return '-2'

    url = f"https://api.themoviedb.org/3/movie/{sort}?api_key={TMDB_API_KEY}&page={pageNumber}"
    response = requests.request("GET", url)
    if response.status_code == 200:
        JSON_DATA = json.loads(response.text)
        return jsonify(JSON_DATA)
    else:
        return '-1'




@app.route("/checkIfUserIsStillLoggedIn", methods=['GET'])
def checkIfUserIsStillLoggedIn():
    return json.dumps(True) if 'logged_in' in session else json.dumps(False)

@app.route("/signOut", methods=['POST'])
def signOut():
    session.clear()
    return "Signed Out"


@app.route("/test", methods=['GET'])
def test():
    return render_template('layout.html')

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_password_hash(password, hash):
    if hash_password(password) == hash:
        return True
    return False

# C:\Users\jahei\OneDrive\Documents\Hackathon-1