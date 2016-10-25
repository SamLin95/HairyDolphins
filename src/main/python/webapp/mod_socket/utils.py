__author__ = 'slin'
from ..models.models import Message, db

class ChatroomTable(object):
    INSTANCE = None

    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("You can only instantiate this table once")
        self.table = {}
        self.room_count = 0

    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = ChatroomTable()
        return cls.INSTANCE

    def add_room(self, user_id, room_id):
        if self.table.get(str(user_id)) is None:
            self.table[str(user_id)] = [room_id]
        else:
            self.table[str(user_id)].append(room_id)
        self.room_count += 1

    def leave_room(self, user_id, room_id):
        try:
            self.table.get(str(user_id)).remove(room_id)
            self.room_count -= 1
        except ValueError:
            print "user %s does not have a room yet"%(user_id)
            return

    def clear_user_rooms(self, user_id):
        if self.table.get(str(user_id)) is None:
            return
        self.room_count -= len(self.table.get(user_id))
        self.table[user_id] = None


class MessageWrapper(object):
    def __init__(self, body, room_id, sender=None,receiver=None, type="boardcast"):
        self._body = body
        self._room_id = room_id
        self._sender = sender
        self._receiver = receiver
        self._type = type

    def get_dict(self):
        return {'sender': self._sender, 'type': self._type, 'receiver': self._receiver,
            'body' : self._body, 'room': self._room_id}

    def save_to_db(self):
        if self._sender is not None:
            msg = Message(message_body=self._body, sender_id=self._sender,
                receiver_id=self._receiver)
            db.session.add(msg)
            db.session.commit()
        else:
            print "broadcast message not saved"
