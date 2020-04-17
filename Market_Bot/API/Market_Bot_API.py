from MBot import MBOT
from flask_cors import CORS
from flask import Flask, json, g, request, jsonify, abort, Response
from binance.client import Client
import time
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import uuid
import threading
import sys
if('C:\\Users\\dwood\\Python' not in sys.path):
    sys.path.insert(0, 'C:\\Users\\dwood\\Python')
    from Hidden import hidden
    from helpers import DecimalEncoder, ParseBehaviorGroup, ParseBehavior
    from TemporalFeatures import Features as ft

h = hidden.hidden()  # uses hidden keys from unshared class to instantiate a connection to the db and to the exchange's client
db = h.dynamodb
market_bot_table = db.Table('Market_Bots')
market_prices_table = db.Table('Market_Prices')
client = h.client

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Welcome!"


@app.route("/api/get_bots/", methods=["GET"])
def get_bots():
    db_response = market_bot_table.scan(

    )

    return json.dumps(db_response['Items'], cls=DecimalEncoder)


@app.route("/api/get_bot/<name>", methods=["GET"])
def get_bot(name):
    db_response = market_bot_table.get_item(
        Key={
            'name': name
        }
    )

    return json.dumps(db_response['Item'], cls=DecimalEncoder)


@app.route("/api/save_bot/", methods=["POST"])
def save_bot():
    request_data = request.get_json()
    # validate incoming bot properties -- if name exists in db, dont allow

    # save bot in aws dynamodb table
    db_response = market_bot_table.put_item(
        Item={
            "name": request_data['name'],
            "buy_behaviors": request_data['buy_behaviors'],
            "sell_behaviors": request_data['sell_behaviors']
        }
    )
    return json.dumps(db_response, cls=DecimalEncoder)


@app.route("/api/delete_bot/", methods=["POST"])
def delete_bot():
    request_data = request.get_json()
    name = request_data['name']

    db_response = market_bot_table.delete_item(
        Key={
            'name': name
        },
        ConditionExpression=Key('name').eq(name)
    )

    return json.dumps(db_response, cls=DecimalEncoder)


@app.route("/api/run_bot/", methods=["POST"])
def run_bot():
    # creates an mbot instance with the given behaviors and then executes the run function
    request_data = request.get_json()
    request_name = request_data['name']
    request_cycles = request_data['cycles']
    request_token = request_data['token']
    request_asset = request_data['asset']
    if('test' in request_data):
        request_test = request_data['test']

    if(request_name):
        # get mbot properties from name in dynamodb table
        db_response = market_bot_table.get_item(
            Key={
                'name': request_name
            }
        )

        if(db_response['Item']):
            # parse buy behaviors into buy group
            buy_behaviors = ParseBehaviorGroup(
                db_response['Item']['buy_behaviors'])
            # parse sell behaviors into sell group
            sell_behaviors = ParseBehaviorGroup(
                db_response['Item']['sell_behaviors'])
            # create instnace of mbot with the parsed buy behaviors and sell behaviors
            mbot = MBOT(buy_behaviors, sell_behaviors)
            if(request_test):
                # get test data
                test_data = market_prices_table.scan(
                    FilterExpression=Key('token_asset').eq(
                        request_token+"_"+request_asset),  # & Key('open_time').gt(decimal.Decimal((time.time()-(30*86400))*1000)),
                    ProjectionExpression="open_price"
                )
                input_array = [float(x['open_price'])
                               for x in test_data['Items']]
                return json.dumps(mbot.test_run(input_array, request_token, request_asset), cls=DecimalEncoder)
            else:
                # MBOT.run()
                pass
            # Should return data from test/actual run
    return json.dumps(db_response, cls=DecimalEncoder)


@app.route("/api/get_sell_behaviors/", methods=["GET"])
def get_sell_behaviors(name):
    # Requests and returns the sell behavior data of the current market bot object from the db,
    # returns an empty json object if the market bot doesn't exist
    request_data = request.get_json()
    if("name" in request_data):
        db_response = market_bot_table.get_item(
            Key={
                'name': request_data['name']
            }
        )
        if(db_response['Item']):
            return json.dumps(db_response['Item']['sell_behaviors'], cls=DecimalEncoder)
    return "{}"


@app.route("/api/set_sell_behaviors/", methods=["POST"])
def set_sell_behaviors():
    # Sets the sell behaviors of the current market bot object in the db,
    # If the current market bot doesnt exist yet, this operation fails. Ensure that
    # the UI doesnt allow one to make this call unless they are adding it
    # to an existing market bot entry
    request_data = request.get_json()
    if("name" in request_data):
        request_name = request_data['name']
        db_response = market_bot_table.update_item(
            Key={
                'name': request_name
            },
            UpdateExpression="set sell_behaviors = :r",
            ExpressionAttributeValues={
                ':r': request_data['sell_behaviors']
            },
            ReturnValues="UPDATED_NEW"
        )
        if(db_response):
            return json.dumps(db_response, cls=DecimalEncoder)
    return "Update Failed"


