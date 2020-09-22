import json
import pickle
import pandas as pd
import numpy as np
import random
import pathlib
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier


def findtokens(Sourcestring):
    #checking for the special charcters in the string

    if "_" in Sourcestring:
        return  Sourcestring.split("_")

    elif " " in Sourcestring:
        return  Sourcestring.split(" ")

    elif "-" in Sourcestring:
        return  Sourcestring.split("-")
    else :
        #checking for the camelcase
        get_tokens=[]
        tempString=""
        Sourcelen=len(Sourcestring)
        allcaps=False
        #find if there are all caps
        for  i in range(Sourcelen):
            if (Sourcestring[i].isupper()):
                allcaps=True
            else:
                allcaps=False


        if not allcaps:
            for j in range(Sourcelen):
                if (Sourcestring[j].isupper()):
                    if len(tempString)>0:
                        get_tokens.append(tempString)
                    tempString="{}".format(Sourcestring[j])

                else:
                    tempString="{}{}".format(tempString,Sourcestring[j])
                    if Sourcelen==(j+1):
                        get_tokens.append(tempString)

        else:
            get_tokens.append(Sourcestring)

        return get_tokens


def converttonumber(source_field):
    '''
    convert the string to unique numbers
    '''
    SourceValues=[]
    for i in source_field:
        temp=""
        for j in i:
            temp="{}{}".format(temp,ord(j.lower()))
        SourceValues.append(int(temp))
    return SourceValues




def traintokens():
    '''
    training the token dataset
    '''
    with open("tokens.json",'r') as openfile:
        json_object=json.load(openfile)

    Source_token=[]
    Target_token=[]

    for i in json_object:
        Target_token.append(i['target'])
        Source_token.append(i['match'])

    Sc_values=converttonumber(Source_token)


    Sc_train=np.array(Sc_values).reshape(-1,1)
    '''
    knn = KNeighborsClassifier(n_neighbors=1, metric='euclidean')
    knn.fit(Sc_train,Target_token)
    model_file='model.pkl'
    pickle.dump(knn,open(model_file,'wb'))
    '''
    svc_model=SVC(kernel='rbf',random_state=1,gamma=5.0,C=1.0)
    svc_model.fit(Sc_train,Target_token)
    model_file='model.svc'
    pickle.dump(svc_model,open(model_file,'wb'))


def predicttoken(Src_vals):
    '''
    prediction of the values of token
    '''

    svc_file =pickle.load(open('model.svc','rb'))
    prediction_result=svc_file.predict(np.array(Src_vals).reshape(-1,1))
    return prediction_result
'''
    knn_file =pickle.load(open('model.pkl','rb'))
    prediction_result=knn_file.predict(np.array(Src_vals).reshape(-1,1))
    return prediction_result


print(converttonumber('linkFskfdfs'))00
print(findtokens('LinkedDale'))
'''
