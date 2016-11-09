__author__ = 'slin'
from ..models.models import Message, db
import datetime
class ChatroomTable(object):
    INSTANCE = None

    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("You can only instantiate this table once")
        self.table = {}
        self.reverse_table = {}
        self.room_count = 0

    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = ChatroomTable()
        return cls.INSTANCE

    def join_to_room(self, user_id, room_id):
        cur_room = self.table.get(user_id)
        # Users in old room.
        if cur_room is not None:
            old_users = self.reverse_table.get(cur_room)
            if old_users is not None and user_id in old_users:
                # Remove user from old chat room.
                old_users.remove(user_id)
            # users in current room.
        cur_users = self.reverse_table.get(room_id)
        if cur_users is None:
            self.reverse_table[room_id] = []
            self.reverse_table[room_id].append(user_id)
        elif user_id not in cur_users:
            cur_users.append(user_id)
        self.table[user_id] = room_id

    def leave_room(self, user_id):
        room_id = self.table.get(user_id)
        if room_id is not None:
            self.table[user_id] = None
            if self.reverse_table.get(room_id) is not None and user_id in self.reverse_table.get(room_id):
                self.reverse_table[room_id].remove(user_id)

    def is_in_room(self, user_id, room_id):
        return self.table.get(user_id) is room_id

    def get_current_room(self, user_id):
        return self.table[user_id]

class MessageWrapper(object):
    BOARDCAST_TYPE = "boardcast"
    MESSAGE_TYPE = "msg"
    OFFLINE_TYPE = "offline"
    def __init__(self, body, room_id, sender=None,receiver=None, type=BOARDCAST_TYPE):
        self._body = body
        self._room_id = room_id
        self._sender = sender
        self._receiver = receiver
        self._type = type

    def get_dict(self):
        return {'sender': self._sender, 'type': self._type, 'receiver': self._receiver,
            'body' : self._body, 'room': self._room_id}

    def save_to_db(self):
        if self._type is MessageWrapper.MESSAGE_TYPE:
            msg = Message(message_body=self._body, sender_id=self._sender,
                receiver_id=self._receiver, read_at=datetime.datetime.now)
            db.session.add(msg)
            db.session.commit()
        elif self._type is MessageWrapper.OFFLINE_TYPE:
            msg = Message(message_body=self._body, sender_id=self._sender,
                receiver_id=self._receiver)
            db.session.add(msg)
            db.session.commit()
        elif self._type is MessageWrapper.BOARDCAST_TYPE:
            print "broadcast message is not saved."

if __name__ == "__main__":
    ct = ChatroomTable.get_instance()
    user1 = 'sam'
    user2 = 'billy'
    user3 = "dick"
    room1 = 1
    room2 = 2
    room3 = 3
    ct.join_to_room(user1, room1)
    ct.join_to_room(user2, room2)
    ct.join_to_room(user1, room1)
    ct.join_to_room(user1, room1)
    ct.join_to_room(user1, room1)
    ct.join_to_room(user1, room1)
    ct.join_to_room(user1, room2)
    ct.join_to_room(user2, room1)
    ct.join_to_room(user3, room3)
    ct.join_to_room(user3, room1)
    ct.join_to_room(user2, room1)
    print ct.table
    print ct.reverse_table
