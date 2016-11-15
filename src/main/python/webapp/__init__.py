from flask import Flask, request, url_for, send_file
from flask_triangle import Triangle
from flask_socketio import SocketIO
from flask_login import LoginManager, current_user

app = Flask(__name__, static_path='/static')
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)

socketio = SocketIO()
socketio.init_app(app)

from mod_user.controllers import mod_user as user_module
app.register_blueprint(user_module)

from mod_search.controllers import mod_search as search_module
app.register_blueprint(search_module)

from mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module)

from mod_api.controllers import mod_api as api_module
app.register_blueprint(api_module)

from mod_socket.controllers import mod_socket as socket_module
app.register_blueprint(socket_module)

Triangle(app)

@app.route("/", methods=["GET", "POST"])
def index():
    return send_file('templates/index.html')

if __name__ == '__main__':
    socketio.run(app)
