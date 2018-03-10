import sqlite3
from flask_restful import Resource, reqparse
from flask import request

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(self, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ?"

        result = cursor.execute(query, (username,))  #always needs to be an tuple

        row = result.fetchone()   # get first one

        if row:
            user = User(row[0], row[1], row[2])
            print(user.username)
            #EQuivalent user = User(*row)
        else:
            print("user not found")
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id = ?"

        result = cursor.execute(query, (_id,))  #always needs to be an tuple

        row = result.fetchone()   # get first one

        if row:
            user = cls(row[0], row[1], row[2])
            #EQuivalent user = cls(*row)
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field can't be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field can't be blank."
    )

    def post(self):
        #data = request.get_json()

        data = UserRegister.parser.parse_args()

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES(NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()

        connection.close()
        return {'message': 'User created successfully'}
