import pymysql
import urllib
import sqlalchemy as sal
from sqlalchemy import create_engine
import pandas as pd
import json

import datetime,json
import requests
from requests.auth import HTTPBasicAuth


    
def accept_anomaly(anomaly_id,reason):
    connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
    engine = sal.create_engine(connection_uri)
    engine.connect()
    print("*"*100,reason)
    result = engine.execute('Insert into accepted_anomalies (Visit_ID, Patient_ID, DateTime, Anomaly_On, Type) Select Visit_ID, Patient_ID, DateTime, Anomaly_On, Type From current_anomalies Where ID = {}'.format(anomaly_id))
    result = engine.execute('DELETE FROM current_anomalies WHERE ID = {}'.format(anomaly_id))
    result = engine.execute('update accepted_anomalies set Reason = "{}" where ID ={}'.format(reason,anomaly_id))
    
    
    return result

accept_anomaly()