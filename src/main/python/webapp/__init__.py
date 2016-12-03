from flask import Flask, request, url_for, send_file
from flask_triangle import Triangle
from flask_socketio import SocketIO
from flask_login import LoginManager, current_user

#Initialize the application
app = Flask(__name__, static_path='/static')
app.config.from_object('config')

#Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)

#Initialize the SocketIO module
socketio = SocketIO()
socketio.init_app(app)

#The Blueprint registration of each module.
from mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module)

from mod_api.controllers import mod_api as api_module
app.register_blueprint(api_module)

from mod_socket.controllers import mod_socket as socket_module
app.register_blueprint(socket_module)

#To avoid conflict between Jinja2 template and AngularJS templates
Triangle(app)

#Return the index page.
@app.route("/", methods=["GET", "POST"])
def index():
    return send_file('templates/index.html')

#Run application through SocketIO's given approach
if __name__ == '__main__':
    socketio.run(app)
