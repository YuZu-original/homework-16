from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

from data_json import USERS, ORDERS, OFFERS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    
    def make_dict(self):
        """ Возвращает данные о User в виде dict """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    
    def make_dict(self):
        """ Возвращает данные о Order в виде dict """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    
    def make_dict(self):
        """ Возвращает данные о Offer в виде dict """
        return {
            "id":self.id,
            "order_id":self.order_id,
            "executor_id":self.executor_id
        }


db.create_all()


for user_info in USERS:
    user = User(
        id = user_info["id"],
        first_name = user_info["first_name"],
        last_name = user_info["last_name"],
        age = user_info["age"],
        email = user_info["email"],
        role = user_info["role"],
        phone = user_info["phone"]
    )
    db.session.add(user)
    db.session.commit()

for order_info in ORDERS:
    order = Order(
        id = order_info["id"],
        name = order_info["name"],
        description = order_info["description"],
        start_date = order_info["start_date"],
        end_date = order_info["end_date"],
        address = order_info["address"],
        price = order_info["price"],
        customer_id = order_info["customer_id"],
        executor_id = order_info["executor_id"]
    )
    db.session.add(order)
    db.session.commit()

for offer_info in OFFERS:
    offer = Offer(
        id = offer_info["id"],
        order_id = offer_info["order_id"],
        executor_id = offer_info["executor_id"]
    )
    db.session.add(offer)
    db.session.commit()


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
        user = User(
            id = user_info["id"],
            first_name = user_info["first_name"],
            last_name = user_info["last_name"],
            age = user_info["age"],
            email = user_info["email"],
            role = user_info["role"],
            phone = user_info["phone"]
        )
        db.session.add(user)
        db.session.commit()
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
        user = User.query.get(pk)
        user.first_name = user_info["first_name"]
        user.last_name = user_info["last_name"]
        user.age = user_info["age"]
        user.email = user_info["email"]
        user.role = user_info["role"]
        user.phone = user_info["phone"]
        
        db.session.add(user)
        db.session.commit()
        return ""
    elif request.method == "DELETE":
        user = User.query.get(pk)
        db.session.delete(user)
        db.session.commit()
        return ""

@app.route('/orders')
def all_orders_page():
    if request.method == 'GET':
        orders_list = []
        for order in Order.query.all():
            orders_list.append(order.make_dict())
        
        return jsonify(orders_list)
    elif request.method == 'POST':
        order_info = json.loads(request.data)
        order = Order(
            id = order_info["id"],
            name = order_info["name"],
            description = order_info["description"],
            start_date = order_info["start_date"],
            end_date = order_info["end_date"],
            address = order_info["address"],
            price = order_info["price"],
            customer_id = order_info["customer_id"],
            executor_id = order_info["executor_id"]
        )
        db.session.add(order)
        db.session.commit()
        return ""

@app.route('/orders/<int:pk>')
def orders_by_id_page(pk):
    if request.method == 'GET':
        order = Order.query.get(pk)
        if order:
            return jsonify(order.make_dict())
        return jsonify([])
    elif request.method == 'PUT':
        order_info = json.loads(request.data)
        order = Order.query.get(pk)
        
        order.id = order_info["id"]
        order.name = order_info["name"]
        order.description = order_info["description"]
        order.start_date = order_info["start_date"]
        order.end_date = order_info["end_date"]
        order.address = order_info["address"]
        order.price = order_info["price"]
        order.customer_id = order_info["customer_id"]
        order.executor_id = order_info["executor_id"]
        
        db.session.add(order)
        db.session.commit()
        return ""
    elif request.method == "DELETE":
        order = Order.query.get(pk)
        db.session.delete(order)
        db.session.commit()
        return ""


@app.route('/offers')
def all_offers_page():
    if request.method == 'GET':
        offers_list = []
        for offer in Offer.query.all():
            offers_list.append(offer.make_dict())
        
        return jsonify(offers_list)
    elif request.method == 'POST':
        offer_info = json.loads(request.data)
        offer = Offer(
            id = offer_info["id"],
            order_id = offer_info["order_id"],
            executor_id = offer_info["executor_id"]
        )
        db.session.add(offer)
        db.session.commit()
        return ""

@app.route('/offers/<int:pk>')
def offers_by_id_page(pk):
    if request.method == 'GET':
        offer = Offer.query.get(pk)
        if offer:
            return jsonify(offer.make_dict())
        return jsonify([])
    elif request.method == 'PUT':
        offer_info = json.loads(request.data)
        offer = Offer.query.get(pk)
        
        offer.id = offer_info["id"]
        offer.order_id = offer_info["order_id"]
        offer.executor_id = offer_info["executor_id"]
        
        db.session.add(offer)
        db.session.commit()
        return ""
    elif request.method == "DELETE":
        offer = Offer.query.get(pk)
        db.session.delete(offer)
        db.session.commit()
        return ""

if __name__ == '__main__':
    app.run(debug=True)