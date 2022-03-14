import time
from flask import Flask, request, jsonify
from data import MessageService, Message

app = Flask(__name__)
ms = MessageService()
password = 'x123456'

def to_timestamp(local_date, local_time):
    return int(time.mktime(time.strptime(f'{local_date} {local_time}', "%Y-%m-%d %H.%M")))

def to_time_str(timestamp):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))

@app.route('/')
def hello():
    return '<h1>Message Application</h1>'


@app.route('/recv',methods=["POST"])
def recv():
    token = request.form['token']
    content = request.form['content']
    local_date = request.form['local_date']
    local_time = request.form['local_time']
    title = request.form['title']
    user = request.form['user']
    user_name = request.form['user_name']
    if token == password:
        message = Message(title, content, to_timestamp(local_date, local_time), user=user, user_name=user_name)
        ms.add(message)
    return jsonify({'code': 0})


@app.route('/list',methods=["POST"])
def list():
    token = request.form['token']
    page = int(request.form['page']) # page should start with 1
    page_size = int(request.form['page_size'])
    if token == password:
        offset = page_size * (page - 1)
        limit = page_size
        out_list = ms.list(limit, offset)
        cnt = ms.count()
        print([x.to_map() for x in out_list])
        return jsonify({'code': 0, 'count': cnt, 'data': [x.to_map() for x in out_list]})
    else:
        return jsonify({'code': -1})



app.run(port=8082, host='0.0.0.0')