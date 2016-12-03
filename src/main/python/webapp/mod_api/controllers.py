from flask import Blueprint, request, render_template, redirect, url_for, Flask, jsonify
import werkzeug
import flask_restful
from sqlalchemy import and_, or_, exc, func
from flask_restful import reqparse
from flask_restful_swagger import swagger
from datetime import datetime
from sqlalchemy_searchable import search, parse_search_query

from ..models.models import *
from ..models.schemas import *
from ..lib.s3_lib import *

#API Versions and Conventioanl HTTP Codes Constants
API_VERSION = 1

HTTP_BAD_REQUEST                     = 400
HTTP_UNAUTHORIZED                    = 401
HTTP_PAYMENT_REQUIRED                = 402
HTTP_FORBIDDEN                       = 403
HTTP_NOT_FOUND                       = 404
HTTP_METHOD_NOT_ALLOWED              = 405
HTTP_NOT_ACCEPTABLE                  = 406
HTTP_PROXY_AUTHENTICATION_REQUIRED   = 407
HTTP_REQUEST_TIMEOUT                 = 408
HTTP_CONFLICT                        = 409
HTTP_GONE                            = 410
HTTP_LENGTH_REQUIRED                 = 411
HTTP_PRECONDITION_FAILED             = 412
HTTP_REQUEST_ENTITY_TOO_LARGE        = 413
HTTP_REQUEST_URI_TOO_LONG            = 414
HTTP_UNSUPPORTED_MEDIA_TYPE          = 415
HTTP_REQUESTED_RANGE_NOT_SATISFIABLE = 416
HTTP_EXPECTATION_FAILED              = 417
HTTP_PRECONDITION_REQUIRED           = 428
HTTP_TOO_MANY_REQUESTS               = 429
HTTP_REQUEST_HEADER_FIELDS_TOO_LARGE = 431
HTTP_INTERNAL_SERVER_ERROR           = 500
HTTP_NOT_IMPLEMENTED                 = 501
HTTP_BAD_GATEWAY                     = 502
HTTP_SERVICE_UNAVAILABLE             = 503
HTTP_GATEWAY_TIMEOUT                 = 504
HTTP_HTTP_VERSION_NOT_SUPPORTED      = 505
HTTP_NETWORK_AUTHENTICATION_REQUIRED = 511

#Makes the API an Blueprint object.
mod_api = Blueprint('api', __name__, url_prefix='/api')
api = flask_restful.Api()
#Calling init_app can defer for Blueprint object
api.init_app(mod_api)
#The swagger module is a simple way to create API documentation in the future.
api = swagger.docs(api, apiVersion=API_VERSION, api_spec_url='/spec')

