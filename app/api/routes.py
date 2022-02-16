from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Inventory, car_schema, inventory_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/inventory', methods = ['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Inventory(make, model, year, color, user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/inventory', methods = ['GET'])
@token_required
def get_inventory(current_user_token):
    a_user = current_user_token.token
    inventory = Inventory.query.filter_by(user_token = a_user).all()
    response = inventory_schema.dump(inventory)
    return jsonify(response)
    
@api.route('/inventory/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    car = Inventory.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

#update endpoint
@api.route('/inventory/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Inventory.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.color = request.json['color']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


#delete endpoint
@api.route('/inventory/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Inventory.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)