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


@app.route('/signup/tutor', methods=['GET', 'POST'])
def signup_tutor():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        description = request.form['description']
        profile_image = request.files['profile_image']

        profile_image_filename = None
        if profile_image:
            profile_image_filename = f'{username}_{profile_image.filename}'
            profile_image.save(path.join('static/profile_images', profile_image_filename))

        hashed_password = generate_password_hash(password)

        query = """
        INSERT INTO user_profile (username, password, email, first_name, last_name, role, description, profile_image_url, is_verified)
        VALUES (:username, :password, :email, :first_name, :last_name, 'tutor', :description, :profile_image_url, TRUE)
        """

        params = {
            'username': username,
            'password': hashed_password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'description': description,
            'profile_image_url': profile_image_filename
        }

        try:
            execute_modify(query, params)

            session['username'] = username
            session['role'] = 'tutor'
            flash('Tutor account created successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(request.url)
    else:
        return render_template('signup_tutor.html')

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
            session['username'] = username
            session['role'] = role
            flash('User created successfully!', 'success')
            return redirect(url_for('upload_profile'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(request.url)
    else:
        return render_template('signup.html')
    
@app.route('/upload_profile', methods=['GET', 'POST'])
def upload_profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        profile_image_url = request.form['profile_image_url'] 
        description = request.form['description']
        
        query = """
        UPDATE user_profile
        SET profile_image_url = :profile_image_url, description = :description
        WHERE username = :username
        """
        
        params = {
            'profile_image_url': profile_image_url,
            'description': description,
            'username': username
        }
        
        try:
            execute_modify(query, params)
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('choose_tutor_group'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('upload_profile.html')

@app.route('/choose_tutor_group', methods=['GET', 'POST'])
def choose_tutor_group():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        tutor_group_id = request.form['tutor_group_id']
        
        query = """
        UPDATE user_profile
        SET tutor_group = :tutor_group_id
        WHERE username = :username
        """
        
        params = {
            'tutor_group_id': tutor_group_id,
            'username': username
        }
        
        try:
            execute_modify(query, params)
            flash('Tutor group selected successfully!', 'success')
            return redirect(url_for('index'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(request.url)
    
    query = """
    SELECT tg.id, tg.group_name, tg.group_color, 
           t1.profile_image_url AS tutor1_image, t1.first_name AS tutor1_name, 
           t2.profile_image_url AS tutor2_image, t2.first_name AS tutor2_name
    FROM tutor_group tg
    JOIN user_profile t1 ON tg.tutor1_id = t1.id
    JOIN user_profile t2 ON tg.tutor2_id = t2.id
    """
    tutor_groups = execute_query(query).fetchall()
    
    return render_template('choose_tutor_group.html', tutor_groups=tutor_groups)



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
            return redirect(url_for('login'))  # 
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
    if 'role' in session and session['role'] == 'fresher':

        query = """
        SELECT id, title, content, status FROM challange_post
        WHERE artist_id = (SELECT id FROM user_profile WHERE username = :username)
        """
        challenges = execute_query(query, {'username': session['username']}).fetchall()
    else:

        query = """
        SELECT id, title, content, status FROM challange_post
        """
        challenges = execute_query(query).fetchall()

    return render_template('feed.html', challenges=challenges)


@app.route('/mark_challenge_complete', methods=['POST'])
def mark_challenge_complete():
    if 'role' not in session or session['role'] != 'fresher':
        flash('You do not have permission to mark challenges.', 'error')
        return redirect(url_for('feed'))

    challenge_id = request.form['challenge_id']

    query = """
    UPDATE challange_post SET status = 'pending' WHERE id = :challenge_id AND artist_id = (SELECT id FROM user_profile WHERE username = :username)
    """
    execute_modify(query, {'challenge_id': challenge_id, 'username': session['username']})


    flash('Challenge marked as complete and awaiting approval!', 'success')
    return redirect(url_for('feed'))


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

        search_query = f"%{query}%"
        sql = "SELECT * FROM user_profile WHERE role = 'artist' AND username ILIKE :search_query"
        artists = execute_query(sql, {'search_query': search_query}).fetchall()
        return render_template('search_results.html', artists=artists, query=query)
    else:
        flash('Please provide a search query.', 'error')
        return redirect(url_for('index'))

    
@app.route('/artist/<username>')
def artist_profile(username):

    query_artist = "SELECT * FROM user_profile WHERE username = :username"
    artist = execute_query(query_artist, {'username': username}).fetchone()


    query_posts = "SELECT * FROM posts WHERE artist_id = :artist_id ORDER BY created_at DESC LIMIT 5"
    posts = execute_query(query_posts, {'artist_id': artist.id}).fetchall()

    # Example query to fetch the number of followers
    query_followers = "SELECT COUNT(*) FROM followers WHERE artist_id = :artist_id"
    followers_count = execute_query(query_followers, {'artist_id': artist.id}).fetchone()[0]

    return render_template('artist_profile.html', artist=artist, followers_count=followers_count, posts=posts)


@app.route('/give_points', methods=['POST'])
def give_points():

@app.route('/review_challenge', methods=['POST'])
def review_challenge():
    if 'role' not in session or session['role'] != 'tutor':
        flash('You do not have permission to review challenges.', 'error')
        return redirect(url_for('index'))

    challenge_id = request.form['challenge_id']
    points = request.form['points']
    status = request.form['status']  

    query = """
    UPDATE challange_post SET status = :status, points_awarded = :points WHERE id = :challenge_id
    """
    execute_modify(query, {'status': status, 'points': points, 'challenge_id': challenge_id})
    flash('Challenge reviewed successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/review_challenges')
def review_challenges():
    if 'role' not in session or session['role'] != 'tutor':
        flash('You do not have permission to review challenges.', 'error')
        return redirect(url_for('feed'))

    tutor_id = session['user_id']
    query = """
    SELECT cp.id, cp.title, cp.content, cp.status, u.username, u.first_name, u.last_name
    FROM challange_post cp
    JOIN user_profile u ON cp.artist_id = u.id
    JOIN tutor_group tg ON u.tutor_group = tg.id
    WHERE cp.status = 'pending' AND (tg.tutor_1_id = :tutor_id OR tg.tutor_2_id = :tutor_id)
    """
    pending_challenges = execute_query(query, {'tutor_id': tutor_id}).fetchall()

    return render_template('review_challenges.html', pending_challenges=pending_challenges)


@app.route('/update_challenge_status', methods=['POST'])
def update_challenge_status():
    if 'role' not in session or session['role'] != 'tutor':
        flash('You do not have permission to update challenge statuses.', 'error')
        return redirect(url_for('feed'))

    challenge_id = request.form['challenge_id']
    action = request.form['action'] 
    points_awarded = request.form.get('points_awarded', 0)

    if action == 'accept':
        query = """
        UPDATE challange_post SET status = 'completed', points_awarded = :points_awarded WHERE id = :challenge_id;
        UPDATE user_profile SET points = points + :points_awarded WHERE id = (SELECT artist_id FROM challange_post WHERE id = :challenge_id)
        """
    elif action == 'deny':
        query = """
        UPDATE challange_post SET status = 'denied' WHERE id = :challenge_id
        """
    execute_modify(query, {'challenge_id': challenge_id, 'points_awarded': points_awarded})

    flash('Challenge status updated successfully!', 'success')
    return redirect(url_for('review_challenges'))






