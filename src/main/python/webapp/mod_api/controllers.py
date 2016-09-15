from flask import Blueprint, request, render_template, redirect, url_for, Flask, jsonify
import flask_restful

from ..models.models import *
from ..models.schemas import *

API_VERSION = 1

mod_api = Blueprint('api', __name__, url_prefix='/api')
api = flask_restful.Api(mod_api)

class HelloWorld(flask_restful.Resource):
    def get(self):
        entity = Entity.query.all()
        entity_schema = EntitySchema()
        entity_json = entity_schema.dump(entity, many=True).data
        return entity_json

api.add_resource(HelloWorld, '/users')
