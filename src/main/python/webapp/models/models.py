from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:superjuniors@hairydolphins.c37rymkezk94.us-east-1.rds.amazonaws.com:5432/dev'
db = SQLAlchemy(app)

#Class to add, update and delete data via SQLALchemy sessions
class CRUD():   
 
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()   
 
    def update(self):
        return db.session.commit()
 
    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

# All tables must have those four columns
# The inheritance approach is from: http://docs.sqlalchemy.org/en/rel_1_0/orm/extensions/declarative/mixins.html#mixing-in-columns
class TableTemplate():
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.datetime.now)

    @declared_attr
    def creator_id(cls):
        return db.Column(db.Integer, db.ForeignKey('entity.id'))

    @declared_attr
    def creator(cls):
        return db.relationship('Entity', backref=db.backref('entity', lazy='dynamic'))

    @declared_attr
    def modified_at(cls):
        return db.Column(db.DateTime, onupdate=datetime.datetime.now)

    @declared_attr
    def modifier_id(cls):
        return db.Column(db.Integer, db.ForeignKey('entity.id'))

    @declared_attr
    def modifier(cls):
        return db.relationship('Entity', backref=db.backref('entity', lazy='dynamic'))

class Entity(TableTemplate, db.Model, CRUD):
    id           = db.Column(db.Integer, primary_key=True)
    username     = db.Column(db.String(20), unique=True, nullable=False)
    password     = db.Column(db.String(20), nullable=False)
    email        = db.Column(db.String(120), unique=True, nullable=False)
    first_name   = db.Column(db.String(20), nullable=False)
    last_name    = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20))
    is_active    = db.Column(db.Boolean, nullable=False, server_default='true')
    
    #Foreign Keys
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role    = db.relationship('Role', backref=db.backref('entities', lazy='dynamic'))

    local_advisor_profile_id = db.Column(db.Integer, db.ForeignKey('local_advisor_profile.id'), unique=True)
    local_adviosr_profile    = db.relationship('LocalAdvsiorProfile', backref=db.backref('entity', lazy='dynamic'))

    admin_profile_id = db.Column(db.Integer, db.ForeignKey('admin_profile.id'), unique=True)
    admin_profile    = db.relationship('AdminProfile', backref=db.backref('entity', lazy='dynamic'))

    message_senders = db.relationship('Message', backref='receiver')

    

    def __init__(self, username, password, email, first_name, last_name):
        self.username   = username
        self.password   = password
        self.email      = email
        self.first_name = first_name
        self.last_name  = last_name

    def __repr__(self):
        return '<User %r>' % self.username

class Role(TableTemplate, db.Model, CRUD):
    id    = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return '<Role %r>' % self.label

class LocalAdvisorProfile(TableTemplate, db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)

class AdminProfile(TableTemplate, db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)

class Message(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True) 
    message_body = db.Column(db.String(1024), nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    delivered_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)
    
    #Foreign Keys
    sender_id = db.Column(db.Integer, db.ForeignKey('entity.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('entity.id'))

    sender = db.relationship('Entity', backref='sent_messages')
