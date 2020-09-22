from flask import request,jsonify
from flask_restful import Resource
import random
import pickle
import pandas as pd
import numpy as np
import pathlib
import json
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import find_train_token


class mapping_Learn(Resource):
    def get(self):
        return {"mapping_Learn":"GET"}

    def put(self):
        return {"mapping_Learn":"PUT"}

    def post(self):

        #getting the data
        data=request.get_json(force=True)

        mapping = data['mappings']

        Source_field=[]
        Target_field=[]

        #extract source field an map to target field
        for item in mapping:
            Source_field.append(item["sourceField"])
            Target_field.append(item["targetField"])

        #token initilization
        sourcetokens=[]
        targettokens=[]

        tokenize=[]
        token_dataset=pathlib.Path("tokens.json")


        if token_dataset.exists():
            with open(token_dataset,'r') as openfile:
                json_object=json.load(openfile)
            tokenize=json_object

        for index in range (len(Source_field)):
            sourcefield=Source_field[index]
            targetfield=Target_field[index]
            #getting toekns
            source_tokens=find_train_token.findtokens(sourcefield)
            target_tokens=find_train_token.findtokens(targetfield)

            len_source=len(source_tokens)
            len_target=len(target_tokens)

            if len_source>len_target:
                min_token=len_target
            else:
                min_token=len_source

            for token in range(min_token):
                temp={
                "target":target_tokens[token],
                "match":source_tokens[token].lower()
                }

                tokenize.append(temp)

                #preparing the training data
                targettokens.append(target_tokens[token])
                sourcetokens.append(source_tokens[token].lower())

        with open (token_dataset,"w") as outfile:
            json.dump(tokenize,outfile)

        find_train_token.traintokens()

        #prepare response data
        reponse_data={
            "sourceFormatName":data['source']['formatName'],
            "targetFormatName":data['target']['formatName'],
            "Message":"Learned The Mapping"

        }

        return jsonify(reponse_data)
