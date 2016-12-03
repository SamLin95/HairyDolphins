from flask import Flask
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_searchable import make_searchable
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import datetime
from .. import app

#The Postgres Database URI needs to be set here
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:superjuniors@hairydolphins.c37rymkezk94.us-east-1.rds.amazonaws.com:5432/test'

#Initialze the sqlalchemy database object
db = SQLAlchemy(app)

#The postgres full-text search setting chosen: simple mode. 
make_searchable(options={'regconfig': 'pg_catalog.simple'})

#Query classes for full text searching
class EntityQuery(BaseQuery, SearchQueryMixin):
    pass

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

#Users of the webiste
class Entity(TableTemplate, db.Model, CRUD):
    #Changed the default query to self-defined EntityQuery
    query_class = EntityQuery

    #Attrbutes
    id                       = db.Column(db.Integer, primary_key=True)
    username                 = db.Column(db.String(20), unique=True, nullable=False)
    password                 = db.Column(db.String(20), nullable=False)
    email                    = db.Column(db.String(120), unique=True, nullable=False)
    first_name               = db.Column(db.String(20), nullable=False)
    last_name                = db.Column(db.String(20), nullable=False)
    phone_number             = db.Column(db.String(20))
    birthday_id              = db.Column(db.Integer, db.ForeignKey('date.id'))
    is_active                = db.Column(db.Boolean, nullable=False, server_default='true')
    role_id                  = db.Column(db.Integer, db.ForeignKey('role.id'))
    local_advisor_profile_id = db.Column(db.Integer, db.ForeignKey('local_advisor_profile.id'), unique=True)
    admin_profile_id         = db.Column(db.Integer, db.ForeignKey('admin_profile.id'), unique=True)

    #Relationships
    birthday              = db.relationship('Date')
    role                  = db.relationship('Role', backref=db.backref('entities'))
    local_advisor_profile = db.relationship('LocalAdvisorProfile', backref=db.backref('entity'))
    admin_profile         = db.relationship('AdminProfile', backref=db.backref('entity'))
    sent_messages         = db.relationship('Message', foreign_keys='[Message.sender_id]', backref=db.backref('sender'))

    #Seach Vector
    search_vector = db.Column(TSVectorType('username', 'first_name', 'last_name'))

    #Four subroutines required by Flask-Login. The id is defined using entity's primary index.
    def is_active(self):
        return self.is_active;

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    #The profile photo url of an Entity
    @hybrid_property
    def profile_photo_url(self):
        #Among all pictures owned by a user, profile pictures are those whose is_profile_picture attribute is true.
        profile_photos = filter(lambda entity_photo: entity_photo.is_profile_picture  == True, self.entity_photos)

        if(profile_photos):
            profile_photo = profile_photos[0];
            return profile_photo.file.download_link
        else:
            return None

    #The average rating of an Entity if the role is local advisor
    @hybrid_property
    def average_rating(self):
        if(self.local_advisor_profile):
            return self.local_advisor_profile.average_rating
        else:
            return None

    #This is the hybrid attribute designed for messenger to get recent contacts
    @hybrid_property
    def contacts(self):
        messages=[]
        if(self.sent_messages or self.received_messages):
            for message in self.received_messages:
                duplicate = False
                replacable = False
                replace_index = None
                #For every messsage recieved, check if its sender is in the current list
                for i in range(len(messages)):
                    checked_message = messages[i]
                    #If the sender exists, compare the sent time.
                    if(checked_message['user_id'] == message.sender.id):
                        duplicate = True
                        replace_index = i
                        if(checked_message['sent_at'] < message.sent_at):
                            replacable = True

                if(duplicate):
                    messages[replace_index]['unread_count'] += (0 if message.read_at else 1)

                    if(replacable):
                        messages[replace_index] = \
                        {\
                            'sent_at': message.sent_at,\
                            'user_id': message.sender.id,\
                            'unread_count' : messages[replace_index]['unread_count']
                        }
                else:
                    messages.append(\
                    {\
                        'sent_at': message.sent_at,\
                        'user_id': message.sender.id,\
                        'unread_count' :  (0 if message.read_at else 1)
                    })

            #For every messsage sent, check if its receiver is in the current list
            for message in self.sent_messages:
                duplicate = False
                replacable = False
                replace_index = None
                for i in range(len(messages)):
                    checked_message = messages[i]
                    #If the receiver exists, compare the sent time.
                    if(checked_message['user_id'] == message.receiver.id):
                        duplicate = True
                        replace_index = i
                        if(checked_message['sent_at'] < message.sent_at):
                            replacable = True

                if(duplicate):
                    if(replacable):
                        messages[replace_index] =\
                        {\
                            'sent_at': message.sent_at,\
                            'user_id': message.receiver.id,\
                            'unread_count' :  messages[replace_index]['unread_count']
                        }
                else:
                    messages.append(\
                    {\
                        'sent_at': message.sent_at,\
                        'user_id': message.receiver.id,\
                        'unread_count' : 0
                    })

            messages.sort(key=lambda message:message['sent_at'], reverse=True)

            contacts = []
            for message in messages:
                contacts.append({ 'user': Entity.query.get(message['user_id']), 'unread_count': message['unread_count'] if 'unread_count' in message else 0})
                
            return contacts
        else:
            return None

    def load_hybrid_properties(self):
        self.average_rating
        self.profile_photo_url
        self.contacts

    def __repr__(self):
        return '<User %r>' % self.username

