from flask import Flask,jsonify,request, Response
import json
from settings import *
from cgid_tables import *
from users import *
import jwt, datetime
from functools import wraps

def validcardobject(cardobject):
    if "name" in cardobject and "type" in cardobject and "limit" in cardobject and  "region" in cardobject:
        return True
    else:
        return False

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
 
@app.route('/cards')

def get_cards():
    return jsonify({'cards_table':CreditCards.get_all_cards()})

@app.route('/cards',methods=['POST'])
@token_required
def add_cards():
    request_data=request.get_json()
    if(validcardobject(request_data)):
        CreditCards.add_all_cards(request_data["name"],request_data["type"],request_data["limit"],request_data["region"])
        response = Response("",201,mimetype='application/json')
        return response
    else:
        invalidcardobjectmsg={"error":"Invalid card details passed","help":"please pass data in right format"}
        response = Response(json.dumps(invalidcardobjectmsg),400,mimetype='application/json')
        return response
 

@app.route('/cards/<int:limit>',methods=['PUT'])
@token_required
def replace_card(limit):
    request_data = request.get_json()
    if(not validcardobject(request_data)):
        invalidcardmsg={"error":"invalid card object passed"}
        response=Response(json.dumps(invalidcardmsg),404,mimetype='application/json')
        return response
    CreditCards.replace_all_card(limit,request_data['name'],request_data["type"],request_data["region"])
    response = Response("",status=204)
    return response
    
@app.route('/cards/<int:limit>',methods=['PATCH'])
@token_required
def update_card(limit):
        request_data = request.get_json()
       # if(not validcardobject(request_data)):
        #    invalidcardmsg={"error":"invalid card object passed"}
         #   response=Response(json.dumps(invalidcardmsg),404,mimetype='application/json')
          #  return response"""
        if("name" in request_data):
            CreditCards.update_card_name(limit,request_data["name"])  
        if("type" in request_data):
           CreditCards.update_card_type(limit,request_data["type"])   
        if("region" in request_data):
            CreditCards.update_card_region(limit,request_data["region"]) 
        response = Response("",status=204)
        return response

@app.route('/cards/<int:limit>',methods=['DELETE'])
@token_required
def delete_card(limit):
    if(CreditCards.delete_card(limit)):
        response = Response("",204)
        return response
    invalidcard={"error":"Enter correct ISBN"}
    response = Response(json.dumps(invalidcard),404,mimetype='application/json')
    return response;


@app.route('/cards/<int:limit>')
def get_cards_by_limit(limit):
    return_value=CreditCards.get_all_cards()
    return jsonify(return_value)



                                 
app.run(port=5000)


    
