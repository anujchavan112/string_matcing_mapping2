from fuzzywuzzy import fuzz
from flask import request,jsonify
from flask_restful import Resource

class match_Confidance(Resource):

    def get(self):
        return {"match_Confidence":"GET"}
    def put(self):
        return {"Match_Confidance":"PUT"}
    def post(self):
        try:
            #getting data from user in json form
            request_data=request.get_json(force=True)

            #taking source field
            source_field=request_data['source']['formatFields']

            #taking target field
            target_field=request_data['target']['formatFields']


            mappings=[]
            overallconfidencetotal=0
            #checking the string
            for source_string in source_field:
                max=0
                match={"sourceField":source_string,"targetField":"","confidence":max}
                for target_string in target_field:
                    confidence=fuzz.ratio(source_string.lower(),target_string.lower())
                    if confidence>max:
                        max=confidence
                        match["targetField"]=target_string
                        match["confidence"]=max
                overallconfidencetotal +=max
                mappings.append(match)

            #calculating the overall confidence
            overallconfidence=(overallconfidencetotal/len(source_field))

            #response data in json form
            response_data={
                "sourceFormatName":request_data['source']['formatName'],
			    "targetFormatName":request_data['target']['formatName'],
			    "overallConfidence":overallconfidence,
			    "mappings":mappings
            }
            return jsonify(response_data)



        except KeyError:
            return jsonify(message = "Sample file 'file' missing in POST request")

