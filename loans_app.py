from flask import Flask,jsonify,request, Response
import json
from settings import *
from cards_table import *
from loans_table import *
from users import *
import jwt, datetime
from functools import wraps
from validobject import *

def token_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token,app.config['SECRET_KEY'])
            return f(*args,**kwargs)
        except:
            return jsonify({"error":"need a valid token"}),401
    return wrapper
   
app.config['SECRET_KEY'] = 'meow'
@app.route('/login',methods=['POST'])
def get_token():
    request_data=request.get_json()
    username=str(request_data['username'])
    password=str(request_data['password'])

    match=User.match_username_pwd(username,password)
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date},app.config['SECRET_KEY'],algorithm='HS256')
        return token
    else:
        return Response("",401,mimetype='application/json')
 
@app.route('/loans')
def get_loans():
    return jsonify({'loans_table':Loans.get_all_loans()})

@app.route('/loans',methods=['POST'])
@token_required
def add_loans():
    request_data=request.get_json()
    if(validloanobject(request_data)):
        Loans.add_a_loan_type(request_data["type"],request_data["term"],request_data["l_limit"],request_data["u_limit"],request_data["facility"])
        response = Response("",201,mimetype='application/json')
        return response
    else:
        invalidcardobjectmsg={"error":"Invalid loan details passed","help":"please pass data in right format"}
        response = Response(json.dumps(invalidcardobjectmsg),400,mimetype='application/json')
        return response
    
@app.route('/loans/<string:type>',methods=['PATCH'])
@token_required
def update_loan(type):
        request_data = request.get_json() 
        if("l_limit" in request_data):
            Loans.update_loan_l_limit_bytype(type,request_data["l_limit"]) 
        if("u_limit" in request_data):
            Loans.update_loan_u_limit_bytype(type,request_data["u_limit"]) 
        if("facility" in request_data):
            Loans.update_loan_facility_by_type(type,request_data["facility"])         
        response = Response("",status=204)
        return response

@app.route('/loans/<string:term>',methods=['DELETE'])
@token_required
def delete_loan_byterm(term):
    if(Loans.delete_loan_by_term(term)):
        response = Response("",204)
        return response
    invalidloan={"error":"Enter correct term"}
    response = Response(json.dumps(invalidloan),404,mimetype='application/json')
    return response;


@app.route('/loans/<string:type>')
def get_loans_by_type(limit):
    return_value=Loans.get_all_loans()
    return jsonify(return_value)

app.run(port=5000)


    
