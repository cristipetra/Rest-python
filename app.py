from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'cristian'
api = Api(app)

jwt = JWT(app, authenticate, identity)   # /auth

items = []


class Item(Resource):
    @jwt_required()
    def get(self, name):

        #item = next(filter(lambda x: x['name'] == name, items), None)
        item = filter(lambda x: x['name'] == name, items)

        return {'item': item}, 200 if item else 404

    def post(self, name):
        '''
        if item = next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' alreadey exist.".format(name)}, 400
        '''
        request_data = request.get_json()
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(ItemList,'/items')

api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

app.run(port=5000)
