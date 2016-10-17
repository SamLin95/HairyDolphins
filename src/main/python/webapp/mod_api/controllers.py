from flask import Blueprint, request, render_template, redirect, url_for, Flask, jsonify
import flask_restful
from sqlalchemy import and_, or_, exc
from flask_restful import reqparse
from flask_restful_swagger import swagger
from datetime import datetime
from sqlalchemy_searchable import search, parse_search_query

from ..models.models import *
from ..models.schemas import *

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

            if(args['keyword']):
                keyword = args['keyword']

                combined_search_vector = ( Entity.search_vector | LocalAdvisorProfile.search_vector | City.search_vector | State.search_vector | Country.search_vector )

                entity_query = entity_query.join((LocalAdvisorProfile, Entity.local_advisor_profile_id == LocalAdvisorProfile.id)).join(City).join(State).join(Country).filter(combined_search_vector.match(parse_search_query(keyword)))

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
