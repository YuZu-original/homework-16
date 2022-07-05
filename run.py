from flask import Flask, jsonify, request
import json

from setup_db import db
from database import Database
from models import User, Order, Offer


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db.init_app(app)
app.app_context().push()

db.create_all()

Database().load_all_users()
Database().load_all_orders()
Database().load_all_offers()


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/users', methods=['GET','POST'])
def all_users_page():
    if request.method == 'GET':
        users_list = []
        for user in User.query.all():
            users_list.append(user.make_dict())
        
        return jsonify(users_list)
    elif request.method == 'POST':
        user_info = json.loads(request.data)
        Database().add_user(user_info)
        return ""


@app.route('/users/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def users_by_id_page(pk):
    if request.method == 'GET':
        user = User.query.get(pk)
        if user:
            return jsonify(user.make_dict())
        return jsonify([])
    elif request.method == 'PUT':
        user_info = json.loads(request.data)
        Database().update_user(pk, user_info)
        return ""
    elif request.method == "DELETE":
        Database().delete_user(pk)
        return ""


@app.route('/orders', methods=['GET','POST'])
def all_orders_page():
    if request.method == 'GET':
        orders_list = []
        for order in Order.query.all():
            orders_list.append(order.make_dict())
        
        return jsonify(orders_list)
    elif request.method == 'POST':
        order_info = json.loads(request.data)
        Database().add_order(order_info)
        return ""


@app.route('/orders/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def orders_by_id_page(pk):
    if request.method == 'GET':
        order = Order.query.get(pk)
        if order:
            return jsonify(order.make_dict())
        return jsonify([])
    elif request.method == 'PUT':
        order_info = json.loads(request.data)
        Database().update_order(pk, order_info)
        return ""
    elif request.method == "DELETE":
        order = Order.query.get(pk)
        db.session.delete(order)
        db.session.commit()
        return "", 200


@app.route('/offers', methods=['GET','POST'])
def all_offers_page():
    if request.method == 'GET':
        offers_list = []
        for offer in Offer.query.all():
            offers_list.append(offer.make_dict())
        
        return jsonify(offers_list)
    elif request.method == 'POST':
        offer_info = json.loads(request.data)
        Database().add_offer(offer_info)
        return ""


@app.route('/offers/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def offers_by_id_page(pk):
    if request.method == 'GET':
        offer = Offer.query.get(pk)
        if offer:
            return jsonify(offer.make_dict())
        return jsonify([])
    elif request.method == 'PUT':
        offer_info = json.loads(request.data)
        Database().update_offer(pk, offer_info)
        return ""
    elif request.method == "DELETE":
        Database().delete_offer(pk)
        return ""


if __name__ == '__main__':
    app.run(debug=True)