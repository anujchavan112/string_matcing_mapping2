from flask import request,jsonify
from flask_restful import Resource
from fuzzywuzzy import fuzz
import random
import pickle
import pandas as pd
import numpy as np
import pathlib
import json
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import find_train_token

class Prediction(Resource):
    def get(self):
        return {"Prediction":"GET"}

    def put(self):
        return {"Prediction":"PUT"}

    def post(self):
        #getting data from user
        data = request.get_json(force=True)

        model_file=pathlib.Path("model.svc")
        #checking if trained model is available
        if model_file.exists():
            model=pickle.load(open(model_file, 'rb'))
            Source_fields=data['source']['formatFields']
            Target_fields=data['target']['formatFields']

            response_data = {
                "sourceFormatName":data['source']['formatName'],
                "targetFormatName":data['target']['formatName'],
                "overallConfidence":0,
                "mappings":[]
            }

            sourceTokens=[]
            mappings=[]
            overallConfidence=0

            for i in range(len(Source_fields)):
                sourcefield=Source_fields[i]

                source_Tokens=find_train_token.findtokens(sourcefield)
                temp=""

                for token in source_Tokens:

                    sourcet=token.lower()
                    SrVals=find_train_token.converttonumber([sourcet])
                    result=find_train_token.predicttoken(SrVals)
                    temp="{}{}".format(temp,result[0])

                max=0

                for tstring in Target_fields:
                    confidance=fuzz.ratio(temp.lower(),tstring.lower())
                    if  confidance>max:
                        max=confidance

                overallConfidence +=max

                temp_dict={
                    "sourceField":sourcefield,
                    "targetField":temp,
                    "confidence":max
                }
                mappings.append(temp_dict)
                #filling the mappings

            totalconfidance=overallConfidence/len(Source_fields)

            response_data['overallConfidence']=totalconfidance
            response_data['mappings']=mappings

        else:
            response_data = {
                "sourceFormatName":data['source']['formatName'],
                "targetFormatName":data['target']['formatName'],
                "Message":"Please train the model first"
            }
        return jsonify(response_data)


