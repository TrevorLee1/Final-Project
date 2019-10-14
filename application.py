import os

from flask import Flask, session, render_template, url_for, redirect, request, escape
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index(): #Start page, allows for registration and login
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register(): #Registration for users
    error = None #Error message that may or may not be used
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = escape(request.form.get("username")) #Takes user's input and sanitizes input
        password = escape(request.form.get("password"))

        if username == "": #Prevents blank space or NULL usernames
            return render_template("register.html", error="Input a valid username!")

        elif db.execute("SELECT * FROM users WHERE username = :username", {"username":username}).rowcount == 0: #If username not taken
            db.execute("INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)", {"username": username, "password": password, "admin":"FALSE"})
            #Inserts a new un-admined user and their password into the database
            db.commit()
            return redirect(url_for("login")) #redirect to login page

        else: #If username is taken
            return render_template("register.html", error="That username is already taken!")
            #Error message


@app.route("/login", methods=["GET","POST"])
def login(): #Login page
    fail_msg = None

    if request.method == "GET":
        return render_template("login.html")

    else:
        username = escape(request.form.get('username')) #escape() sanitizes input
        password = escape(request.form.get('password'))

        #Check if username exists and corresponding password matches -> login
        if db.execute("SELECT * FROM users WHERE username = :username and password = :password", {"username": username, "password": password}).rowcount == 1:
            session['username'] = username
            #Stores the user's name inside the session, keeps track of who is
            #logged in
            return redirect(url_for("home"))
        else: #If username or password is wrong or does not match
            return render_template("login.html", fail_msg = "Invalid username / password! Please try again!")

@app.route("/home")
def home(): #Home page
    if 'username' not in session:
        return render_template("loginerror.html")
    #Prevents users who have not logged in from accessing page

    return render_template("home.html")

@app.route("/motions_index")
def motions_index(): #For users to browse or look for specific motions
    if 'username' not in session:
        return render_template("loginerror.html")

    return render_template("motions_index.html")

@app.route("/motioninput", methods=["GET","POST"])
def motioninput(): #For admins to add new motions
    fail_msg = None
    if 'username' not in session:
        return render_template("loginerror.html")

    elif 'username' in session:
        username = session['username'] #Determines current user

    motion = escape(request.form.get("motion")).upper()
    #Uppercase to maintain consistency
    type = escape(request.form.get("type"))
    #Type of motion: philosophical, policy or retrospective
    tournament = escape(request.form.get("tournament"))
    #Determines if motion has been featured in a tournament or not

    if request.method == "GET":
        return render_template("motioninput.html")

    elif request.method == "POST": #If users are attempting to edit
        if db.execute("SELECT * FROM users WHERE username = :username and admin = TRUE", {"username": username}).rowcount == 0:
            return render_template("motioninput.html", fail_msg="You do not have admin access!")
        #Prevents non-admins from editing

        if motion == "": #Prevents blank space or NULL motions
            return render_template("motioninput.html", fail_msg="Please input a motion!")

        elif db.execute("SELECT * FROM motions WHERE motion = :motion", {"motion":motion}).rowcount == 0: #If motion does not already exist
            db.execute("INSERT INTO motions (motion, type, tournament) VALUES (:motion, :type, :tournament)", {"motion": motion, "type": type, "tournament":tournament})
            #Adds a new motion and relevant details to the database
            db.commit()
            return redirect(url_for("motions_index")) #redirect to motion index page

        else:
            return render_template("motioninput.html", fail_msg="That motion already exists!")


@app.route("/motions_search", methods=["GET","POST"])
def motions_search():
    fail_msg = None
    if 'username' not in session:
        return render_template("loginerror.html")

    elif request.method == "GET":
        return render_template("motions_search.html")

    else:
        motion = escape(request.form.get("motion")).upper()
        #Uppercase for consistency

        results = db.execute("SELECT * FROM motions WHERE motion LIKE (:motion)", {"motion":'%'+motion+'%'}).fetchall()
        #Returns motions that contain the searched phrase
        if len(results) == 0: #If there were no motions found
            return render_template("motions_search.html", fail_msg = "No results found! Please try again!")

        else: #If there were motions found
            return render_template("search_results.html", results=results)

@app.route("/motion/types/<type>")
def types(type): #Used when user clicks on pre-organised categories of motions
    if 'username' not in session:
        return render_template("loginerror.html")

    elif type == 'all': #If user wants to see all motions
        results = db.execute("SELECT * FROM motions")

    elif type == 'case': #If user wants to see motions with a case prepared
        results = db.execute("SELECT * FROM motions WHERE ideal_case <> ''")

    elif type == 'tournament': #If user wants to see tournament motions
        results = db.execute("SELECT * FROM motions WHERE tournament = 'Tournament'")

    else: #If user wants to see philosophical or retrospective or policy motions
        results = db.execute("SELECT * FROM motions WHERE type = :type", {"type": type})

    return render_template("search_results.html", results=results)

@app.route("/motion/<int:id>", methods=["GET", "POST"])
def motion(id): #Variable 'id' is a unique number given to each motion in the
                #database. Hence each motion has its own page
    admin_status = ""
    if 'username' not in session:
        return render_template("loginerror.html")

    if 'username' in session:
        username = session['username']

    motion = db.execute("SELECT * FROM motions where id = :id", {"id":id}).fetchone()
    #Selects the motion that the user has chosen

    if request.method == "GET":
        return render_template("motion.html", motion=motion)

    elif request.method == "POST": #If user attempts to make edits
        if db.execute("SELECT * FROM users WHERE username = :username and admin = TRUE", {"username": username}).rowcount == 1:
        # Checks that editing user has admin status and is authorised
            definitions = escape(request.form.get('definitions'))
            stances = escape(request.form.get('stances'))
            ideal_case = escape(request.form.get('ideal_case'))
            #Retrieves user input

            #Allows user to edit current entries or add to empty ones:
            db.execute("UPDATE motions SET definitions = :definitions WHERE id = :id", {"definitions":definitions, "id":id})
            db.execute("UPDATE motions SET stances = :stances WHERE id = :id", {"stances":stances, "id":id})
            db.execute("UPDATE motions SET ideal_case = :ideal_case WHERE id = :id", {"ideal_case":ideal_case, "id":id})
            db.commit()

            return redirect(url_for("motion", id=id))
            #Allows for page to refresh immediately by performing another get
            #request. Thus users can see their changes instantly

        else: #if current user is not an admin
            return render_template("motion.html", motion=motion, admin_status="You are not an administrator")

@app.route("/logout")
def logout(): #Logout
    session.pop('username', None) #Removes the user's name from the session
    return redirect(url_for('index')) #Returns to index/start page

@app.errorhandler(404)
def page_not_found(e): #Allows logout or navigation back to main search page
                       #when user accesses a non-existent page.
    return render_template('404.html'), 404
