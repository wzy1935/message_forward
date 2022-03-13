from flask import Flask, request
from data import MessageService, Message

app = Flask(__name__)
ms = MessageService()

@app.route('/')
def hello():
    print('yes')
    return '?'


@app.route('/message',methods=["POST"])
def get_message():
    if request.method == 'POST':
        token = request.form['token']
        message = request.form['text']
        if token == 'x123456':
            pass
    return 'done.'


@app.route('/message/list',methods=["POST"])
def list():
    if request.method == 'POST':
        token = request.form['token']
        message = request.form['text']
        if token == 'x123456':
            pass
    return 'done.'


app.run(port=8082, host='0.0.0.0')