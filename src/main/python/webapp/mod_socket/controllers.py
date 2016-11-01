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
    global chatroom_table
    room_id = str(data.get('room')) if data.get('room') is not None else chatroom_table.get_current_room(str(data.get('sender')))
    if chatroom_table.is_in_room(data.get("receiver"), room_id):
        msg = MessageWrapper(
            body=data.get('body'),
            sender=str(data.get('sender')),
            room_id = room_id,
            type=MessageWrapper.MESSAGE_TYPE,
            receiver=data.get('receiver'))
    else:
        print "another user is not in table..."
        msg = MessageWrapper(
            body=data.get('body'),
            sender=data.get('sender'),
            room_id = room_id,
            type=MessageWrapper.OFFLINE_TYPE,
            receiver=data.get('receiver'))
    send(msg.get_dict(), room=room_id)
    msg.save_to_db()


@socketio.on('join')
def on_join(data):
    global chatroom_table
    if current_user.is_authenticated:
        current_user_id = str(data.get('currentUser'))
        target_user_id = str(data.get('targetUser'))
        print "current user is %s, target user is %s"%(current_user_id, target_user_id)

        #room id is based on two user id, so two user will always join the same room.
        room_id = str(max(current_user_id, target_user_id))  + str(min(current_user_id, target_user_id))
        join_room(room_id)
        chatroom_table.join_to_room(current_user_id, room_id)
        msg = MessageWrapper(body='user %s has entered chatroom %s'%(current_user.username, room_id), room_id=room_id)
        print 'user %s has entered chatroom %s'%(current_user.username, room_id)

        send(msg.get_dict(), room=room_id)
        return room_id

@socketio.on('connect')
def test_connect():
    if current_user.is_authenticated:
        print "The session id for %s is %s"%(current_user.username, request.sid)