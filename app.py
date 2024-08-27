import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
import psycopg2
from psycopg2 import sql
from werkzeug.security import generate_password_hash
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

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
    cur.execute(sql, params or {})
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def execute_modify(sql, params=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql, params or {})
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
        
        hashed_password = generate_password_hash(password)
        
        sql = """
        INSERT INTO user_profile (username, password, email, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        params = (username, hashed_password, email, first_name, last_name)
        
        try:
            execute_modify(sql, params)

            session['username'] = username
            flash('User created successfully!', 'success')
            return redirect(url_for('index'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('signup'))
    
    return render_template('signup.html')



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT password, role FROM user_profile WHERE username = :username"
        result = execute_query(sql, {"username": username}).fetchone()

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
    sql = "SELECT username, first_name, last_name, role FROM user_profile WHERE username = :username"
    user_data = execute_query(sql, {'username': username}).fetchone()
    
    return render_template('profile.html', user=user_data)



if __name__ == "__main__":
    app.run(debug=True)


