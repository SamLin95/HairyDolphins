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

# Editable tables must have those four columns
# The inheritance approach is from: http://docs.sqlalchemy.org/en/rel_1_0/orm/extensions/declarative/mixins.html#mixing-in-columns
class TableTemplate():
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

    @declared_attr
    def creator_id(cls):
        return db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)

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
    id                       = db.Column(db.Integer, primary_key=True)
    username                 = db.Column(db.String(20), unique=True, nullable=False)
    password                 = db.Column(db.String(20), nullable=False)
    email                    = db.Column(db.String(120), unique=True, nullable=False)
    first_name               = db.Column(db.String(20), nullable=False)
    last_name                = db.Column(db.String(20), nullable=False)
    phone_number             = db.Column(db.String(20))
    is_active                = db.Column(db.Boolean, nullable=False, server_default='true')
    role_id                  = db.Column(db.Integer, db.ForeignKey('role.id'))
    local_advisor_profile_id = db.Column(db.Integer, db.ForeignKey('local_advisor_profile.id'), unique=True)
    admin_profile_id         = db.Column(db.Integer, db.ForeignKey('admin_profile.id'), unique=True)
    
    #Relationships
    role                  = db.relationship('Role', backref=db.backref('entities', lazy='dynamic'))
    local_adviosr_profile = db.relationship('LocalAdvsiorProfile', backref=db.backref('entity', lazy='dynamic'))
    admin_profile         = db.relationship('AdminProfile', backref=db.backref('entity', lazy='dynamic'))
    sent_messages         = db.relationship('Message', backref='sender')

    def __init__(self, username, password, email, first_name, last_name, phone_number=None, is_active=True, role_id=None, local_advisor_profile_id=None, admin_profile_id=None):
        self.username                 = username
        self.password                 = password
        self.email                    = email
        self.first_name               = first_name
        self.last_name                = last_name
        self.phone_number             = phone_number
        self.is_active                = is_active
        self.role_id                  = role_id
        self.local_advisor_profile_id = local_advisor_profile_id
        self.admin_id                 = admin_id

    def __repr__(self):
        return '<User %r>' % self.username

class Role(db.Model, CRUD):
    id    = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return '<Role %r>' % self.label

#Join table of local advisor profile and date
local_advisor_available_dates = db.Table( 'local_advisor_available_dates',
    db.Column('local_advisor_profile_id', db.Integer, db.ForeignKey('local_advisor_profile.id')),
    db.Column('date_id', db.Integer, db.ForeignKey('date.id'))
)

class LocalAdvisorProfile(TableTemplate, db.Model, CRUD):
    id          = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1024))
    city_id     = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    #Relationships
    city            = db.relationship('City', backref='local_advisor_profiles')
    available_dates = db.relationship('Date', secondary=local_advisor_available_dates, backref=db.backref('local_advisor_profiles'), lazy='dynamic')

class AdminProfile(TableTemplate, db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)

class Message(db.Model, CRUD):
    id           = db.Column(db.Integer, primary_key=True)
    message_body = db.Column(db.String(1024), nullable=False)
    sent_at      = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    delivered_at = db.Column(db.DateTime)
    read_at      = db.Column(db.DateTime)
    sender_id    = db.Column(db.Integer, db.ForeignKey('entity.id'))
    receiver_id  = db.Column(db.Integer, db.ForeignKey('entity.id'))
    
    #Relationships
    receiver = db.relationship('Entity', backref='received_messages')

class City(db.Model, CRUD):
    id       = db.Column(db.Integer, primary_key=True)
    label    = db.Column(db.String(32), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))

    #Relationships
    state    = db.relationship('State', backref='cities')

class State(db.Model, CRUD):
    id        = db.Column(db.Integer, primary_key=True)
    label     = db.Column(db.String(32), nullable=False)
    county_id = db.Column(db.Integer, db.ForeignKey('state.id'))

    #Relationships
    country   = db.relationship('Country', backref='states')

class Country(db.Model, CRUD):
    id    = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(32), nullable=False)

class Date(db.Model, CRUD):
    id       = db.Column(db.Integer, primary_key=True)
    year     = db.Column(db.String(4), nullable=False)
    month_id = db.Column(db.Integer, db.ForeignKey('month.id'), nullable=False)
    day      = db.Column(db.Integer, nullable=False)

    #Relationships
    month    = db.relationship('Month', backref='dates')

class Month(db.Model, CRUD):
    id    = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(32), nullable=False)

class Review(TableTemplate, db.Model, CRUD):
    id                       = db.Column(db.Integer, primary_key=True)
    rating                   = db.Column(db.Integer, nullable=False)
    title                    = db.Column(db.String(64), nullable=False)
    posted                   = db.Column(db.DateTime, nullable=False)
    local_advisor_profile_id = db.Column(db.Integer, db.ForeignKey('entity.id'))

    #Relationships
    local_avsisor_profile = db.relationship('LocalAdvisorProfile', backref='reviews')

    #Constraints
    __table_args__ = (
        db.CheckConstraint('rating <= 5 and rating >= 0'),
        {})
    
    

