from settings import *
from flask import Flask
import json
from flask_sqlalchemy import SQLAlchemy


db=SQLAlchemy(app)

class Loans(db.Model):
    __tablename__='loans_table'
    id=db.Column(db.Integer,primary_key=True)
    type=db.Column(db.String(80),nullable=False)
    term=db.Column(db.String(80),nullable=False)
    l_limit=db.Column(db.Float,nullable=False)
    u_limit=db.Column(db.Float,nullable=False)
    facility=db.Column(db.String(80),nullable=False)

    def json(self):
        return {"type":self.type,"term":self.term,"l_limit":self.l_limit,"u_limit":self.u_limit,"facility":self.facility}
    
    
    def get_all_loans():
        return  [Loans.json(loan) for loan in Loans.query.all()]

    
    def add_a_loan_type(_type,_term,l_limit,u_limit,_facility):
        new_loan = Loans(type=_type,term=_term,l_limit=l_limit,u_limit=u_limit,facility=_facility)
        db.session.add(new_loan)
        db.session.commit()

    def get_all_loans_by_type(_type):
        return Loans.json(Loans.query.filter_by(type=_type).first())
    
    def delete_loan_by_type(_type):
        is_successful =  CreditCards.query.filter_by(type=_type).delete()
        db.session.commit()
        return bool(is_successful)

    def delete_loan_by_term(_term):
        is_successful =  CreditCards.query.filter_by(term=_term).delete()
        db.session.commit()
        return bool(is_successful)
        
    def update_loan_facility_by_type(_type,_facility):
        loan_to_update = Loans.query.filter_by(type=_type).first()
        loan_to_update.facility = _facility
        db.session.commit()

    def update_loan_l_limit_bytype(_type,_l_limit):
        loan_to_update = Loans.query.filter_by(type=_type).first()
        loan_to_update.l_limit = _l_limit
        db.session.commit()
        
    def update_loan_u_limit_bytype(_type,_u_limit):
        loan_to_update = Loans.query.filter_by(type=_type).first()
        loan_to_update.u_limit = _u_limit
        db.session.commit()
        
    
    def __repr__(self):
        loan_object={
            'type':self.type,
            'term':self.term,
            'l_limit':self.l_limit,
            'u_limit':self.u_limit,
            'facility':self.facility
            }
        return json.dumps(loan_object)



