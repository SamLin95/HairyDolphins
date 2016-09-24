from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify
from webapp import login_manager
from flask_login import login_required, login_user, logout_user, current_user, login_url
from ..models.models import Entity
from ..models.schemas import EntitySchema


mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route('/', methods=['POST', 'GET'])
def test():
	return "This is authentication route"

@mod_auth.route("/signin", methods = ["POST","GET"])
def sign_in():
    username = str(request.args["username"])
    password = str(request.args["password"])
    next_page = request.values.get("next", "/")

    user = Entity.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message" : "Incorrect username or password"}), 400

    match = user.password == password
    if match:
        result = login_user(user)
        entity_schema = EntitySchema(only=("id", "first_name", "last_name"))
        return  jsonify(entity_schema.dump(user).data)
    else:
        return jsonify({"message" : "Incorrect username or password"}), 400

@mod_auth.route("/logout", methods = ["GET"])
def sign_out():
    logout_user()
    session.clear()
    return redirect("/")

@mod_auth.route("/current_user", methods = ["GET"])
def get_current_user():
    if(current_user.get_id()):
        entity_schema = EntitySchema(only=("id", "first_name", "last_name"))
        return  jsonify(entity_schema.dump(current_user).data)
    else:
        return jsonify({"message" : "User not logged in"}), 401

@login_manager.user_loader
def load_user(id):
    user = Entity.query.filter_by(id=id).first()
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return "unauthorized"



