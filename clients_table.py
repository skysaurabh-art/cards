from settings import *
from flask import Flask
import json
from flask_sqlalchemy import SQLAlchemy


db=SQLAlchemy(app)

class Clients(db.Model):
    __tablename__='Clients_table_new'
    id=db.Column(db.Integer,primary_key=True)
    client_name=db.Column(db.String(80),nullable=False)
    client_acct_no=db.Column(db.String(80),nullable=False)
    client_id=db.Column(db.String(80),nullable=False)
    branch_id=db.Column(db.String(80),nullable=False)
    curr_clos_bal=db.Column(db.Float,nullable=False)
    cred_hist_len=db.Column(db.Float,nullable=False)
    has_card=db.Column(db.String(2),nullable=False)
    has_acct=db.Column(db.String(2),nullable=False)
    cred_pts=db.Column(db.Float,nullable=False)
    appr_status=db.Column(db.String(2),nullable=False)

    def json(self):
        return {"client_name":self.client_name,"client_acct_no":self.client_acct_no,"client_id":self.client_id,"branch_id":self.branch_id
        ,"curr_clos_bal":self.curr_clos_bal,"cred_hist_len":self.cred_hist_len,"has_card":self.has_card,"has_acct":self.has_acct
        ,"cred_pts":self.cred_pts,"appr_status":self.appr_status}
    
    
    def get_all_clients():
        return  [Clients.json(client) for client in Clients.query.all()]

    def check_for_score(_client_name,_client_acct_no,_branch_id,_curr_clos_bal,_cred_hist_len,_has_card,_has_acct):
        gen_client_id = _client_name[:3] + _client_acct_no[:3] + _branch_id[:2]

        a_pts =0
        b_pts = 0 
        if _cred_hist_len > 23:
            a_pts = 5
        if _cred_hist_len > 11 and _cred_hist_len < 24:
            a_pts = 2
        if _has_card == 'Y' and _has_acct == 'Y':
            b_pts == 3
        if _has_card == 'Y' and _has_acct == 'N':
            b_pts == 2
        if _has_card == 'N' and _has_acct == 'Y':
            b_pts == 2

        total_pts = a_pts + b_pts
        if total_pts > 4:
            _appr_status = 'Y'
        else:
            _appr_status = 'N'
        new_client = Clients(client_name=_client_name,client_acct_no=_client_acct_no,client_id=gen_client_id,branch_id=_branch_id,
            curr_clos_bal=_curr_clos_bal,cred_hist_len=_cred_hist_len,has_card=_has_card,has_acct=_has_acct,
            cred_pts=total_pts,appr_status=_appr_status)
        db.session.add(new_client)
        db.session.commit()

    
    def delete_client_by_name(_client_name):
        is_successful =  Clients.query.filter_by(client_name=_client_name).delete()
        db.session.commit()
        return bool(is_successful)


            
    def __repr__(self):
        loan_object={
            'client_name':self.client_name,
            'client_acct_no':self.client_acct_no,
            'client_id':self.client_id,
            'branch_id':self.branch_id,
            'curr_clos_bal':self.curr_clos_bal,
            'cred_hist_len':self.cred_hist_len,
            'has_card':self.has_card,
            'has_acct':self.has_acct,
            'cred_pts':self.cred_pts
            }
        return json.dumps(loan_object)



