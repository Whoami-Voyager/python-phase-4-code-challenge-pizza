#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods = ["GET"])
def served_resteraunt():
    chain = Restaurant.query.all()
    return [restaurant.to_dict(rules = ("-restaurant_pizzas",)) for restaurant in chain], 200

@app.route("/restaurants/<int:id>", methods = ["GET", "DELETE"])
def single_restaurant(id):
    rest = Restaurant.query.filter(Restaurant.id == id).first()
    if rest:
        if request.method == "GET":
            return rest.to_dict()
        elif request.method == "DELETE":
            db.session.delete(rest)
            db.session.commit()
            return {}, 204
    else:
        return {"error": "Restaurant not found"}, 404

@app.route("/pizzas", methods = ["GET"])
def food():
    all_pizza = Pizza.query.all()
    return [pizza.to_dict(rules = ("-restaurant_pizzas",)) for pizza in all_pizza], 200

@app.route("/restaurant_pizzas", methods = ["POST"])
def friends():
    try:
        data = request.get_json()
        join_pizza = RestaurantPizza(
            pizza_id = data['pizza_id'],
            restaurant_id = data['restaurant_id'],
            price = data['price']
        )
        db.session.add(join_pizza)
        db.session.commit()
        print(join_pizza.to_dict())
        return join_pizza.to_dict(), 201
    except:
        return {"errors": ["validation errors"]}, 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
