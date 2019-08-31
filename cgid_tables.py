from settings import *
from flask import Flask
import json
from flask_sqlalchemy import SQLAlchemy


db=SQLAlchemy(app)

class CreditCards(db.Model):
    __tablename__='cards_table'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    type=db.Column(db.String(80),nullable=False)
    limit=db.Column(db.Float,nullable=False)
    region=db.Column(db.String(80),nullable=False)

    def json(self):
        return {"name":self.name,"type":self.type,"limit":self.limit,"region":self.region}
    
    
    def get_all_cards():
        return  [CreditCards.json(card) for card in CreditCards.query.all()]

    
    def add_all_cards(_name,_type,_limit,_region):
        new_card = CreditCards(name=_name, type=_type,limit=_limit,region=_region)
        db.session.add(new_card)
        db.session.commit()

    def get_all_cards_by_limit(_limit):
        return CreditCards.json(CreditCards.query.filter_by(limit=_limit).first())
    
    def delete_card(_limit):
        is_successful =  CreditCards.query.filter_by(limit=_limit).delete()
        db.session.commit()
        return bool(is_successful)
        
    def update_card_region(_limit,_region):
        card_to_update = CreditCards.query.filter_by(limit=_limit).first()
        card_to_update.region = _region
        db.session.commit()

    def update_card_type(_limit,_type):
        card_to_update = CreditCards.query.filter_by(limit=_limit).first()
        card_to_update.type = _type
        db.session.commit()
        
    def update_card_name(_limit,_name):
        card_to_update = CreditCards.query.filter_by(limit=_limit).first()
        card_to_update.name = _name
        db.session.commit()
        
    def replace_all_card(_limit,_name,_type,_region):
        card_to_replace = CreditCards.query.filter_by(limit=_limit).first()
        card_to_replace.region = _region
        card_to_replace.name = _name
        card_to_replace.type = _type
        db.session.commit()
    
    def __repr__(self):
        card_object={
            'name':self.name,
            'type':self.type,
            'limit':self.limit,
            'region':self.region
            }
        return json.dumps(card_object)



