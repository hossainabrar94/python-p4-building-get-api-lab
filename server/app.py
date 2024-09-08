#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc
import ipdb

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries_list = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
            "updated_at": bakery.updated_at
        }
        bakeries_list.append(bakery_dict)

    return make_response(bakeries_list,200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    baked_goods = []
    for good in bakery.baked_goods:
        baked_good = {
            "name": good.name,
            "price": good.price,
            "bakery_id": good.bakery_id,
            "created_at": good.created_at,
            "updated_at": good.updated_at
        }
        baked_goods.append(baked_good)
    bakery_dict = {
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,
        "updated_at": bakery.updated_at,
        "baked_goods": baked_goods
    }
    return make_response(bakery_dict, 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    baked_goods_list=[]
    for good in baked_goods:
        baked_good_dict = {
            "id": good.id,
            "name": good.name,
            "price": good.price,
            "bakery_id": good.bakery_id,
            "created_at": good.created_at,
            "updated_at": good.updated_at
        }
        baked_goods_list.append(baked_good_dict)
    return make_response(baked_goods_list,200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first()
    baked_good_dict = {
        "id": baked_good.id,
        "name": baked_good.name,
        "price": baked_good.price,
        "bakery_id": baked_good.bakery_id,
        "created_at": baked_good.created_at,
        "updated_at": baked_good.updated_at
    }
    return make_response(baked_good_dict,200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
