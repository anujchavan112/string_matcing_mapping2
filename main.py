from flask import Flask, json,request
from flask_restful import Api, Resource
from match_cofidance import match_Confidance
from mapping_learn import mapping_Learn
from prediction import Prediction

app = Flask(__name__)
main=Api(app)

main.add_resource(match_Confidance,'/train/format/match')
main.add_resource(mapping_Learn,'/train/format/learn')
main.add_resource(Prediction,'/format/match')
if __name__ == '__main__':
    app.run(debug=True,port=5002)
