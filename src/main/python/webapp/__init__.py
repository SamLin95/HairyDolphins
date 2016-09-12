from flask import Flask, request, url_for

app = Flask(__name__)
app.config.from_object('config')

from mod_user.controllers import mod_user as user_module
app.register_blueprint(user_module)

from mod_search.controllers import mod_search as search_module
app.register_blueprint(search_module)

from mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module)

@app.route("/", methods=["GET", "POST"])
def index():
	return "Hello Word!"