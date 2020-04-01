from flask import Flask, json, g, request, jsonify, abort, Response
from binance.client import Client
import time
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import uuid
import sys
if('C:\\Users\\dwood\\Python' not in sys.path):
    sys.path.insert(0, 'C:\\Users\\dwood\\Python')
from Hidden import hidden
from helpers import DecimalEncoder, ParseBehaviorGroup
from MBot import MBOT


h = hidden.hidden() #uses hidden keys from unshared class to instantiate a connection to the db and to the exchange's client
db = h.dynamodb
marketBotTable = db.Table('Market_Bots')
client = h.client

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome!"

@app.route("/api/save_bot/", methods=["POST"])
def save_bot():
    request_data = request.get_json()
    #validate incoming bot properties -- if name exists in db, dont allow

    #save bot in aws dynamodb table
    response = marketBotTable.put_item(
        Item={
                "name": request_data['name'],
                "buy_behaviors": request_data['buy_behaviors'],
                "sell_behaviors": request_data['sell_behaviors']
            }
        )
    return response

@app.route("/api/delete_bot/", methods=["POST"])
def delete_bot():
    request_data = request.get_json()
    name = request_data['name']
    
    delete_response = marketBotTable.delete_item(
        Key={
            'name': name
        },
        ConditionExpression=Key('name').eq(name)
    )

    return delete_response


@app.route("/api/run_bot/", methods=["POST"])
def run_bot():
    #creates an mbot instance with the given behaviors and then executes the run function
    try:
        request_data = request.get_json()
        request_name = request_data['name']
        request_cycles = request_data['cycles']
        request_token = request_data['token']
        request_asset = request_data['asset']
        
        if(request_name):
        #get mbot properties from name in dynamodb table
            db_response = marketBotTable.get_item(
                Key = {
                    'name': request_name
                }
            )
            if(len(db_resonse['Items']) > 0):
                #parse buy behaviors into buy group
                buy_behaviors = ParseBehaviorGroup(db_response['Items'][0]['buy_behaviors'])
                #parse sell behaviors into sell group
                sell_behaviors = ParseBehaviorGroup(db_response['Items'][0]['sell_behaviors'])
                #create instnace of mbot with the parsed buy behaviors and sell behaviors
                MBOT(buy_behaviors, sell_behaviors)
                MBOT.test_run(request_token, request_asset, request_cycles)
                # Should return data from test/actual run
        return "Bot Run "+request_cycles+" times!"
    except: 
        return

@app.route("/api/get_sell_behaviors/<identifier>", methods=["GET"])
def get_sell_behaviors(identifier):
    # Requests and returns the buy behavior data of the current market bot object from the db,
    # returns an empty json object if the market bot doesn't exist
    dbResponse = marketBotTable.get_item(
        Key={
            'id': identifier
            }
        )
    
    mbot_json = json.dumps(dbResponse['Item'], indent=4, cls=DecimalEncoder)
    sell_behaviors = mbot_json.sell_behaviors
    #todo -- validation
    
    return jsonify(sell_behaviors)

@app.route("/api/set_sell_behaviors/", methods=["POST"])
def set_sell_behaviors():
    try:
        request_object = json.parse(request.get_json())
        request_id = request_object.id
        
        dbResponse = marketBotTable.get_item(
            Key={
                'id': request_id
                }
            )
    except:
        return
    # Sets the sell behaviors of the current market bot object in the db, 
    # If the current market bot doesnt exist yet, this operation fails. Ensure that
    # the UI doesnt allow one to make this call unless they are adding it 
    # to an existing market bot entry
    return "set_sell_behaviors"

@app.route("/api/get_buy_behaviors/<identifier>", methods=["GET"])
def get_buy_behaviors(identifier):
    # Requests and returns the sell behavior data of the current market bot object from the db,
    # returns an empty json object if the market bot doesn't exist
    return "get_buy_behaviors"

@app.route("/api/set_buy_behaviors/", methods=["POST"])
def set_buy_behaviors():
    try:
        request_object = json.parse(request.get_json())
        request_id = request_object.id
    except:
        return
    # Sets the buy behaviors of the current market bot object in the db, 
    # If the current market bot doesnt exist yet, this operation fails. Ensure that
    # the UI doesnt allow one to make this call unless they are adding it 
    # to an existing market bot entry
    return "set_buy_behaviors"

@app.route("/api/update_api_keys/", methods=["POST"])
def update_api_keys():
    # gets my auth keys for the binance api and 
    pass
    
# bot = {
#             "id":"123",
#             "name":"Bob",
#             "buy_behaviors":{
#                                 "group_conditional":"or",
#                                 "group":[
#                                             {
#                                                 "group_conditional":"and",
#                                                 "group":[
#                                                             {
#                                                                 "function":"moving_average",
#                                                                 "inputs":{
#                                                                             "interval":200
#                                                                     },
#                                                                 "conditional":"greater_than",
#                                                                 "target":"current_price"
#                                                                 },
#                                                             {
#                                                                 "function":"moving_dx",
#                                                                 "inputs":{
#                                                                             "interval":50
#                                                                     },
#                                                                 "conditional":"less_than",
#                                                                 "target":"0.996"
#                                                                 }
#                                                     ]
#                                                 }
#                                     ]
#                 },
#             "sell_behaviors":{
#                                 "group_conditional":"or",
#                                 "group":[
#                                             {
#                                                 "group_conditional":"and",
#                                                 "group":[
#                                                             {
#                                                                 "function":"support",
#                                                                 "inputs":{
#                                                                             "interval":200
#                                                                     },
#                                                                 "conditional":"less_than",
#                                                                 "target":"current_price"
#                                                                 },
#                                                             {
#                                                                 "function":"moving_dx",
#                                                                 "inputs":{
#                                                                             "interval":50
#                                                                     },
#                                                                 "conditional":"greater_than_or_equal_to",
#                                                                 "target":"1.12"
#                                                                 }
#                                                     ]
#                                                 }
#                                     ]
#                 }
#         }




app.run()