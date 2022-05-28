import json
import time
from datetime import datetime
import pymongo

from bson import ObjectId, json_util
from flask import Flask, request
from pymongo import MongoClient


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class Message:

    @staticmethod
    def send_message():
        pylounge = {
            'username': str(input('Введите имя пользователя:')),
            'text': str(input('Введите сообщение:'))
        }

        ins_result = collection.insert_one(pylounge)

        return ins_result

    @staticmethod
    def get_message():
        for channel in collection.find():
            print(channel['username'], channel['text'])


def connect_to_mongodb():
    client = MongoClient('mongodb://localhost:27017/', username='my-user')
    return client.dbdbd_db


def check_error(username, pwd):
    if username == '' or pwd == '':
        return False
    return True


db_client = pymongo.MongoClient("mongodb://localhost:27017/")

current_db = db_client["HW_from_leoska"]

collection = current_db["Messages"]

Message.send_message()
Message.get_message()

app = Flask(__name__)
start_time = datetime.now().strftime('%H:%M:%S %d.%m.%Y')


@app.route('/')
def hello():
    return 'Hello, user! Это мессенджер.'


# отправка сообщений
@app.route("/SendMessage")
def SendMessage():
    username = request.json['username']
    password = request.json['password']
    text = request.json['text']
    db = connect_to_mongodb()
    usr = db.users
    msg = db.messages

    if check_error(username, password):
        if usr.find_one({"username": username}):
            if not usr.find_one({"username": username, "password": password}):
                return False
        else:
            usr.insert_one({"username": username, "password": password})
        msg.insert_one({'username': username, 'text': text, 'timestamp': time.time()})

    return {'ok': True}


# получение сообщений
@app.route('/GetMessage')
def GetMessage():
    db = connect_to_mongodb()
    messages = db.messages
    after = float(request.args['after'])
    result = []
    for message in messages.find():
        # msg = loads(dumps(message))
        if message['timestamp'] > after:
            result.append(message)

    return {
        'messages': json.loads(json_util.dumps(result))
    }


app.run(host='0.0.0.0')