@app.route("/api/get_buy_behaviors/<name>", methods=["GET"])
def get_buy_behaviors(name):
    # Requests and returns the sell behavior data of the current market bot object from the db,
    # returns an empty json object if the market bot doesn't exist
    request_data = request.get_json()
    if("name" in request_data):
        db_response = market_bot_table.get_item(
            Key={
                'name': request_data['name']
            }
        )
        if(db_response['Item']):
            return json.dumps(db_response['Item']['buy_behaviors'], cls=DecimalEncoder)
    return "{}"


@app.route("/api/set_buy_behaviors/", methods=["POST"])
def set_buy_behaviors():
    # Sets the buy behaviors of the current market bot object in the db,
    # If the current market bot doesnt exist yet, this operation fails. Ensure that
    # the UI doesnt allow one to make this call unless they are adding it
    # to an existing market bot entry
    request_data = request.get_json()
    if("name" in request_data):
        request_name = request_data['name']
        db_response = market_bot_table.update_item(
            Key={
                'name': request_name
            },
            UpdateExpression="set buy_behaviors = :r",
            ExpressionAttributeValues={
                ':r': request_data['buy_behaviors']
            },
            ReturnValues="UPDATED_NEW"
        )
        if(db_response):
            return json.dumps(db_response, cls=DecimalEncoder)
    return "Update Failed"


@app.route("/api/test_behavior/", methods=['POST'])
def test_behavior():
    # takes the function object from the request body and runs that function over
    # the prices in the db (or for the last x days if supplied in request body)
    request_data = request.get_json()
    request_days = 30
    request_days = request_data['days']
    request_token = request_data['token']
    request_asset = request_data['asset']
    request_behavior = request_data['behavior']
    behavior = ParseBehavior(request_behavior)
    test_data = market_prices_table.scan(
        FilterExpression=Key('token_asset').eq(
            request_token+"_"+request_asset),  # & Key('open_time').gt(decimal.Decimal((time.time() - 86400*request_days))*1000),
        ProjectionExpression="open_price"
    )
    input_array = [float(x['open_price'])
                   for x in test_data['Items']]

    a = input_array  # ft.normalize(input_array)
    # ft.normalize(behavior.set_data(input_array))
    b = behavior.set_data(input_array)
    if(b[0]/a[0] < 0.75):
        a = ft.normalize(input_array)
        b = ft.normalize(behavior.set_data(input_array))
    return json.dumps([a, b])


@app.route("/api/update_market_prices/", methods=['POST'])
def Update_Market_Prices():
    request_data = request.get_json()

    days = 5
    token = 'BTC'
    asset = 'USDT'

    if('days' in request_data):
        days = request_data['days']
    if('token' in request_data):
        token = request_data['token']
    if('asset' in request_data):
        asset = request_data['asset']

    try:
        t1 = threading.Thread(
            target=lambda: execute_prices_update(days, token, asset))
        t1.start()

        # if no error is thrown, return that the database is updating
        return "Database Updated!"
    except:
        return "Database Update Failed! (unable to make contact with the exchange or aws)"


def execute_prices_update(days, token, asset):
    start = time.perf_counter()
    # query the exchange's api to get the data (do this in a different thread)
    klines = client.get_historical_klines(token+asset, Client.KLINE_INTERVAL_1MINUTE,
                                          str(time.time()-(86400*days)))

    # in that thread, send the data back up to the database
    with market_prices_table.batch_writer() as batch:
        for i in klines:
            batch.put_item(
                Item={
                    'token_asset': token+"_"+asset,
                    'open_time': i[0],
                    'open_price': i[1],
                    'high_price': i[2],
                    'low_price': i[3],
                    'close_price': i[4],
                    'volume': i[5],
                    'close_time': i[6],
                    'quote_asset_volume': i[7],
                    'number_of_trades': i[8],
                    'taker_buy_base_asset_volume': i[9],
                    'taker_buy_quote_asset_volume': i[10]
                }
            )
    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} seconds')
    return


app.run()

# bot = {
#     "id": "123",
#     "name": "Bob",
#             "buy_behaviors": {
#                 "group_conditional": "or",
#                 "group": [
#                     {
#                         "group_conditional": "and",
#                         "group": [
#                             {
#                                 "function": "moving_average",
#                                 "inputs": {
#                                     "interval": 200
#                                 },
#                                 "conditional": "greater_than",
#                                 "target": "current_price"
#                             },
#                             {
#                                 "function": "moving_dx",
#                                 "inputs": {
#                                     "interval": 50
#                                 },
#                                 "conditional": "less_than",
#                                 "target": "0.996"
#                             }
#                         ]
#                     }
#                 ]
#             },
#     "sell_behaviors": {
#                 "group_conditional": "or",
#                 "group": [
#                     {
#                         "group_conditional": "and",
#                         "group": [
#                             {
#                                 "function": "support",
#                                 "inputs": {
#                                     "interval": 200
#                                 },
#                                 "conditional": "less_than",
#                                 "target": "current_price"
#                             },
#                             {
#                                 "function": "moving_dx",
#                                 "inputs": {
#                                     "interval": 50
#                                 },
#                                 "conditional": "greater_than_or_equal_to",
#                                 "target": "1.12"
#                             }
#                         ]
#                     }
#                 ]
#             }
# }
