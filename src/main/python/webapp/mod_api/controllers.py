from flask import Blueprint, request, render_template, redirect, url_for, Flask, jsonify
import flask_restful

from ..models.models import *
from ..models.schemas import *

API_VERSION = 1

mod_api = Blueprint('api', __name__, url_prefix='/api')
api = flask_restful.Api(mod_api)

class GetUsers(flask_restful.Resource):
    def get(self):
        entities = Entity.query.all()
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
