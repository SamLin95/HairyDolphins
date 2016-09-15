from flask import Blueprint, request, render_template, redirect, url_for, Flask, jsonify
import flask_restful
from flask_restful import reqparse

from ..models.models import *
from ..models.schemas import *

API_VERSION = 1

mod_api = Blueprint('api', __name__, url_prefix='/api')
api = flask_restful.Api(mod_api)

class GetUsers(flask_restful.Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('role_id', type=int)

        self.parser = parser

    def get(self):
        args = self.parser.parse_args()
        entity_query = Entity.query

        if args['user_id']:
            user_id = args['user_id']
            entity = entity_query.filter_by(id=user_id).first()
            entity_schema = EntitySchema(exclude='password')
            entity_json = entity_schema.dump(entity).data
        else:
            if(args['role_id']):
                role_id = args['role_id']
                entity_query = entity_query.filter_by(role_id=role_id)

            entities = entity_query.all()
            entity_schema = EntitySchema(exclude='password')
            entity_json = entity_schema.dump(entities, many=True).data
        return entity_json

api.add_resource(GetUsers, '/users')

class GetRoles(flask_restful.Resource):
    def get(self):
        roles = Role.query.all()
        role_schema = RoleSchema()
        role_json = role_schema.dump(roles, many=True).data
        return role_json

api.add_resource(GetRoles, '/roles')
