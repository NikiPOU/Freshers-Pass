import os
import routes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from os import getenv

app = Flask(__name__)

app.secret_key = 'nikiniki'
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pass_integralis@hotmail.com'
app.config['MAIL_PASSWORD'] = 'integralispass1000'
app.config['MAIL_DEFAULT_SENDER'] = 'pass_integralis@hotmail.com'

db = SQLAlchemy(app)
mail = Mail(app)


from mailer import init_mail
init_mail(app)

if __name__ == "__main__":
    app.run(debug=True)
