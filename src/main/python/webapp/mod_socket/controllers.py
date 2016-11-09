from flask import Blueprint, Flask, request
from flask_login import current_user
from flask_socketio import SocketIO, join_room, leave_room, send
from utils import ChatroomTable, MessageWrapper
import time

from .. import app, socketio
from ..models.models import Message

mod_socket = Blueprint('socket', __name__)

chatroom_table = ChatroomTable.get_instance()

@socketio.on('send message')
def handle_send_message(data):
    room_id = data.get('room')
    msg = MessageWrapper(
        body=data.get('body'),
        sender=data.get('sender'),
        room_id = room_id,
        receiver=data.get('receiver'))
    msg.save_to_db()
    send(msg.get_dict(), room=room_id)

@socketio.on('join')
def on_join(data):
    if current_user.is_authenticated:
        room_id = str(max(data.get('currentUser'), data.get('targetUser'))) \
            + str(min(data.get('currentUser'), data.get('targetUser'))) + str(int(time.time() * 100))
        join_room(room_id)
        chatroom_table.add_room(current_user.id, room_id)
        msg = MessageWrapper(body='user %s has entered chatroom %s'%(current_user.username, room_id), room_id=room_id)
        print 'user %s has entered chatroom %s'%(current_user.username, room_id)
        send(msg.get_dict(), room=room_id)
        return room_id

@socketio.on('connect')
def test_connect():
    if current_user.is_authenticated:
        print "The session id for %s is %s"%(current_user.username, request.sid)
