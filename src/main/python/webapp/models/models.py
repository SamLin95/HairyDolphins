from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
import datetime

app = Flask(__name__)
#TODO Hard coded here for now, will be placed somewhere else in the future
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:superjuniors@hairydolphins.c37rymkezk94.us-east-1.rds.amazonaws.com:5432/test'
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
    def modified_at(cls):
        return db.Column(db.DateTime, onupdate=datetime.datetime.now)

class Entity(TableTemplate, db.Model, CRUD):
    id                       = db.Column(db.Integer, primary_key=True)
    username                 = db.Column(db.String(20), unique=True, nullable=False)
    password                 = db.Column(db.String(20), nullable=False)
    email                    = db.Column(db.String(120), unique=True, nullable=False)
    first_name               = db.Column(db.String(20), nullable=False)
    last_name                = db.Column(db.String(20), nullable=False)
    phone_number             = db.Column(db.String(20))
    birthday_id              = db.Column(db.Integer, db.ForeignKey('date.id'))
    is_active                = db.Column(db.Boolean, nullable=False, server_default='true')
    # role_id                  = db.Column(db.Integer, db.ForeignKey('role.id'))
    role_id                  = db.Column(db.String(20), db.ForeignKey('role.label'))
    local_advisor_profile_id = db.Column(db.Integer, db.ForeignKey('local_advisor_profile.id'), unique=True)
    admin_profile_id         = db.Column(db.Integer, db.ForeignKey('admin_profile.id'), unique=True)
    
    #Relationships
    birthday              = db.relationship('Date')
    role                  = db.relationship('Role', backref=db.backref('entities', lazy='joined'), lazy='joined')
    local_advisor_profile = db.relationship('LocalAdvisorProfile', backref=db.backref('entity', lazy='joined'), lazy='joined')
    admin_profile         = db.relationship('AdminProfile', backref=db.backref('entity', lazy='joined'), lazy='joined')
    # sent_messages         = db.relationship('Message', foreign_keys='[Message.sender_id]', backref=db.backref('sender', lazy='joined'), lazy='joined')

    def __repr__(self):
        return '<User %r>' % self.username

class Role(db.Model, CRUD):
    id    = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(20), unique=True, nullable=False)

    # def __init__(self, label):
    #     self.label = label

    def __repr__(self):
        return '<Role %r>' % self.label

#Join table of local advisor profile and date
local_advisor_available_date = db.Table( 'local_advisor_available_date',
    db.Column('local_advisor_profile_id', db.Integer, db.ForeignKey('local_advisor_profile.id')),
    db.Column('date_id', db.Integer, db.ForeignKey('date.id'), unique=True),
    db.UniqueConstraint('local_advisor_profile_id', 'date_id')
)

class LocalAdvisorProfile(TableTemplate, db.Model, CRUD):
    id          = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1024))
    city_id     = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    #Relationships
    city            = db.relationship('City', backref=db.backref('local_advisor_profiles', lazy='joined'), lazy='joined')
    available_dates = db.relationship('Date', secondary=local_advisor_available_date, backref=db.backref('local_advisor_profiles', lazy='joined'), lazy='joined')

class AdminProfile(TableTemplate, db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)

# class Message(db.Model, CRUD):
#     id           = db.Column(db.Integer, primary_key=True)
#     message_body = db.Column(db.String(1024), nullable=False)
#     sent_at      = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
#     delivered_at = db.Column(db.DateTime)
#     read_at      = db.Column(db.DateTime)
#     sender_id    = db.Column(db.Integer, db.ForeignKey('entity.id'))
#     receiver_id  = db.Column(db.Integer, db.ForeignKey('entity.id'))
    

    #Relationships
    # receiver = db.relationship('Entity', foreign_keys=[receiver_id], backref=db.backref('received_messages', lazy='joined'), lazy='joined')


class City(db.Model, CRUD):
    id       = db.Column(db.Integer, primary_key=True)
    label    = db.Column(db.String(32), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))

    #Relationships
    state    = db.relationship('State', backref=db.backref('cities', lazy='joined'), lazy='joined')

    #Constraints
    __table_args__ = (
        db.UniqueConstraint('label', 'state_id'),
        {})

class State(db.Model, CRUD):
    id        = db.Column(db.Integer, primary_key=True)
    label     = db.Column(db.String(32), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    #Relationships
    country   = db.relationship('Country', backref=db.backref('states', lazy='joined'), lazy='joined')

    #Constraints
    __table_args__ = (
        db.UniqueConstraint('label', 'country_id'),
        {})

class Country(db.Model, CRUD):
    id    = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(32), nullable=False, unique=True)

