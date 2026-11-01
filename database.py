from pymongo import MongoClient
import pandas as pd
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import os
import visualization
import sys


def mongodbConncect():
    datalink=os.environ.get("DATABASE_LINK")
    if not datalink:
        raise RuntimeError("DATABASE_LINK must be configured to use MongoDB")
    myclient =MongoClient(datalink)
    mydb = myclient["Heartpatientdatabase"] 
    mycol = mydb["Heart_Data"]
    
    # df=pd.DataFrame(list(mycol.find({})))
    # print(df.head())
    
    return mycol



def crudprocess(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal,result):   
    sex = {"male": 1, "female": 0}[sex.strip().lower()]
    cp = {"typical angina": 0, "atypical angina": 1, "non-anginal pain": 2,
          "asymptomatic": 3}[cp.strip().lower()]
    exang = {"yes": 1, "no": 0}[exang.strip().lower()]
    fbs = {"yes": 1, "no": 0}[fbs.strip().lower()]
    slope = {
        "upsloping: better heart rate with excercise(uncommon)": 0,
        "flatsloping: minimal change(typical healthy heart)": 1,
        "downsloping: signs of unhealthy heart": 2,
    }[slope.strip().lower()]
    thal = {
        "fixed defect: used to be defect but ok now": 6,
        "reversable defect: no proper blood movement when excercising": 7,
        "normal": 3,
    }[thal.strip().lower()]
    restecg = {
        "nothing to note": 0,
        "st-t wave abnormality": 1,
        "possible or definite left ventricular hypertrophy": 2,
    }[restecg.strip().lower()]
    data_dict={"age":int(age),"sex":int(sex),"cp":int(cp),"trestbps":int(trestbps),"restecg":int(restecg),"chol":int(chol),"fbs":int(fbs),"thalach":int(thalach),"exang":int(exang),"oldpeak":float(oldpeak),"slope":int(slope),"ca":int(ca),"thal":int(thal),"target":int(result)}
    return data_dict




def crudOperation(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal,result):
    data_dict=crudprocess(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal,result)
    data1=json.dumps(data_dict,separators=(',', ':'), sort_keys=True)
    value = json.loads(data1)
    try:
        mycol=mongodbConncect()
        mycol.insert_one(value)
        print('Inserted 1 data to database')
    except:
        print('unable to insert', file=sys.stderr)



# if __name__ == '__main__':
#     crudOperation(39,"male","Non-anginal pain",130,"ST-T Wave abnormality",250,"Yes",187,"Yes",2,"Downsloping: signs of unhealthy heart",2,"normal",1)
#     # mongodbConncect()
#     # print("hi")
