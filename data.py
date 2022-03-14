import sqlite3
import time
import copy

class Message:
    def __init__(self, title, content, time, id=None, user=None, user_name=None):
        self.id = id
        self.title = title
        self.content = content
        self.time = time
        self.user = user
        self.user_name = user_name

    def __str__(self):
        return f'({self.id}, {self.title}, {self.content})'

    def to_tuple(self):
        return (self.id, self.title, self.content, self.time, self.user, self.user_name)

    def to_map(self):
        m = {}
        m['id'] = self.id
        m['title'] = self.title
        m['content'] = self.content
        m['time'] = self.time
        if self.user is not None: m['user'] = self.user
        if self.user_name is not None: m['user_name'] = self.user_name
        return m

    @staticmethod
    def from_tuple(tuple):
        return Message(tuple[1], tuple[2], tuple[3], tuple[0], tuple[4], tuple[5])


class MessageService:
    def __init__(self):
        self.conn = sqlite3.connect('message.db', check_same_thread=False)

    def drop(self):
        with self.conn as conn:
            conn.execute('drop table message;')

    def init(self):
        with self.conn as conn:
            conn.execute('create table message ('
                         'id integer primary key autoincrement, '
                         'title text not null, '
                         'content text not null, '
                         'time int not null, '
                         'user text, '
                         'user_name text);')

    def add(self, message: Message):
        with self.conn as conn:
            message = copy.copy(message)
            message.id = None
            conn.execute('insert into message (id, title, content, time, user, user_name) values (?,?,?,?,?,?);',
                         message.to_tuple())

    def get(self, id):
        with self.conn as conn:
            rows = conn.execute(f'select id, title, content, time, user, user_name from message where id = {id};')
            data = None
            for r in rows: data = r
            return None if data is None else Message.from_tuple(data)

    def remove(self, id):
        if self.get(id) is not None:
            with self.conn as conn:
                conn.execute(f'delete from message where id = {id}')

    def list(self, limit, offset):
        with self.conn as conn:
            output = []
            datas = conn.execute(f'select id, title, content, time, user, user_name from message '
                                f'order by time desc limit {limit} offset {offset}')
            for data in datas:
                output.append(Message.from_tuple(data))
            return output

    def count(self):
        with self.conn as conn:
            cnt, = conn.execute('select count(*) from message;')
            return cnt[0]