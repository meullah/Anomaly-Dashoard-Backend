import pymysql
import urllib
import sqlalchemy as sal
from sqlalchemy import create_engine
import pandas as pd
import json

import datetime,json
import requests
from requests.auth import HTTPBasicAuth


    

connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
engine = sal.create_engine(connection_uri)
engine.connect()

sql_query = pd.read_sql_query("select * from current_anomalies",engine)
res = sql_query.transpose().to_dict()

mylist = []
for key,values in res.items():
    
    url = "http://localhost:8080/openmrs-standalone/ws/rest/v1/patient/{}?v=custom:display".format(values['Patient_ID'])
    res = requests.get(url,auth=HTTPBasicAuth('meullah', 'Ehsan@123')).json()
    values['Patient_ID'] = res['display'][:6]
    mylist.append(values)

print(mylist)
