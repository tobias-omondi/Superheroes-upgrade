#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api,Resource

from models import db, Hero,Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to my API of Super heroes"
        }
        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response
api.add_resource(Home, "/")

# def home():
#     return

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    json_heroes = []
    for hero in heroes:
        json_hero = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        }
        json_heroes.append(json_hero)

    response = make_response(jsonify(json_heroes), 200)
    return response

class HeroResource(Resource):
    def get(self, hero_id):
        hero = Hero.query.get(hero_id)
        if hero is None:
            response = make_response(jsonify({"error": "Hero not found"}))
            response.status_code = 404
            return response

        json_hero = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": []
        }

        for power in hero.hero_powers:
            json_power = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            json_hero["powers"].append(json_power)

        response = make_response(jsonify(json_hero))
        return response
        
@app.route('/powers', methods=['GET'])
def get_powers():
     powers = Power.query.all()
     serialized_powers = []
     for power in powers:
        json_power = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        serialized_powers.append(json_power)

     return jsonify(serialized_powers)

class PowerResource(Resource):
    def get(self, power_id):
        power = Power.query.get(power_id)
        if power is None:
            response = make_response(jsonify({"error": "Power not found"}))
            response.status_code = 404
            return response

        json_power = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }

        response = make_response(jsonify(json_power),200)
        
        return response
    
api.add_resource(PowerResource, '/powers/<int:power_id>', endpoint ='power')


class PowerPatchResource(Resource):
    def patch(self, power_id):
        power = Power.query.get(power_id)
        if power is None:
            response = make_response(jsonify({"error": "Power not found"}))
            response.status_code = 404
            return response

        json_data = request.get_json()
        power.description = json_data["description"]

        try:
            db.session.commit()
        except Exception as e:
            response = make_response(jsonify({"errors": [str(e)]}))
            response.status_code = 400
            return response

        json_power = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }

        response = make_response(jsonify(json_power),201)
        
        return response

api.add_resource(PowerResource, '/powers/<int:power_id>')

class HeroPowerResource(Resource):
    def post(self):
        json_data = request.get_json()

        hero_power = HeroPower(
            strength=json_data["strength"],
            power_id=json_data["power_id"],
            hero_id=json_data["hero_id"]
        )

        try:
            db.session.add(hero_power)
            db.session.commit()
        except Exception as e:
            response = make_response(jsonify({"errors": [str(e)]}))
            response.status_code = 400
            return response

        hero = Hero.query.get(json_data["hero_id"])

        json_hero = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": []
        }

        for hero_power in hero.hero_powers:
            json_power = {
                "id": hero_power.id,
                "name": hero_power.power.name,
                "description": hero_power.power.description
            }
            json_hero["powers"].append(json_power)

        response = make_response(jsonify(json_hero),200)
        
        return response

api.add_resource(HeroPowerResource, '/hero_powers')

# @app.route('/')
# def home():
#     return ''



if __name__ == '__main__':
    app.run(port=5552, debug= True)
