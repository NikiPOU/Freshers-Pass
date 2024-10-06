from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def init_mail(app):
    mail.init_app(app)

def send_welcome_email(email, first_name):
    with current_app.app_context():
        msg = Message(
            "Welcome to Integralis Pass!",
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[email]
        )
        msg.body = f"Hello {first_name},\n\nYour account has been successfully created.\n\nBest Regards,\nIntegralis"
        mail.send(msg)
