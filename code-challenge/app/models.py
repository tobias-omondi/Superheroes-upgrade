from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes' 
    serialize_rules = ('-powers.heroes', '-heropowers.power')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
# add any models you may need.

    powers = db.relationship('HeroPower', back_populates='hero')

    def repr(self):  
        return f'<Hero {self.name} aka {self.super_name}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers' 
    serialize_rules = ('-heroes.powers', '-heropowers.hero')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String)  
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship('HeroPower', back_populates='power')

    def repr(self):  
        return f'<Power {self.name} aka {self.description}'
    
    @validates('description')
    def validate_description(self, key, description):
        if description is None or len(description) < 20:
            raise ValueError('Description must be present and at least 20 characters long.')
        return description

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'heropowers' 
    serialize_rules = ('-hero.powers', '-power.heroes')

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(10))
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError('Strength must be one of the following values: Strong, Weak, Average')
        return strength