class Recommendations(flask_restful.Resource):
    #Returns the information of a list of recommendations which meet all given criteria
    def get(self):
        #Define arguments
        parser = reqparse.RequestParser()
        parser.add_argument('recommendation_id', type=int)
        parser.add_argument('recommendation_category_id', type=int)
        parser.add_argument('city_id', type=int)
        parser.add_argument('limit', type=int)
        parser.add_argument('request_fields', type=str, action='append')

        #Parse arguments and store in a dict
        args = parser.parse_args()

        #Initialize the query object to construct query
        recommendation_query = Recommendation.query

        #Only dump required fields
        if(args['request_fields']):
            request_fields = tuple(args['request_fields'])
            recommendation_schema = RecommendationSchema(only=request_fields)
        else:
            recommendation_schema = RecommendationSchema()

        #Ignore all other search criteria and return the specific recommendation if id given.
        if args['recommendation_id']:
            recommendation_id = args['recommendation_id']
            recommendation = recommendation_query.get(recommendation_id)

            if(not recommendation):
                return {"message" :"Recommendation not found"}, HTTP_NOT_FOUND

            try:
                recommendation_json = recommendation_schema.dump(recommendation).data
                return recommendation_json
            except AttributeError as err:
                return {"message" : {"request_fields" : format(err)}}, HTTP_BAD_REQUEST
        else:
            #Add filters if given
            if(args['recommendation_category_id']):
                recommendation_category_id = args['recommendation_category_id']
                recommendation_query = recommendation_query.filter_by(recommendation_category_id=recommendation_category_id)

            if(args['city_id']):
                city_id = args['city_id']
                recommendation_query = recommendation_query.filter_by(city_id=city_id)

            if(args['limit']):
                limit = args['limit']
                recommendation_query = recommendation_query.limit(limit)

            recommendations = recommendation_query.all()

            #Return error message if no recommnedation found
            if(not recommendations):
                return {"message" :"No expected recommendation found"}, HTTP_NOT_FOUND

            #Return recommendations as JSON object if found
            try:
                recommendation_json = recommendation_schema.dump(recommendations, many=True).data
                return recommendation_json
            except AttributeError as err:
                return {"message" : {"request_fields" : format(err)}}, HTTP_BAD_REQUEST

    #The route to create a new recommendation
    def post(self):
        #Define arguments and parse arguments
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('address_line_one', type=str, required=True)
        parser.add_argument('address_line_two', type=str)
        parser.add_argument('zip_code', type=str, required=True)
        parser.add_argument('city_id', type=int, required=True)
        parser.add_argument('recommender_id', type=int, required=True)
        parser.add_argument('recommendation_category_id', type=int, required=True)
        parser.add_argument('file_id', type=int, required=True)
        args = parser.parse_args()

        title = args['title']
        description = args['description']
        address_line_one = args['address_line_one']
        address_line_two = args['address_line_two']
        zip_code = args['zip_code']
        city_id = args['city_id']
        recommendation_category_id = args['recommendation_category_id']
        recommender_id = args['recommender_id']
        file_id = args['file_id']

        try:
            #Create the recommendation object
            new_recommendation = Recommendation(title=title, description=description, address_line_one=address_line_one, address_line_two=address_line_two, zip_code=zip_code, recommender_id=recommender_id, city_id=city_id, recommendation_category_id=recommendation_category_id,is_draft=False)

            #Write to database
            new_recommendation.add(new_recommendation)

            #If recommendation photo file is given, then associate it with the newly created recommendation
            new_recommendation_photo = RecommendationPhoto(recommendation=new_recommendation, file_id=file_id, uploader_id=recommender_id)
            new_recommendation_photo.add(new_recommendation_photo)

            #Dump the newly created recommendation and returns to user.
            recommendation_schema = RecommendationSchema()
            recommendation_json = recommendation_schema.dump(new_recommendation).data
        except exc.IntegrityError as err:
            return{"message" : "Failed to add recommendation during database execution. The error message returned is: {0}".format(err)}, HTTP_BAD_REQUEST

        return recommendation_json 

api.add_resource(Recommendations, '/recommendations')

