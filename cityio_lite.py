#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Jul  2 16:28:20 2020

@author: doorleyr
"""

from flask import Flask, request, jsonify, Response
import datetime
import json
from flask_cors import CORS
import sys
import hashlib

app = Flask(__name__)
CORS(app)

table_names = [n for n in sys.argv[1:len(sys.argv)]]
tables={}

for table_name in table_names:
    print('Loading {}'.format(table_name))
    tables[table_name]=json.load(open('base/{}_base.json'.format(table_name)))

def dict_to_hash(the_dict):
    return hashlib.sha224(json.dumps(the_dict).encode()).hexdigest()

@app.route('/api/table/<table_name>/<field>/',methods = [ 'POST', 'DELETE'])
def post_field(table_name, field):
    if request.method=='POST':
        data=json.loads(request.data.decode())
        resp=Response(status=200)
        tables[table_name][field]=data
        now_ts=str(datetime.datetime.now().timestamp())
        tables[table_name]['meta']['hashes'][field]=dict_to_hash(tables[table_name][field])
        tables[table_name]['meta']['id']=dict_to_hash(tables[table_name]['meta']['hashes'])
        tables[table_name]['meta']['timestamp']=now_ts
        return resp
    else:
        if field in tables[table_name]:
            del tables[table_name][field]
            del tables[table_name]['meta']['hashes'][field]
            return Response(status=200)
        else:
            return Response(status=200)

@app.route('/api/table/<table_name>/<field>/',methods = ['GET']) 
def get_field(table_name, field):
    return jsonify(tables[table_name][field]), 200

@app.route('/api/table/<table_name>/<field>/<subfield>/',methods = ['GET']) 
def get_sub(table_name, field, subfield):
    return jsonify(tables[table_name][field][subfield]), 200

@app.route('/api/table/<table_name>/<field>/<subfield>/<subsubfield>/',methods = ['GET']) 
def get_sub_sub(table_name, field, subfield, subsubfield):
    return jsonify(tables[table_name][field][subfield][subsubfield]), 200

if __name__ == '__main__':
   app.run(debug = True)
