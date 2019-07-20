from flask import Flask
from config import Config
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)


mail_settings = {
        "MAIL_SERVER" : 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": 'username@account.com',
        "MAIL_PASSWORD": 'password'
}

app.config.update(mail_settings)
mail = Mail(app)

from app import routes
