from flask import Flask
from flask import redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import text

from os import getenv

from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

'''
Tästä lähtien oletamme, että ympäristömuuttuja DATABASE_URL kertoo tietokannan osoitteen. Tämä tieto voi olla ympäristöstä riippuen tiedostossa .env tai määritetty muulla tavalla.
'''
db = SQLAlchemy(app)

@app.route('/create_user', methods=['POST'])
def create_user():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    role = request.form['role']
    
    new_user = User(username=username, password=password, email=email, role=role)
    db.session.add(new_user)
    db.session.commit()
    
    return 'User created successfully!'


@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    

    hash_value = generate_password_hash(password)

    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

    return redirect("/")

@app.route("/signup")
def signup():
    return "Sign Up page"


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = text("INSERT INTO messages (content) VALUES (:content)")
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/")

@app.route("/find_creator")
def find_creator():
    return "Find Creator page"

@app.route("/map")
def map():
    return "Map page"


