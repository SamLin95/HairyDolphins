from flask import Flask, request, url_for, render_template
from flask.ext.triangle import Triangle

app = Flask(__name__, static_path='/static')
app.config.from_object('config')

from mod_user.controllers import mod_user as user_module
app.register_blueprint(user_module)

from mod_search.controllers import mod_search as search_module
app.register_blueprint(search_module)

from mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module)

from mod_api.controllers import mod_api as api_module
app.register_blueprint(api_module)

Triangle(app)

@app.route("/", methods=["GET", "POST"])
def index():
	return render_template('index.html')
