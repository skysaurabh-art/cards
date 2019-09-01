from flask import Flask,jsonify,request, Response
import json
from settings import *
from cards_table import *
from loans_table import *
from clients_table import *
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
 
@app.route('/clients')
def get_clients():
    return jsonify({'Clients_table_new':Clients.get_all_clients()})

@app.route('/clients',methods=['POST'])
@token_required
def add_clients():
    request_data=request.get_json()
    if(validclientobject(request_data)):
        Clients.check_for_score(request_data["client_name"],request_data["client_acct_no"],request_data["branch_id"],
            request_data["curr_clos_bal"],request_data["cred_hist_len"],request_data["has_card"],request_data["has_acct"])
        response = Response("Please check the Approval Status for loan",201,mimetype='application/json')
        return response
    else:
        invalidcardobjectmsg={"error":"Invalid client details passed","help":"please pass data in right format"}
        response = Response(json.dumps(invalidcardobjectmsg),400,mimetype='application/json')
        return response


@app.route('/Clients/<string:client_name>',methods=['DELETE'])
@token_required
def delete_client_by_nm(client_name):
    if(Clients.delete_client_by_name(client_name)):
        response = Response("",204)
        return response
    invalidloan={"error":"Enter correct client"}
    response = Response(json.dumps(invalidloan),404,mimetype='application/json')
    return response;

@app.route('/clients/<string:client_name>')
def get_clients_by_type(client_name):
    return_value=Clients.get_all_clients()
    return jsonify(return_value)

app.run(port=5000)


    
