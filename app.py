import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from os import getenv
from flask_mail import Mail, Message


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

app.secret_key = 'nikiniki'

app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pass_integralis@hotmail.com'
app.config['MAIL_PASSWORD'] = 'integralispass1000'
app.config['MAIL_DEFAULT_SENDER'] = 'pass_integralis@hotmail.com'

mail = Mail(app)

def get_db_connection():
    return psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])

def execute_sql(filepath):
    with open(filepath, 'r') as file:
        sql_commands = file.read()

    conn = get_db_connection()
    cur = conn.cursor()
    for command in sql_commands.split(';'):
        command = command.strip()
        if command:
            cur.execute(command)
    cur.close()
    conn.commit()
    conn.close()

if not os.path.exists('db_initialized.txt'):
    execute_sql('db.sql')
    with open('db_initialized.txt', 'w') as file:
        file.write('Initialized')

def execute_query(sql, params=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def execute_modify(sql, params=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        tutor_group_id = request.form['tutor_group_id']
        
        hashed_password = generate_password_hash(password)
        
        sql = """
        INSERT INTO fresher_profile (username, password, email, first_name, last_name, tutor_group_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        params = (username, hashed_password, email, first_name, last_name, tutor_group_id)
        
        execute_modify(sql, params)

        session.pop('username', None)
        session.pop('role', None)

        flash('User created successfully! Please log in again.', 'success')
        
        msg = Message("Welcome to Integralis Pass!",
            sender="pass_integralis@hotmail.com",
            recipients=[email])
        msg.body = f"Hello {first_name},\n\nYour account has been successfully created.\n\nBest Regards,\nIntegralis"
        mail.send(msg)

        return redirect(url_for('login'))

    return render_template('signup.html')




@app.route('/tutorsignup', methods=['GET', 'POST'])
def tutorsignup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        tutor_group_id = request.form['tutor_group_id']
        
        hashed_password = generate_password_hash(password)
        
        sql = """
        INSERT INTO tutor_profile (username, password, email, first_name, last_name, tutor_group_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        params = (username, hashed_password, email, first_name, last_name, tutor_group_id)
        
        try:
            execute_modify(sql, params)

            session['username'] = username
            return redirect(url_for('feed'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('tutorsignup'))
    
    return render_template('signup_tutor.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        fresher_sql = "SELECT password, 'fresher' as role FROM fresher_profile WHERE username = %s"
        fresher_info = execute_query(fresher_sql, (username,))

        if fresher_info and check_password_hash(fresher_info[0][0], password):
            session["username"] = username
            session["role"] = 'fresher'
            return redirect(url_for('feed'))

        tutor_sql = "SELECT password, 'tutor' as role FROM tutor_profile WHERE username = %s"
        tutor_info = execute_query(tutor_sql, (username,))

        if tutor_info and check_password_hash(tutor_info[0][0], password):
            session["username"] = username
            session["role"] = 'tutor'
            return redirect(url_for('feed'))

        flash("Invalid username or password.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("role", None)
    return redirect(url_for('index'))

@app.route("/profile")
def profile():
    username = session.get('username')
    role = session.get('role')

    if not username:
        return redirect(url_for('index'))

    if role == 'fresher':
        sql = """
        SELECT username, first_name, last_name, email, points, 
        (SELECT COUNT(*) FROM challenge_completion WHERE fresher_id = fresher_profile.id) as completed_challenges
        FROM fresher_profile 
        WHERE username = %s
        """
        user_data = execute_query(sql, (username,))
        if not user_data:
            return redirect(url_for('index'))
        
        user_info = user_data[0]
        return render_template('profile.html', user=user_info, role=role)
    
    elif role == 'tutor':
        sql = """SELECT username, first_name, last_name, email FROM tutor_profile WHERE username = %s"""
        user_data = execute_query(sql, (username,))
        if user_data:
            user_info = user_data[0]
            return render_template('profile.html', user=user_info, role=role)
        else:
            return redirect(url_for('index'))
    else:
        flash("Invalid user role.", "error")
        return redirect(url_for('index'))


    
@app.route('/feed')
def feed():
    sql = "SELECT * FROM challenge_post ORDER BY created_at DESC"
    posts = execute_query(sql)

    freshers = []
    completed_challenges = set()
    fresher_completions = {}

    if 'role' in session and session['role'] == 'fresher':
        username = session.get('username')

        fresher_id = get_fresher_id(username)

        completed_challenges_sql = """
        SELECT challenge_id
        FROM challenge_completion
        WHERE fresher_id = %s
        """
        completed_challenges_data = execute_query(completed_challenges_sql, (fresher_id,))
        completed_challenges = {row[0] for row in completed_challenges_data}

        fresher_completions = {post[0]: 'complete' if post[0] in completed_challenges else 'incomplete' for post in posts}

    if 'role' in session and session['role'] == 'tutor':
        username = session.get('username')

        tutor_group_id_sql = "SELECT tutor_group_id FROM tutor_profile WHERE username = %s"
        tutor_group_id = execute_query(tutor_group_id_sql, (username,))[0][0]

        freshers_sql = "SELECT id, username FROM fresher_profile WHERE tutor_group_id = %s"
        freshers_data = execute_query(freshers_sql, (tutor_group_id,))
        freshers = [{'id': fresher[0], 'username': fresher[1]} for fresher in freshers_data]

        completed_challenges_sql = """
        SELECT fresher_id, challenge_id
        FROM challenge_completion
        WHERE fresher_id IN (SELECT id FROM fresher_profile WHERE tutor_group_id = %s)
        """
        completed_challenges_data = execute_query(completed_challenges_sql, (tutor_group_id,))
        completed_challenges = {(row[0], row[1]) for row in completed_challenges_data}

    return render_template('feed.html', posts=posts, freshers=freshers, completed_challenges=completed_challenges, fresher_completions=fresher_completions)



@app.route('/challenge/create', methods=['GET', 'POST'])
def create_challenge():
    if 'role' not in session or session['role'] != 'tutor':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        deadline = request.form['deadline']
        points_awarded = request.form['points_awarded']

        sql = """INSERT INTO challenge_post (title, content, deadline, points_awarded)
        VALUES (%s, %s, %s, %s)"""
        params = (title, content, deadline, points_awarded)

        try:
            execute_modify(sql, params)
            return redirect(url_for('feed'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('create_challenge'))
    
    return render_template('create_challenge.html')


@app.route('/challenge/mark_complete', methods=['POST'])
def mark_challenge_complete():
    if 'role' not in session or session['role'] != 'tutor':
        return redirect(url_for('index'))

    challenge_id = request.form.get('challenge_id')
    fresher_username = request.form.get('fresher_username')

    if not challenge_id or not fresher_username:
        return redirect(url_for('feed'))

    fresher_id = get_fresher_id(fresher_username)
    if not fresher_id:
        return redirect(url_for('feed'))

    completion_check_sql = """SELECT * FROM challenge_completion WHERE fresher_id = %s AND challenge_id = %s"""
    existing_completion = execute_query(completion_check_sql, (fresher_id, challenge_id))

    if existing_completion:
        flash("Challenge already completed for this fresher.", "info")
        return redirect(url_for('feed'))

    sql = """INSERT INTO challenge_completion (fresher_id, challenge_id) VALUES (%s, %s)"""
    execute_modify(sql, (fresher_id, challenge_id))

    update_points_sql = """
    UPDATE fresher_profile
    SET points = points + (SELECT points_awarded FROM challenge_post WHERE id = %s)
    WHERE id = %s
    """
    execute_modify(update_points_sql, (challenge_id, fresher_id))

    flash("Challenge marked complete and points updated!", "success")
    return redirect(url_for('feed'))

def get_fresher_id(username):
    sql = "SELECT id FROM fresher_profile WHERE username = %s"
    result = execute_query(sql, (username,))
    return result[0][0] if result else None

if __name__ == "__main__":
    app.run(debug=True)
