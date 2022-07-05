from data_json import USERS, ORDERS, OFFERS
from models import User, Order, Offer
from setup_db import db

class Database:
    def load_all_users(self):
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


    def load_all_orders(self):
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


    def load_all_offers(self):
        for offer_info in OFFERS:
            offer = Offer(
                id = offer_info["id"],
                order_id = offer_info["order_id"],
                executor_id = offer_info["executor_id"]
            )
            db.session.add(offer)
            db.session.commit()
    
    
    ########## USER ##########
    def add_user(self, user_info):
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
    
    
    def update_user(self, pk, user_info):
        user = User.query.get(pk)
        user.first_name = user_info["first_name"]
        user.last_name = user_info["last_name"]
        user.age = user_info["age"]
        user.email = user_info["email"]
        user.role = user_info["role"]
        user.phone = user_info["phone"]
        
        db.session.add(user)
        db.session.commit()
    
    
    def delete_user(self, pk):
        user = User.query.get(pk)
        db.session.delete(user)
        db.session.commit()
    
    
    ######### ORDER ##########
    def add_order(self, order_info):
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
    
    
    def update_order(self, pk, order_info):
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
    
    
    def delete_order(self, pk):
        order = Order.query.get(pk)
        db.session.delete(order)
        db.session.commit()
    
    
    ######### OFFER ##########
    def add_offer(self, offer_info):
        offer = Offer(
            id = offer_info["id"],
            order_id = offer_info["order_id"],
            executor_id = offer_info["executor_id"]
        )
        db.session.add(offer)
        db.session.commit()
    
    
    def update_offer(self, pk, offer_info):
        offer = Offer.query.get(pk)
        
        offer.id = offer_info["id"]
        offer.order_id = offer_info["order_id"]
        offer.executor_id = offer_info["executor_id"]
        
        db.session.add(offer)
        db.session.commit()
    
    
    def delete_offer(self, pk):
        offer = Offer.query.get(pk)
        db.session.delete(offer)
        db.session.commit()