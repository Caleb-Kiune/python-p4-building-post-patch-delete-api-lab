#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)

@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)
    bakery_data = bakery.to_dict()
    return make_response(jsonify(bakery_data), 200)

@app.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [bg.to_dict() for bg in baked_goods]
    return make_response(jsonify(baked_goods_list), 200)

@app.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    baked_good_data = baked_good.to_dict() if baked_good else {}
    return make_response(jsonify(baked_good_data), 200)

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_baked_good = BakedGood(
        name=data.get('name'),
        price=data.get('price'),
        bakery_id=data.get('bakery_id')
    )
    db.session.add(new_baked_good)
    db.session.commit()
    
    baked_good_data = new_baked_good.to_dict()
    return make_response(jsonify(baked_good_data), 201)

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)
    
    data = request.form
    if 'name' in data:
        bakery.name = data['name']
    
    db.session.commit()
    
    bakery_data = bakery.to_dict()
    return make_response(jsonify(bakery_data), 200)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = db.session.get(BakedGood, id)
    if not baked_good:
        return make_response(jsonify({'error': 'Baked good not found'}), 404)
    
    db.session.delete(baked_good)
    db.session.commit()
    
    response = make_response(jsonify({"message": "Baked good successfully deleted"}), 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
