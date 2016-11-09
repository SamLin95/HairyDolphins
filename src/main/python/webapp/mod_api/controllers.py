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

mod_api = Blueprint('api', __name__, url_prefix='/api')
api = flask_restful.Api()
"""Calling init_app can defer for Blueprint object"""
api.init_app(mod_api)
api = swagger.docs(api, apiVersion=API_VERSION, api_spec_url='/spec')

class Recommendations(flask_restful.Resource):
    "A list of recommendations"

    @swagger.operation(
        summary = "Returns the information of a list of recommendations which meet all given criteria",
        nickname = "Search Recommendatons",
        parameters=[
            {
              "name": "recommendation_id",
              "description": "Primary key of the expected recommendation. Cannot put retriction on any other fields of a recommendation if this parameter is being used",
              "required": False,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "query"
            },
            {
              "name": "recommendation_category_id",
              "description": "The primary key of the category of recommendations in the expected recommendation list",
              "required": False,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "query"
            },
            {
              "name": "city_id",
              "description": "The primary key of city that the recommendationthat belongs to",
              "required": False,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
            {
              "name": "request_fields",
              "description": "Names of the fields of each recommendation that are required to be returned",
              "required": False,
              "allowMultiple": True,
              "dataType": "string",
              "paramType": "query"
            },
       ]
    )
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('recommendation_id', type=int)
        parser.add_argument('recommendation_category_id', type=int)
        parser.add_argument('city_id', type=int)
        parser.add_argument('limit', type=int)
        parser.add_argument('request_fields', type=str, action='append')
        args = parser.parse_args()
        recommendation_query = Recommendation.query

        if(args['request_fields']):
            request_fields = tuple(args['request_fields'])
            recommendation_schema = RecommendationSchema(only=request_fields)
        else:
            recommendation_schema = RecommendationSchema()

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

            if(not recommendations):
                return {"message" :"No expected recommendation found"}, HTTP_NOT_FOUND

            try:
                recommendation_json = recommendation_schema.dump(recommendations, many=True).data
                return recommendation_json
            except AttributeError as err:
                return {"message" : {"request_fields" : format(err)}}, HTTP_BAD_REQUEST

    def post(self):
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
            new_recommendation = Recommendation(title=title, description=description, address_line_one=address_line_one, address_line_two=address_line_two, zip_code=zip_code, recommender_id=recommender_id, city_id=city_id, recommendation_category_id=recommendation_category_id,is_draft=False)

            new_recommendation.add(new_recommendation)

            new_recommendation_photo = RecommendationPhoto(recommendation=new_recommendation, file_id=file_id, uploader_id=recommender_id)
            new_recommendation_photo.add(new_recommendation_photo)

            recommendation_schema = RecommendationSchema()
            recommendation_json = recommendation_schema.dump(new_recommendation).data
        except exc.IntegrityError as err:
            return{"message" : "Failed to add recommendation during database execution. The error message returned is: {0}".format(err)}, HTTP_BAD_REQUEST

        return recommendation_json 

api.add_resource(Recommendations, '/recommendations')

class RecommendationResource(flask_restful.Resource):
    """A Recommendation"""

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('request_fields', type=str, action='append')

        self.parser = parser

    @swagger.operation(
        summary = "Returns the information of the recommendation with given id",
        nickname = "Get Recommendation",
        parameters=[
            {
              "name": "recommendation_id",
              "description": "Primary key of the expected recommendation.",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            },
            {
              "name": "request_fields",
              "description": "Names of the fields of the recommnendation that are required to be returned",
              "required": False,
              "allowMultiple": True,
              "dataType": "string",
              "paramType": "query"
            },
       ]
    )
    def get(self, recommendation_id):
        args = self.parser.parse_args()
        recommendation_query = Recommendation.query

        if(args['request_fields']):
            request_fields = tuple(args['request_fields'])
            recommendation_schema = RecommendationSchema(only=request_fields)
        else:
            recommendation_schema = RecommendationSchema()

        recommendation = recommendation_query.get(recommendation_id)

        if(not recommendation):
            return {"message" :"Recommendation not found"}, HTTP_NOT_FOUND

        try:
            recommendation_json = recommendation_schema.dump(recommendation).data
            return recommendation_json
        except AttributeError as err:
            return {"message" : {"request_fields" : format(err)} }, HTTP_BAD_REQUEST

api.add_resource(RecommendationResource, '/recommendations/<int:recommendation_id>')

class User(flask_restful.Resource):
    """An User"""

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('request_fields', type=str, action='append')

        self.parser = parser

    @swagger.operation(
        summary = "Returns the information of the user with given id",
        nickname = "Get User",
        parameters=[
            {
              "name": "user_id",
              "description": "Primary key of the expected user.",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            },
            {
              "name": "request_fields",
              "description": "Names of the fields of the user that are required to be returned",
              "required": False,
              "allowMultiple": True,
              "dataType": "string",
              "paramType": "query"
            },
       ]
    )
    def get(self, user_id):
        args = self.parser.parse_args()
        entity_query = Entity.query

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

    def put(self, user_id):
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

        existing_entity = Entity.query.filter(and_(Entity.email==email, Entity.id!=user_id)).first()
        if(existing_entity):
            return {"message" :"Email already used"}, HTTP_BAD_REQUEST

        try:
            entity = Entity.query.get(user_id)

            entity.email = email
            entity.first_name = first_name
            entity.last_name = last_name
            entity.phone_number = phone_number
            birthday= datetime.datetime.strptime(args['birthday'], "%Y-%m-%d")
            birthday_date = Date.query.filter(Date.date==birthday).first()
            if(not birthday_date):
                birthday_date = Date(date=birthday)
                birthday_date.add(birthday_date)
    
            entity.birthday = birthday_date
            print entity.birthday

            if(file_id):
                old_profile_picture = EntityPhoto.query.filter(and_(EntityPhoto.entity_id==user_id, EntityPhoto.is_profile_picture==True)).first()
                if(old_profile_picture):
                    old_profile_picture.is_profile_picture = False
                    old_profile_picture.update()

                entity_photo = EntityPhoto(file_id=file_id, entity_id=user_id, is_profile_picture=True)
                entity_photo.add(entity_photo)

            entity.update()

            entity_schema = EntitySchema(only=("id", "first_name", "last_name", "email", "username",     "birthday", "phone_number", "profile_photo_url", "role"))
            entity_json = entity_schema.dump(entity).data
        except exc.IntegrityError as err:
            return{"message" : "Failed to add use during database execution. The error message returned is: {0}".format(err)}, HTTP_BAD_REQUEST
        except ValueError as err:
             return {"message" : {"birthday": format(err)}}, HTTP_BAD_REQUEST

        return entity_json

api.add_resource(User, '/users/<int:user_id>')

class Users(flask_restful.Resource):
    "A list of users"

    @swagger.operation(
        summary = "Returns the information of a list of users which meet all given criteria",
        nickname = "Search Users",
        parameters=[
            {
              "name": "user_id",
              "description": "Primary key of the expected user. Cannot put retriction on any other fields of a user if this parameter is being used",
              "required": False,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "query"
            },
            {
              "name": "role_id",
              "description": "The primary key of the role of users in the expected user list",
              "required": False,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "query"
            },
            {
              "name": "available_date",
              "description": "The expected avaialble date of local advisors that are required to be returned",
              "required": False,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
            {
              "name": "keyword",
              "description": "Keyword related to the users (can be user's username, first_name, last_name, description as a local advisor, city, state, or the country the user belongs to or any combination of them) that are required to be returned",
              "required": False,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
            {
              "name": "request_fields",
              "description": "Names of the fields of each user that are required to be returned",
              "required": False,
              "allowMultiple": True,
              "dataType": "string",
              "paramType": "query"
            },
       ]
    )
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('role_id', type=int)
        parser.add_argument('city_id', type=int)
        parser.add_argument('available_date', type=str)
        parser.add_argument('keyword', type=str)
        parser.add_argument('limit', type=int)
        parser.add_argument('request_fields', type=str, action='append')
        args = parser.parse_args()
        entity_query = Entity.query

        if(args['request_fields']):
            request_fields = tuple(args['request_fields'])
            entity_schema = EntitySchema(exclude=('password',), only=request_fields)
        else:
            entity_schema = EntitySchema(exclude=('password',))

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
                entity_query = entity_query.join(LocalAdvisorProfile, aliased=True).filter_by(city_id=city_id)

            if(args['keyword']):
                keyword = args['keyword']

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

    @swagger.operation(
        summary = "Create a new User",
        nickname = "Create User",
        parameters=[
            {
              "name": "username",
              "description": "The username of the user to be created",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
            {
              "name": "password",
              "description": "The password of the user to be created",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
            {
              "name": "email",
              "description": "The email of the user to be created",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
            {
              "name": "first_name",
              "description" : "The first name of the user to be created",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
            {
              "name": "last_name",
              "description" : "The last name of the user to be created",
              "required": True,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
       ]
    )
    def post(self):
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

        existing_entity = Entity.query.filter(or_(Entity.email==email, Entity.username==username)).first()
        if(existing_entity):
            return {"message" :"Username or email already used"}, HTTP_BAD_REQUEST

        visitor_role = Role.query.filter_by(label='Visitor').first()

        if(not visitor_role):
            return {"message" : "Visitor role not found"}, HTTP_INTERNAL_SERVER_ERROR

        try:
            new_entity = Entity(username=username, password=password, email=email, first_name=first_name, last_name=last_name, role=visitor_role)

            new_entity.add(new_entity)
            entity_schema = EntitySchema(exclude=('password',))
            entity_json = entity_schema.dump(new_entity).data
        except exc.IntegrityError as err:
            return{"message" : "Failed to add use during database execution. The error message returned is: {0}".format(err)}, HTTP_BAD_REQUEST

        return entity_json

api.add_resource(Users, '/users')

class Roles(flask_restful.Resource):
    def get(self):
        roles = Role.query.all()
        role_schema = RoleSchema()
        role_json = role_schema.dump(roles, many=True).data
        return role_json

api.add_resource(Roles, '/roles')


class Messages(flask_restful.Resource):
    def get(self):
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
        message_json.sort(key=lambda message:message['sent_at'])

        return message_json
    
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('messages_to_mark', type=int, action='append', required=True)
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
    def get(self):
        cities = City.query.all()
        city_schema = CitySchema()
        return city_schema.dump(cities, many=True).data

api.add_resource(Cities, '/cities')

class RecommendationCategories(flask_restful.Resource):
    def get(self):
        recommendation_categories = RecommendationCategory.query.all()
        recommendation_category_schema = RecommendationCategorySchema()
        return recommendation_category_schema.dump(recommendation_categories, many=True).data

api.add_resource(RecommendationCategories, '/recommendation_categories')

class Files(flask_restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('photo', type=werkzeug.datastructures.FileStorage, location='files')

        args = parser.parse_args()
        photo = args['photo']
        photo_basename = photo.filename.rsplit('.', 1)[0]
        photo_ext = photo.filename.rsplit('.', 1)[1]

        #Recompose filename to include current datetime
        photo_filename = '{0}_{1}.{2}'.format(photo_basename, datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'), photo_ext)
        photo_tmp_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo.save(photo_tmp_path)

        upload_error = None
        try:
            s3_helper = S3Helper()
            s3_helper.upload_file(photo_tmp_path, photo_filename)
        except:
            upload_error = True
        finally:
            os.remove(photo_tmp_path)

        if(upload_error):
            return {"message" : "Failed to upload profile picture"}, HTTP_INTERNAL_SERVER_ERROR

        photo_s3_url = 'https://s3.amazonaws.com/hairydolphins/{0}'.format(photo_filename)
        photo_file = File(name = photo_filename, checksum = 0, download_link = photo_s3_url, file_type_id = 1)
        photo_file.add(photo_file)
        file_schema = FileSchema()

        return file_schema.dump(photo_file).data
        
api.add_resource(Files, '/files')

class Reviews(flask_restful.Resource):
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

        if(local_advisor_profile_id):
            existing_local_advisor_review = Review.query.filter(and_(Review.local_advisor_profile_id==local_advisor_profile_id, Review.reviewer_id==reviewer_id)).first()
            if(existing_local_advisor_review):
                return {"message" :"You cannot twice on the same local advisor."}, HTTP_BAD_REQUEST

        if(recommendation_id):
            existing_recommendation_review = Review.query.filter(and_(Review.recommendation_id==recommendation_id, Review.reviewer_id==reviewer_id)).first()
            if(existing_recommendation_review):
                return {"message" :"You cannot twice on the same recommendation."}, HTTP_BAD_REQUEST

        try:
            new_review = Review(title=title, content=content, rating=rating, reviewer_id=reviewer_id, recommendation_id=recommendation_id, local_advisor_profile_id=local_advisor_profile_id)

            new_review.add(new_review)

            review_schema = ReviewSchema()
            review_json = review_schema.dump(new_review).data
        except exc.IntegrityError as err:
            return{"message" : "Failed to add review during database execution. The error message returned is: {0}".format(err)}, HTTP_BAD_REQUEST

        return review_json 

api.add_resource(Reviews, '/reviews')

class EntityRecommendations(flask_restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('recommendation_id', type=int, required=True)
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('reason', type=str)
        args = parser.parse_args()

        recommendation_id = args['recommendation_id']
        entity_id = args['user_id']
        reason = args['reason']

        existing_entity_recommendation = EntityRecommendation.query.join(Recommendation).filter(and_(EntityRecommendation.recommendation_id==recommendation_id, and_(EntityRecommendation.entity_id==entity_id, Recommendation.recommender_id==entity_id))).first()

        if(existing_entity_recommendation):
            return {"message" :"You have already recommended this place!"}, HTTP_BAD_REQUEST

        try:
            new_entity_recommendation = EntityRecommendation(entity_id=entity_id, recommendation_id=recommendation_id, reason=reason)

            new_entity_recommendation.add(new_entity_recommendation)

            entity_recommendation_schema = EntityRecommendationSchema()
            entity_recommendation_json = entity_recommendation_schema.dump(new_entity_recommendation).data
        except exc.IntegrityError as err:
            return{"message" : "Failed to add entity_recommendation during database execution. The error message returned is: {0}".format(err)}, HTTP_BAD_REQUEST

        return entity_recommendation_json 

api.add_resource(EntityRecommendations, '/entity_recommendations')

class LocalAdvisorProfileRecommendations(flask_restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('recommendation_id', type=int, required=True)
        parser.add_argument('user_id', type=int, required=True)
        args = parser.parse_args()

        recommendation_id = args['recommendation_id']
        entity_id = args['user_id']

        try:
            recommendation = Recommendation.query.get(recommendation_id)
            local_advisor_profile = Entity.query.get(entity_id).local_advisor_profile
            recommendation.local_advisor_profiles.append(local_advisor_profile)
            recommendation.update()

            local_advisor_profile_schema = LocalAdvisorProfileSchema()
            local_advisor_profile_json = local_advisor_profile_schema.dump(local_advisor_profile).data
        except exc.IntegrityError as err:
            return{"message" : "Failed to add entity_recommendation during database execution. The error message returned is: {0}".format(err)}, HTTP_BAD_REQUEST

        return local_advisor_profile_json 

api.add_resource(LocalAdvisorProfileRecommendations, '/local_advisor_profile_recommendations')
