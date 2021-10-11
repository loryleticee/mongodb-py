import sys, re, json
from datetime import datetime
from dotenv import dotenv_values
import ast

ip_adress = sys.argv[1][:-3]
_responses=dict()
_datas=dict()
def BDD():
    from pymongo import MongoClient
    config = dotenv_values(".env")
    CONNECTION_STRING = 'mongodb://'+config["USER"] +':'+ config["MDP"] +'@'+ config["IP"] +':'+ config["PORT"] +'/'+ config["BDD"]
    client = MongoClient(CONNECTION_STRING)

    return client[config["BDD"]]

def GET_USER( _sDB, _oQY={}, _sSort='', _nOrder= '', _nLimit= '' ):
    global _responses
    global _datas
    try:
        _responses = BDD().get_collection(_sDB).find(_oQY).sort(_sSort, _nOrder).limit(_nLimit)
        if isinstance(_responses[0], dict) == False:
            raise Exception("Error on query")
    except Exception as error:
        print(repr(error))

    for i, response in enumerate(_responses):
        _datas.update({'{}'.format(i) :response})
    return _datas["0"]

def SET_LAST_CONNECT():
    global ip_adress
    SET = {"$set": { "last_connection": datetime.now() }}
    where = {"ip": {"$regex":ip_adress[:-6]}}
    run_update = BDD().get_collection("client").update_many(where, SET)

# This is added so that many files can reuse the function BDD()
if __name__ == "__main__":
    _sQuery = {"last_connection": {"$lt": datetime.now()}}
    _oResp = GET_USER("client", _sQuery, "last_connection", -1, 1)
    if "name" in _oResp:
        print("{} {} at: {} {}".format(_oResp['name'], _oResp['ip'], _oResp['last_connection'], "Europe/Paris"))
    if "error" in _oResp:
        print("{}".format(_oResp))

    SET_LAST_CONNECT()
