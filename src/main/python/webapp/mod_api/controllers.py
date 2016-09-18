from flask import Blueprint, request, render_template, redirect, url_for, Flask, jsonify
import flask_restful
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
api = swagger.docs(flask_restful.Api(mod_api), apiVersion=API_VERSION, api_spec_url='/spec')

class User(flask_restful.Resource):
    "An User"

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

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('role_id', type=int)
        parser.add_argument('available_date', type=str)
        parser.add_argument('keyword', type=str)
        parser.add_argument('limit', type=int)
        parser.add_argument('request_fields', type=str, action='append')

        self.parser = parser

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
        args = self.parser.parse_args()
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

                print str(entity_query)

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

api.add_resource(Users, '/users')

class Roles(flask_restful.Resource):
    def get(self):
        roles = Role.query.all()
        role_schema = RoleSchema()
        role_json = role_schema.dump(roles, many=True).data
        return role_json

api.add_resource(Roles, '/roles')