class RecommendationResource(flask_restful.Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('request_fields', type=str, action='append')

        self.parser = parser

    #Returns the information of the recommendation with given id
    def get(self, recommendation_id):
        args = self.parser.parse_args()
        recommendation_query = Recommendation.query

        #Only dump required fields
        if(args['request_fields']):
            request_fields = tuple(args['request_fields'])
            recommendation_schema = RecommendationSchema(only=request_fields)
        else:
            recommendation_schema = RecommendationSchema()

        recommendation = recommendation_query.get(recommendation_id)

        #Return 404 error if the id is not valid
        if(not recommendation):
            return {"message" :"Recommendation not found"}, HTTP_NOT_FOUND

        #Return the recommendation in JSON formats
        try:
            recommendation_json = recommendation_schema.dump(recommendation).data
            return recommendation_json
        except AttributeError as err:
            return {"message" : {"request_fields" : format(err)} }, HTTP_BAD_REQUEST

api.add_resource(RecommendationResource, '/recommendations/<int:recommendation_id>')

class User(flask_restful.Resource):
    #Initialize the parser and define arguments
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('request_fields', type=str, action='append')

        self.parser = parser

    #Returns the information of the user with given id while ignoring all other search criteria
    def get(self, user_id):
        args = self.parser.parse_args()
        #Initialize the query object for query construction
        entity_query = Entity.query

        #Only dump required fields
        if(args['request_fields']):
            request_fields = tuple(args['request_fields'])
            entity_schema = EntitySchema(exclude='password', only=request_fields)
        else:
            entity_schema = EntitySchema(exclude='password')

        entity = entity_query.get(user_id)

        if(not entity):
            return {"message" :"User not found"}, HTTP_NOT_FOUND

        try:
            entity_json = entity_schema.dump(entity).data
            return entity_json
        except AttributeError as err:
            return {"message" : {"request_fields" : format(err)} }, HTTP_BAD_REQUEST

    #The route to update profile of an existing user.
    def put(self, user_id):
        #Define arguments and parse arguments
        parser = reqparse.RequestParser()
        parser.add_argument('phone_number', type=str)
        parser.add_argument('birthday', type=str)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('file_id', type=int)
        args = parser.parse_args()

        phone_number= args['phone_number']
        birthday = args['birthday']
        email = args['email']
        first_name = args['first_name']
        last_name = args['last_name']
        file_id = args['file_id']

        #Make sure that the email doesn't conflict with any existing email
        existing_entity = Entity.query.filter(and_(Entity.email==email, Entity.id!=user_id)).first()
        if(existing_entity):
            return {"message" :"Email already used"}, HTTP_BAD_REQUEST

        try:
            #Get the original entity from the database for modification
            entity = Entity.query.get(user_id)

            entity.email = email
            entity.first_name = first_name
            entity.last_name = last_name
            entity.phone_number = phone_number
            if(args['birthday']):
                #Reformat the birthday to make it legitimate for Postgres. Then
                #look for the birthday on the Date table. If the date doesn't exist,
                #the route will add this date to the date table.
                birthday= datetime.datetime.strptime(args['birthday'], "%Y-%m-%d")
                birthday_date = Date.query.filter(Date.date==birthday).first()
                if(not birthday_date):
                    birthday_date = Date(date=birthday)
                    birthday_date.add(birthday_date)
        
                entity.birthday = birthday_date

            #If file_id is given, the profile picture has been changed. The old profile
            #picture needs to be changed to not be the profile picture and the new photo
            #should be assoicated.
            if(file_id):
                old_profile_picture = EntityPhoto.query.filter(and_(EntityPhoto.entity_id==user_id, EntityPhoto.is_profile_picture==True)).first()
                if(old_profile_picture):
                    old_profile_picture.is_profile_picture = False
                    old_profile_picture.update()

                entity_photo = EntityPhoto(file_id=file_id, entity_id=user_id, is_profile_picture=True)
                entity_photo.add(entity_photo)

            entity.update()

            #Dump the modified entity in JSON format
            entity_schema = EntitySchema(only=("id", "first_name", "last_name", "email", "username",     "birthday", "phone_number", "profile_photo_url", "role"))
            entity_json = entity_schema.dump(entity).data
        except exc.IntegrityError as err:
            return{"message" : "Failed to add use during database execution. The error message returned is: {0}".format(err)}, HTTP_BAD_REQUEST
        except ValueError as err:
             return {"message" : {"birthday": format(err)}}, HTTP_BAD_REQUEST

        return entity_json

api.add_resource(User, '/users/<int:user_id>')

class Users(flask_restful.Resource):
    #Returns the information of a list of users which meet all given criteria
    def get(self):
        #Define arguments and parse arguments
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('role_id', type=int)
        parser.add_argument('city_id', type=int)
        parser.add_argument('available_date', type=str)
        parser.add_argument('keyword', type=str)
        parser.add_argument('limit', type=int)
        parser.add_argument('request_fields', type=str, action='append')
        args = parser.parse_args()

        #Initialize the entity query for query construction
        entity_query = Entity.query

        #Dump only required fields if defined
        if(args['request_fields']):
            request_fields = tuple(args['request_fields'])
            entity_schema = EntitySchema(exclude=('password',), only=request_fields)
        else:
            entity_schema = EntitySchema(exclude=('password',))

        #If the specific id is given. The route should ignore other searching
        #criteria and returns the user with the given id.
        if args['user_id']:
            user_id = args['user_id']
            entity = entity_query.get(user_id)

            if(not entity):
                return {"message" :"User not found"}, HTTP_NOT_FOUND

            try:
                entity_json = entity_schema.dump(entity).data
                return entity_json
            except AttributeError as err:
                return {"message" : {"request_fields" : format(err)}}, HTTP_BAD_REQUEST
        else:
            #Add any filter that has been specified.
            if(args['role_id']):
                role_id = args['role_id']
                entity_query = entity_query.filter_by(role_id=role_id)

            if(args['available_date']):
                try:
                    available_date = datetime.datetime.strptime(args['available_date'], "%Y-%m-%d")
                    entity_query = entity_query.join(LocalAdvisorProfile, aliased=True).join(LocalAdvisorProfile.available_dates, aliased=True).filter_by(date=available_date)
                except ValueError as err:
                    return {"message" : {"available_date": format(err)}}, HTTP_BAD_REQUEST

            if(args['city_id']):
                city_id = args['city_id']
                entity_query = entity_query.join((LocalAdvisorProfile, Entity.local_advisor_profile_id == LocalAdvisorProfile.id), aliased=True).filter_by(city_id=city_id)

            if(args['keyword']):
                keyword = args['keyword']

                #The search vector should be combined together. For those tables that a user doesn't necessarily 
                #relate to (means a left join needs to be used), the coalesce function needs to be used.
                combined_search_vector = ( Entity.search_vector | func.coalesce(LocalAdvisorProfile.search_vector, u'') | func.coalesce(City.search_vector, u'') | func.coalesce(State.search_vector, u'') | func.coalesce(Country.search_vector, u'') )

                entity_query = entity_query.outerjoin((LocalAdvisorProfile, Entity.local_advisor_profile_id == LocalAdvisorProfile.id)).outerjoin(City).outerjoin(State).outerjoin(Country).filter(combined_search_vector.match(parse_search_query(keyword)))

            if(args['limit']):
                limit = args['limit']
                entity_query = entity_query.limit(limit)

            entities = entity_query.all()

            if(not entities):
                return {"message" :"No expected user found"}, HTTP_NOT_FOUND

            try:
                entity_json = entity_schema.dump(entities, many=True).data
                return entity_json
            except AttributeError as err:
                return {"message" : {"request_fields" : format(err)}}, HTTP_BAD_REQUEST

    #This route is used to create a new User(registration)
    def post(self):
        #define arguments and parse arguments
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        args = parser.parse_args()

        username = args['username']
        password = args['password']
        email = args['email']
        first_name = args['first_name']
        last_name = args['last_name']

        #Check to make sure that the given email doesn't conflict with any existing one
        existing_entity = Entity.query.filter(or_(Entity.email==email, Entity.username==username)).first()
        if(existing_entity):
            return {"message" :"Username or email already used"}, HTTP_BAD_REQUEST

        visitor_role = Role.query.filter_by(label='Visitor').first()

        if(not visitor_role):
            return {"message" : "Visitor role not found"}, HTTP_INTERNAL_SERVER_ERROR

        try:
            #Create the new entity and dump the information if success
            new_entity = Entity(username=username, password=password, email=email, first_name=first_name, last_name=last_name, role=visitor_role)

            new_entity.add(new_entity)
            entity_schema = EntitySchema(exclude=('password',))
            entity_json = entity_schema.dump(new_entity).data
        except exc.IntegrityError as err:
            return{"message" : "Failed to add use during database execution. The error message returned is: {0}".format(err)}, HTTP_BAD_REQUEST

        return entity_json

api.add_resource(Users, '/users')

class Roles(flask_restful.Resource):
    #The route is to get all possible roles of the syste
    def get(self):
        roles = Role.query.all()
        role_schema = RoleSchema()
        role_json = role_schema.dump(roles, many=True).data
        return role_json

api.add_resource(Roles, '/roles')


class Messages(flask_restful.Resource):
    #The route is to get message history between two given users.
    def get(self):
        #Get ids of two users
        parser = reqparse.RequestParser()
        parser.add_argument('bidirect_user_one', type=int, required=True)
        parser.add_argument('bidirect_user_two', type=int, required=True)
        parser.add_argument('limit', type=int, required=False)

        args = parser.parse_args()
        bidirect_user_one = args['bidirect_user_one']
        bidirect_user_two = args['bidirect_user_two']
        
        messages = Message.query.filter(or_(and_(Message.sender_id==bidirect_user_one, Message.receiver_id==bidirect_user_two), and_(Message.sender_id==bidirect_user_two, Message.receiver_id==bidirect_user_one))).order_by(Message.sent_at.desc());

        if(args['limit']):
            messages = messages.limit(args['limit'])

        message_schema = MessageSchema()
        message_json = message_schema.dump(messages, many=True).data
        #The messages need to returned in chronical order
        message_json.sort(key=lambda message:message['sent_at'])

        return message_json
    
    #The route to mark messages as read
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('messages_to_mark', type=int, action='append', required=True)
        #Since messages might be bidirectional, we only mark those whose receiver id matches the given one.
        parser.add_argument('receiver_id', type=int, required=True)
        
        args = parser.parse_args()
        messages_to_mark = args['messages_to_mark']
        receiver_id = args['receiver_id']

        for message in messages_to_mark:
            message_to_mark = Message.query.get(message)
            if(message_to_mark.receiver_id == receiver_id and not message_to_mark.read_at):
                message_to_mark.read_at = datetime.datetime.now()
                message_to_mark.update()
        
        return {"message": "messages successfully marked"}

        
api.add_resource(Messages, '/messages')

class Cities(flask_restful.Resource):
    #The route to return all city options
    def get(self):
        cities = City.query.all()
        city_schema = CitySchema()
        return city_schema.dump(cities, many=True).data

api.add_resource(Cities, '/cities')

class RecommendationCategories(flask_restful.Resource):
    #The route to return all recommendation categories options
    def get(self):
        recommendation_categories = RecommendationCategory.query.all()
        recommendation_category_schema = RecommendationCategorySchema()
        return recommendation_category_schema.dump(recommendation_categories, many=True).data

api.add_resource(RecommendationCategories, '/recommendation_categories')

class Files(flask_restful.Resource):
    #The route to push the file to the S3 and store the metadata
    def post(self):
        parser = reqparse.RequestParser()
        #The type is for file transfer
        parser.add_argument('photo', type=werkzeug.datastructures.FileStorage, location='files')

        args = parser.parse_args()
        photo = args['photo']
        #Removed the postfix
        photo_basename = photo.filename.rsplit('.', 1)[0]
        #Get the file type
        photo_ext = photo.filename.rsplit('.', 1)[1]

        #Recompose filename to include current datetime
        photo_filename = '{0}_{1}.{2}'.format(photo_basename, datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'), photo_ext)
        photo_tmp_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        #Store the photo to the temp file path
        photo.save(photo_tmp_path)

        upload_error = None
        try:
            #Push the file to the S3 repo
            s3_helper = S3Helper()
            s3_helper.upload_file(photo_tmp_path, photo_filename)
        except:
            upload_error = True
        finally:
            #Remove the temporary file no matter how
            os.remove(photo_tmp_path)

        if(upload_error):
            return {"message" : "Failed to upload profile picture"}, HTTP_INTERNAL_SERVER_ERROR

        #Compose the file url
        photo_s3_url = 'https://s3.amazonaws.com/hairydolphins/{0}'.format(photo_filename)
        photo_file = File(name = photo_filename, checksum = 0, download_link = photo_s3_url, file_type_id = 1)
        #Save the file metadata to the database
        photo_file.add(photo_file)
        file_schema = FileSchema()

        return file_schema.dump(photo_file).data
        
api.add_resource(Files, '/files')

class Reviews(flask_restful.Resource):
    #The route to post a new review of a recommendation or a local advisor
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('content', type=str, required=True)
        parser.add_argument('rating', type=str, required=True)
        parser.add_argument('reviewer_id', type=int, required=True)
        parser.add_argument('local_advisor_profile_id', type=int)
        parser.add_argument('recommendation_id', type=int)
        args = parser.parse_args()

        title = args['title']
        content = args['content']
        rating = args['rating']
        reviewer_id = args['reviewer_id']
        local_advisor_profile_id = args['local_advisor_profile_id']
        recommendation_id = args['recommendation_id']

        #If the review is for a local advisor, we should make sure this user has not previous review on this local advisor
        if(local_advisor_profile_id):
            existing_local_advisor_review = Review.query.filter(and_(Review.local_advisor_profile_id==local_advisor_profile_id, Review.reviewer_id==reviewer_id)).first()
            if(existing_local_advisor_review):
                return {"message" :"You cannot twice on the same local advisor."}, HTTP_BAD_REQUEST

        #If the review is for a recommendation, we should make sure this user has not previous review on this recommendation
        if(recommendation_id):
            existing_recommendation_review = Review.query.filter(and_(Review.recommendation_id==recommendation_id, Review.reviewer_id==reviewer_id)).first()
            if(existing_recommendation_review):
                return {"message" :"You cannot twice on the same recommendation."}, HTTP_BAD_REQUEST

        try:
            #Save the review in the database and return the data in JSON format
            new_review = Review(title=title, content=content, rating=rating, reviewer_id=reviewer_id, recommendation_id=recommendation_id, local_advisor_profile_id=local_advisor_profile_id)

            new_review.add(new_review)

            review_schema = ReviewSchema()
            review_json = review_schema.dump(new_review).data
        except exc.IntegrityError as err:
            return{"message" : "Failed to add review during database execution. The error message returned is: {0}".format(err)}, HTTP_BAD_REQUEST

        return review_json 

api.add_resource(Reviews, '/reviews')

class EntityRecommendations(flask_restful.Resource):
    #This route is to allow a user to recommendate a existing recommendation
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('recommendation_id', type=int, required=True)
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('reason', type=str)
        args = parser.parse_args()

        recommendation_id = args['recommendation_id']
        entity_id = args['user_id']
        reason = args['reason']

        #Make sure that the recommender has not recommended this recommendation before
        existing_entity_recommendation = EntityRecommendation.query.join(Recommendation).filter(and_(EntityRecommendation.recommendation_id==recommendation_id, and_(EntityRecommendation.entity_id==entity_id, Recommendation.recommender_id==entity_id))).first()

        if(existing_entity_recommendation):
            return {"message" :"You have already recommended this place!"}, HTTP_BAD_REQUEST

        try:
            #Save the new entity recommendation to the database and returns data in JSON
            new_entity_recommendation = EntityRecommendation(entity_id=entity_id, recommendation_id=recommendation_id, reason=reason)

            new_entity_recommendation.add(new_entity_recommendation)

            entity_recommendation_schema = EntityRecommendationSchema()
            entity_recommendation_json = entity_recommendation_schema.dump(new_entity_recommendation).data
        except exc.IntegrityError as err:
            return{"message" : "Failed to add entity_recommendation during database execution. The error message returned is: {0}".format(err)}, HTTP_BAD_REQUEST

        return entity_recommendation_json 

api.add_resource(EntityRecommendations, '/entity_recommendations')

class LocalAdvisorProfileRecommendations(flask_restful.Resource):
    #This route allows a local advisor to claim that he/she can provide services of certain recommendation
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('recommendation_id', type=int, required=True)
        parser.add_argument('user_id', type=int, required=True)
        args = parser.parse_args()

        recommendation_id = args['recommendation_id']
        entity_id = args['user_id']

        try:
            #Post the local advisor recommendation.
            recommendation = Recommendation.query.get(recommendation_id)
            local_advisor_profile = Entity.query.get(entity_id).local_advisor_profile
            #This is how we add the local advisor to the list through appending on the corresponding relationship
            recommendation.local_advisor_profiles.append(local_advisor_profile)
            recommendation.update()

            local_advisor_profile_schema = LocalAdvisorProfileSchema()
            local_advisor_profile_json = local_advisor_profile_schema.dump(local_advisor_profile).data
        except exc.IntegrityError as err:
            return{"message" : "Failed to add entity_recommendation during database execution. The error message returned is: {0}".format(err)}, HTTP_BAD_REQUEST

        #Notice that we return the local advisor's profile here for the front end to add the local advisor to the list
        return local_advisor_profile_json 

api.add_resource(LocalAdvisorProfileRecommendations, '/local_advisor_profile_recommendations')
