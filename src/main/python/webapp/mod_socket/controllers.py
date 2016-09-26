from flask import Blueprint, Flask
from flask_socketio import SocketIO, join_room, leave_room

from .. import app, socketio
from ..models.models import Message

mod_socket = Blueprint('socket', __name__)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
