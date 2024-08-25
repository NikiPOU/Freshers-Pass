import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import create_engine

from os import getenv

from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


def execute_raw_sql_file(filepath):
    with open(filepath, 'r') as file:
        sql_commands = file.read()
    
    with engine.connect() as connection:
        for command in sql_commands.split(';'):
            command = command.strip()
            if command:
                connection.execute(text(command))
                connection.execute(text("COMMIT"))

databasee = 'database.sql'

if not os.path.exists('initialized.txt'):
    execute_raw_sql_file(databasee)

    with open('initialized.txt', 'w') as file:
        file.write('Initialized')


def execute_query(query, params=None):
    with engine.connect() as connection:
        result = connection.execute(text(query), params or {})
        return result

def execute_modify(query, params=None):
    with engine.connect() as connection:
        result = connection.execute(text(query), params or {})
        connection.execute(text("COMMIT"))
        return result

if __name__ == "__main__":
    app.run(debug=True)


    
@app.route('/')
def index():
    print("Session username:", session.get('username'))
    print("Session role:", session.get('role'))
    return render_template('index.html')




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        date_of_birth = request.form['date_of_birth']
        role = request.form['role']
        
        hashed_password = generate_password_hash(password)
        
        query = """
        INSERT INTO user_profile (username, password, email, first_name, last_name, gender, date_of_birth, role)
        VALUES (:username, :password, :email, :first_name, :last_name, :gender, :date_of_birth, :role)
        """
        
        params = {
            'username': username,
            'password': hashed_password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'date_of_birth': date_of_birth,
            'role': role
        }
        
        try:
            execute_modify(query, params)
            # Set session variables after successful signup
            session['username'] = username
            session['role'] = role
            flash('User created successfully!', 'success')
            return redirect(url_for('index'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(request.url)
    else:
        return render_template('signup.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        query = "SELECT password, role FROM user_profile WHERE username = :username"
        result = execute_query(query, {"username": username}).fetchone()

        if result is not None and check_password_hash(result[0], password):
            session["username"] = username
            session["role"] = result[1]
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for('login'))  # Redirect to login page on failed login
    else:
        return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("role", None)
    return redirect(url_for('index'))


@app.route("/profile")
def profile():

    username = session['username']
    query = "SELECT username, first_name, last_name, role FROM user_profile WHERE username = :username"
    user_data = execute_query(query, {'username': username}).fetchone()
    
    return render_template('profile.html', user=user_data)

@app.route('/feed')
def feed():
    return render_template('feed.html')

@app.route("/post")
def post():
    return render_template("post.html")

@app.route("/find_creator")
def find_creator():
    return "Find Creator page"

@app.route("/map")
def map():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    
    if query:
        # Implement logic to search for artists based on the query
        search_query = f"%{query}%"
        sql = "SELECT * FROM user_profile WHERE role = 'artist' AND username ILIKE :search_query"
        artists = execute_query(sql, {'search_query': search_query}).fetchall()
        return render_template('search_results.html', artists=artists, query=query)
    else:
        flash('Please provide a search query.', 'error')
        return redirect(url_for('index'))

    
# Flask route for displaying artist profile
@app.route('/artist/<username>')
def artist_profile(username):
    # Fetch artist details from the database based on username
    query_artist = "SELECT * FROM user_profile WHERE username = :username"
    artist = execute_query(query_artist, {'username': username}).fetchone()

    # Example query to fetch most recent posts of the artist
    query_posts = "SELECT * FROM posts WHERE artist_id = :artist_id ORDER BY created_at DESC LIMIT 5"
    posts = execute_query(query_posts, {'artist_id': artist.id}).fetchall()

    # Example query to fetch the number of followers
    query_followers = "SELECT COUNT(*) FROM followers WHERE artist_id = :artist_id"
    followers_count = execute_query(query_followers, {'artist_id': artist.id}).fetchone()[0]

    return render_template('artist_profile.html', artist=artist, followers_count=followers_count, posts=posts)




