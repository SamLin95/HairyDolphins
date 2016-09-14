from flask import Blueprint, request, render_template, redirect, url_for, Flask, jsonify
import flask_restful

from ..models.models import *

API_VERSION = 1

mod_api = Blueprint('api', __name__, url_prefix='/api')
api = flask_restful.Api(mod_api)

class HelloWorld(flask_restful.Resource):
    def get(self):
        r = Role.query.filter_by(id=1).first()
        return {
            "data" : r.label
        }

api.add_resource(HelloWorld, '/helloworld')
