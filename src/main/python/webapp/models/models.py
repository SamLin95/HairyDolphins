from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:superjuniors@hairydolphins.c37rymkezk94.us-east-1.rds.amazonaws.com:5432/dev'
db = SQLAlchemy(app)


class Entity(db.Model):
    id                    = db.Column(db.Integer, primary_key=True)
    username              = db.Column(db.String(20), unique=True)
    password              = db.Column(db.String(20))
    email                 = db.Column(db.String(120), unique=True)
    first_name            = db.Column(db.String(20))
    last_name             = db.Column(db.String(20))
    phone_number          = db.Column(db.String(20))
    role                  = db.Column(db.Integer)
    local_advisor_profile = db.Column(db.Integer, unique=True)
    admin_profile         = db.Column(db.Integer, unique=True)

    def __init__(self, username, password, email, first_name, last_name):
        self.username   = username
        self.password   = password
        self.email      = email
        self.first_name = first_name
        self.last_name  = last_name

    def __repr__(self):
        return '<User %r>' % self.username
