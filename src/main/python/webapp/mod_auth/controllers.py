from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify
from webapp import login_manager
from flask_login import login_required, login_user, logout_user, current_user, login_url
from ..models.models import Entity
from ..models.schemas import EntitySchema
from ..mod_socket.utils import ChatroomTable

#Makes the module a Blueprint object.
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

#The route to compare username and password provided and sign in the user.
@mod_auth.route("/signin", methods = ["POST","GET"])
def sign_in():
    username = str(request.args["username"])
    password = str(request.args["password"])
    next_page = request.values.get("next", "/")

    #Look for the user by username
    user = Entity.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message" : "Incorrect username or password"}), 400

    #Compare the password
    match = user.password == password

    if match:
        #Login the user in backend and return the basic infomration of the user.
        result = login_user(user)
        entity_schema = EntitySchema(only=("id", "first_name", "last_name", "email", "username", "birthday", "phone_number", "profile_photo_url", "role"))
        return  jsonify(entity_schema.dump(user).data)
    else:
        return jsonify({"message" : "Incorrect username or password"}), 400

#The route to signout the current logged in user.
@mod_auth.route("/logout", methods = ["GET"])
def sign_out():
    #If the user is in the chat room, the system needs to force the user to leave.
    ChatroomTable.get_instance().leave_room(str(current_user.id))

    #Logout the current user and clear the session
    logout_user()
    session.clear()

    return redirect("/")

#Return the current logged in user for persistent login checking in the FE
@mod_auth.route("/current_user", methods = ["GET"])
def get_current_user():
    if(current_user.get_id()):
        entity_schema = EntitySchema(only=("id", "first_name", "last_name", "email", "username", "birthday", "phone_number", "profile_photo_url", "role"))
        return  jsonify(entity_schema.dump(current_user).data)
    else:
        return jsonify({"message" : "User not logged in"}), 401

#The required route of Flask-Login module to load the current user by id.
@login_manager.user_loader
def load_user(id):
    #Since we used the primary index of Entity table as the id, we need to compare ids here.
    user = Entity.query.filter_by(id=id).first()
    return user

#Required function. Reserved for strict authorization policy in the future.
@login_manager.unauthorized_handler
def unauthorized():
    return "unauthorized"