#The table stores all possible user roles that exist in the system.
class Role(db.Model, CRUD):
    id    = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Role %r>' % self.label

# revised: delete date_id unique=True
#Join table of local advisor profile and date which indicates on what dates a local advisor is available.
local_advisor_available_date = db.Table( 'local_advisor_available_date',
    db.Column('local_advisor_profile_id', db.Integer, db.ForeignKey('local_advisor_profile.id')),
    db.Column('date_id', db.Integer, db.ForeignKey('date.id')),
    db.UniqueConstraint('local_advisor_profile_id', 'date_id')
)

#The table stores which recommendations can be provided by which local advisors.
local_advisor_recommendation = db.Table('local_advisor_recommendation',
    db.Column('local_advisor_profile_id', db.Integer, db.ForeignKey('local_advisor_profile.id')),
    db.Column('recommendation_id', db.Integer, db.ForeignKey('recommendation.id')),
    db.UniqueConstraint('local_advisor_profile_id', 'recommendation_id')
)

#The additional infomration for a local advisor user.
class LocalAdvisorProfile(TableTemplate, db.Model, CRUD):
    id          = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1024))
    city_id     = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    #Relationships
    city            = db.relationship('City')
    available_dates = db.relationship('Date', secondary=local_advisor_available_date)
    recommendations = db.relationship('Recommendation', secondary=local_advisor_recommendation)

    #Seach Vector
    search_vector = db.Column(TSVectorType('description'))

    #The average rating of a local advisor.
    @hybrid_property
    def average_rating(self):
        if(self.reviews):
            return float(sum(review.rating for review in self.reviews))/float(len(self.reviews))
        else:
            return None

    #Load the hybrid properties so so that they could be initialized
    def load_hybrid_properties(self):
        self.average_rating

#The table reserved to store additional information for a administrator
class AdminProfile(TableTemplate, db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)

#The messages sent among users.
class Message(db.Model, CRUD):
    id           = db.Column(db.Integer, primary_key=True)
    message_body = db.Column(db.String(1024), nullable=False)
    sent_at      = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    read_at      = db.Column(db.DateTime)
    sender_id    = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    receiver_id  = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)

    #Relationships
    receiver = db.relationship('Entity', foreign_keys=[receiver_id], backref=db.backref('received_messages'))

#The table which stores city information
class City(db.Model, CRUD):
    id       = db.Column(db.Integer, primary_key=True)
    label    = db.Column(db.String(32), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))

    #Relationships
    state    = db.relationship('State', backref=db.backref('cities'))

    #Seach Vector
    search_vector = db.Column(TSVectorType('label'))

    #Constraints
    __table_args__ = (
        db.UniqueConstraint('label', 'state_id'),
        {})

#The table which stores state information
class State(db.Model, CRUD):
    id        = db.Column(db.Integer, primary_key=True)
    label     = db.Column(db.String(32), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))

    #Relationships
    country   = db.relationship('Country', backref=db.backref('states'))

    #Seach Vector
    search_vector = db.Column(TSVectorType('label'))

    #Constraints
    __table_args__ = (
        db.UniqueConstraint('label', 'country_id'),
        {})

#The table which stores country information
class Country(db.Model, CRUD):
    id    = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(32), nullable=False, unique=True)

    #Seach Vector
    search_vector = db.Column(TSVectorType('label'))

#The table which stores date information
class Date(db.Model, CRUD):
    id    = db.Column(db.Integer, primary_key=True)
    date  = db.Column(db.Date, nullable=False)

