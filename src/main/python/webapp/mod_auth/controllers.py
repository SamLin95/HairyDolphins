from flask import Blueprint, request, render_template, redirect, url_for
from webapp import login_manager
from flask_login import login_required, login_user, logout_user, current_user, login_url
from ..models.models import Entity


mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route('/', methods=['POST', 'GET'])
def test():
	return "This is authentication route"

@mod_auth.route("/signin", methods = ["POST", "GET"])
def signin_page():
    if request.method == "GET":
        #return render_template("login.html")
        return "loginPage"

    username = str(request.form["username"])
    password = str(request.form["password"])
    next_page = request.values.get("next", "/")
    match = True
    """TODO: add authentication logic here"""
    if match:
        login_user(Entity.query.filter_by(username=username).first())
        #return redirect(next_page)
        return "logged in"
    else:
        #return render_template("login.html", errMes = "Login Failed, Please try again")
        return "login fail"

@mod_auth.route("/logout")
def sign_out():
    logout_user()
    session.clear()
    return redirect("/")

@login_manager.user_loader
def load_user(id):
    user = Entity.query.filter_by(username=id).first()
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return "unauthorized"