class Date(db.Model, CRUD):
    id    = db.Column(db.Integer, primary_key=True)
    date  = db.Column(db.Date, nullable=False)

class Review(TableTemplate, db.Model, CRUD):
    id                       = db.Column(db.Integer, primary_key=True)
    rating                   = db.Column(db.Integer, nullable=False)
    title                    = db.Column(db.String(64), nullable=False)
    posted                   = db.Column(db.DateTime, nullable=False)
    local_advisor_profile_id = db.Column(db.Integer, db.ForeignKey('local_advisor_profile.id'))
    reviewer_id              = db.Column(db.Integer, db.ForeignKey('entity.id'))

    #Relationships
    local_avsisor_profile = db.relationship('LocalAdvisorProfile', backref=db.backref('reviews', lazy='joined'), lazy='joined')
    reviewer = db.relationship('Entity', backref=db.backref('post_reviews', lazy='joined'), lazy='joined')

    #Constraints
    __table_args__ = (
        db.CheckConstraint('rating <= 5 and rating >= 0'),
        {})

class Recommendation(TableTemplate, db.Model, CRUD):
    id                         = db.Column(db.Integer, primary_key=True)
    title                      = db.Column(db.String(128), nullable=False)
    description                = db.Column(db.String(2048), nullable=False)
    address_line_one           = db.Column(db.String(64), nullable=False)
    address_line_two           = db.Column(db.String(64))
    is_draft                   = db.Column(db.Boolean, nullable=False, server_default='true')
    city_id                    = db.Column(db.Integer, db.ForeignKey('city.id'))
    zip_code                   = db.Column(db.String(5), nullable=False)
    recommendation_category_id = db.Column(db.Integer, db.ForeignKey('recommendation_category.id'))
    recommender_id             = db.Column(db.Integer, db.ForeignKey('entity.id'))
    # entity_recommendations_id  = db.Column(db.Integer, db.ForeignKey('entity_recommendations.id'))

    #Relationships
    city                    = db.relationship('City', backref=db.backref('recommendations', lazy='joined'), lazy='joined')
    recommendation_category = db.relationship('RecommendationCategory', backref=db.backref('recommendations', lazy='joined'), lazy='joined')
    recommender             = db.relationship('Entity', backref=db.backref('recommendations', lazy='joined'), lazy='joined')
    # entity_recommendations  = db.relationship('EntityRecommendation', backref=db.backref('recommendation', lazy='joined'), lazy='joined')

class EntityRecommendation(TableTemplate, db.Model, CRUD):
    id                            = db.Column(db.Integer, primary_key=True)
    entity_id                     = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    recommendation_id             = db.Column(db.Integer, db.ForeignKey('recommendation.id'),nullable=False)
    entity_recommendation_type_id = db.Column(db.Integer, db.ForeignKey('entity_recommendation_type.id'),nullable=False)
    
    #Relationships
    entity = db.relationship('Entity', backref=db.backref('entity_recommendations', lazy='joined'), lazy='joined')
    entity_recommendation_type = db.relationship('EntityRecommendationType', backref=db.backref('entity_recommendations', lazy='joined'), lazy='joined')
    recommendation = db.relationship('Recommendation', backref=db.backref('recommendation', lazy='joined'), lazy='joined')

class EntityRecommendationType(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    label= db.Column(db.String(32), nullable=False, unique=True)

class RecommendationCategory(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    label= db.Column(db.String(32), nullable=False, unique=True)

class EntityPhoto(db.Model, CRUD):
    id        = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    file_id   = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False, unique=True)

    #Relationships
    # entity = db.relationship('Entity', backref=db.backref('entity_photos', lazy='joined'), lazy='joined')
    file   = db.relationship('File')

class RecommendationPhoto(db.Model, CRUD):
    id                = db.Column(db.Integer, primary_key=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey('recommendation.id'), nullable=False)
    uploader_id       = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    file_id           = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False, unique=True)

    #Relationships
    uploader       = db.relationship('Entity', backref=db.backref('uploaded_recommendation_photos', lazy='joined'), lazy='joined')
    recommendation = db.relationship('Recommendation', backref=db.backref('recommendation_photos', lazy='joined'), lazy='joined')
    file           = db.relationship('File')

class File(TableTemplate, db.Model, CRUD):
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(256))
    file_type_id   = db.Column(db.Integer, db.ForeignKey('file_type.id'))
    checksum       = db.Column(db.Integer, nullable=False)
    download_link  = db.Column(db.String(1024), nullable=False)

    #Relationships
    file_type = db.relationship('FileType')

class FileType(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), unique=True)