#The table which stores reviews of local advisors or recommendations
class Review(TableTemplate, db.Model, CRUD):
    id                       = db.Column(db.Integer, primary_key=True)
    rating                   = db.Column(db.Integer, nullable=False)
    title                    = db.Column(db.String(64), nullable=False)
    content                  = db.Column(db.String(2048), nullable=False)
    posted                   = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    local_advisor_profile_id = db.Column(db.Integer, db.ForeignKey('local_advisor_profile.id'))
    recommendation_id        = db.Column(db.Integer, db.ForeignKey('recommendation.id'))
    reviewer_id              = db.Column(db.Integer, db.ForeignKey('entity.id'))

    #Relationships
    local_advisor_profile = db.relationship('LocalAdvisorProfile', backref=db.backref('reviews'))
    recommendation = db.relationship('Recommendation', backref=db.backref('reviews'))
    reviewer = db.relationship('Entity', backref=db.backref('post_reviews'))

    #Constraints
    __table_args__ = (
        db.CheckConstraint('rating <= 5 and rating >= 0'),
        db.CheckConstraint('(local_advisor_profile_id is null) <> (recommendation_id is null)'),
        {})

#The table which stores recommended places.
class Recommendation(TableTemplate, db.Model, CRUD):
    id                         = db.Column(db.Integer, primary_key=True)
    title                      = db.Column(db.String(128), nullable=False)
    description                = db.Column(db.String(2048), nullable=False)
    address_line_one           = db.Column(db.String(64), nullable=False)
    address_line_two           = db.Column(db.String(64))
    is_draft                   = db.Column(db.Boolean, nullable=False, server_default='true')
    city_id                    = db.Column(db.Integer, db.ForeignKey('city.id'))
    zip_code                   = db.Column(db.String(6), nullable=False)
    recommendation_category_id = db.Column(db.Integer, db.ForeignKey('recommendation_category.id'))
    recommender_id             = db.Column(db.Integer, db.ForeignKey('entity.id'))

    #Relationships
    city                    = db.relationship('City')
    recommendation_category = db.relationship('RecommendationCategory')
    recommender             = db.relationship('Entity', backref=db.backref('recommendations'))
    entity_recommendations  = db.relationship('EntityRecommendation', backref=db.backref('recommendation'))
    local_advisor_profiles  = db.relationship('LocalAdvisorProfile', secondary=local_advisor_recommendation)

    #The primary picture url of a recommendation to be displayed in the FE
    @hybrid_property
    def primary_picture(self):
        if(self.recommendation_photos):
            return self.recommendation_photos[0].file.download_link
        else:
            return None

    #The average rating of the recommendation
    @hybrid_property
    def average_rating(self):
        if(self.reviews):
            return float(sum(review.rating for review in self.reviews))/float(len(self.reviews))
        else:
            return None

    #Load the hybrid properties so so that they could be initialized
    def load_hybrid_properties(self):
        self.average_rating
        self.primary_picture

#The table which stores which recommendations are liked by which users and reasons behind.
class EntityRecommendation(TableTemplate, db.Model, CRUD):
    id                = db.Column(db.Integer, primary_key=True)
    entity_id         = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    recommendation_id = db.Column(db.Integer, db.ForeignKey('recommendation.id'), nullable=False)
    reason            = db.Column(db.String(2048))

    #Relationships
    entity = db.relationship('Entity', backref=db.backref('entity_recommendations'))

#The table which stores possible categories of a recommendation
class RecommendationCategory(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    label= db.Column(db.String(32), nullable=False, unique=True)

#The table which stores photos owned by a user
class EntityPhoto(db.Model, CRUD):
    id                 = db.Column(db.Integer, primary_key=True)
    entity_id          = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    file_id            = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False, unique=True)
    is_profile_picture = db.Column(db.Boolean, nullable = False)

    #Relationships
    entity = db.relationship('Entity', backref=db.backref('entity_photos'))
    file   = db.relationship('File')

    #Constraints
    __table_args__ = (
        db.UniqueConstraint('entity_id', 'file_id'),
        db.Index('ix_unique_profile_pic', 'entity_id', unique=True, postgresql_where=(is_profile_picture)),
        {})

#The table which stores photos uploaded for a recommendation
class RecommendationPhoto(db.Model, CRUD):
    id                = db.Column(db.Integer, primary_key=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey('recommendation.id'), nullable=False)
    uploader_id       = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    file_id           = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False, unique=True)

    #Relationships
    uploader       = db.relationship('Entity', backref=db.backref('uploaded_recommendation_photos'))
    recommendation = db.relationship('Recommendation', backref=db.backref('recommendation_photos'))
    file           = db.relationship('File')

    #Contraints
    __table_args__ = (
        db.UniqueConstraint('recommendation_id', 'file_id'),
        {})


#The table which stores files metadata
class File(TableTemplate, db.Model, CRUD):
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(256))
    file_type_id   = db.Column(db.Integer, db.ForeignKey('file_type.id'), nullable=False)
    checksum       = db.Column(db.Integer, nullable=False)
    download_link  = db.Column(db.String(1024), nullable=False)

    #Relationships
    file_type = db.relationship('FileType')

#The table which stores possible file types of a file
class FileType(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), unique=True)
