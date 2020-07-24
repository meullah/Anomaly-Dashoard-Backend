import pyodbc
import urllib
import sqlalchemy as sal
from sqlalchemy import create_engine
import pandas as pd
import datetime
import openMRS_API as mr
import requests
from requests.auth import HTTPBasicAuth

def home_get_monthly_anomalies():
    connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
    engine = sal.create_engine(connection_uri)
    engine.connect()
    Table_names = ['accepted_anomalies', 'pended_anomalies', 'rejected_anomalies']
    data = dict()
    d = pd.DataFrame()
    for table in Table_names:
        sql_query = pd.read_sql_query('SELECT * FROM {}'.format(table), engine)
        df = pd.DataFrame(sql_query, columns = ['ID', 'DateTime'])
        df['Table_name'] = table
        d = d.append(df)
    if len(d) == 0:
        return {'accepted_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0],
        'pended_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0],
        'rejected_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0]}
    year = d.sort_values('DateTime').iloc[-1]['DateTime'].year
    d = d.set_index('DateTime')
    d = d.loc[str(year)]
    for table in Table_names:
        d_curr = d[d['Table_name']==table].resample('M').count().reset_index()
        d_curr['Month'] = pd.DatetimeIndex(d_curr['DateTime']).month-1
        arr = [0 for i in range(12)]
        for i in d_curr[['Table_name', 'Month']].values:
            arr[i[1]] = int(i[0])
        data[table] = arr
    # d.resample('M').count()
    print("-"*100)
    print(data)
    return data

def home_get_total_anomalies():
    connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
    engine = sal.create_engine(connection_uri)
    engine.connect()
    Table_names = ['accepted_anomalies', 'pended_anomalies', 'rejected_anomalies']
    data = {'labels' : [],'data' : []}

    for table in Table_names:
        sql_query = pd.read_sql_query('SELECT * FROM {}'.format(table), engine)
        df = pd.DataFrame(sql_query, columns = ['ID', 'DateTime'])
        data['labels'].append(table)
        data['data'].append(len(df))
    return data

def home_symptom_diagnosis_anomalies():
    connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
    engine = sal.create_engine(connection_uri)
    engine.connect()
    Table_names = ['accepted_anomalies', 'pended_anomalies', 'rejected_anomalies']
    data = {}
    d = pd.DataFrame()
    for table in Table_names:
        sql_query = pd.read_sql_query('SELECT * FROM {}'.format(table), engine)
        df = pd.DataFrame(sql_query, columns = ['ID', 'DateTime', 'Type'])
        df = df[df['Type'] == 'SD']
        df['Table_name'] = table
        d = d.append(df)
    if len(d) == 0:
        return {'accepted_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0],
        'pended_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0],
        'rejected_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0]}
    year = d.sort_values('DateTime').iloc[-1]['DateTime'].year
    d = d.set_index('DateTime')
    d = d.loc[str(year)]
    for table in Table_names:
        d_curr = d[d['Table_name']==table].resample('M').count().reset_index()
        d_curr['Month'] = pd.DatetimeIndex(d_curr['DateTime']).month-1
        arr = [0 for i in range(12)]
        for i in d_curr[['Table_name', 'Month']].values:
            arr[i[1]] = int(i[0])
        data[table] = arr
    return data

def home_diagnosis_procedure_anomalies():
    connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
    engine = sal.create_engine(connection_uri)
    engine.connect()
    Table_names = ['accepted_anomalies', 'pended_anomalies', 'rejected_anomalies']
    data = {}
    d = pd.DataFrame()
    for table in Table_names:
        sql_query = pd.read_sql_query('SELECT * FROM {}'.format(table), engine)
        df = pd.DataFrame(sql_query, columns = ['ID', 'DateTime', 'Type'])
        df = df[df['Type'] == 'DP']
        df['Table_name'] = table
        d = d.append(df)
    if len(d) == 0:
        return {'accepted_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0],
        'pended_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0],
        'rejected_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0]}
    year = d.sort_values('DateTime').iloc[-1]['DateTime'].year
    d = d.set_index('DateTime')
    d = d.loc[str(year)]
    for table in Table_names:
        d_curr = d[d['Table_name']==table].resample('M').count().reset_index()
        d_curr['Month'] = pd.DatetimeIndex(d_curr['DateTime']).month-1
        arr = [0 for i in range(12)]
        for i in d_curr[['Table_name', 'Month']].values:
            arr[i[1]] = int(i[0])
        data[table] = arr
    return data

def patient_symptom_diagnosis_anomalies(openMRS_id):
    uuid = mr.get_uuid(openMRS_id)
    if uuid:
        print("*"*100,uuid)
        connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
        engine = sal.create_engine(connection_uri)
        engine.connect()
        Table_names = ['accepted_anomalies', 'pended_anomalies', 'rejected_anomalies']
        data = {}
        d = pd.DataFrame()
        for table in Table_names:
            sql_query = pd.read_sql_query('SELECT * FROM {}'.format(table), engine)
            df = pd.DataFrame(sql_query, columns = ['ID', 'DateTime', 'Type', 'Patient_ID'])
            df = df[df['Type'] == 'SD']
            df = df[df['Patient_ID'] == uuid]
            df['Table_name'] = table
            d = d.append(df)
        
        if len(d) == 0:
            return {'accepted_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0],
            'pended_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0],
            'rejected_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0]}
        year = d.sort_values('DateTime').iloc[-1]['DateTime'].year
        d = d.set_index('DateTime')
        d = d.loc[str(year)]
        for table in Table_names:
            d_curr = d[d['Table_name']==table].resample('M').count().reset_index()
            d_curr['Month'] = pd.DatetimeIndex(d_curr['DateTime']).month-1
            arr = [0 for i in range(12)]
            for i in d_curr[['Table_name', 'Month']].values:
                arr[i[1]] = int(i[0])
            data[table] = arr
        return data
    else:
        return None

def patient_diagnosis_procedure_anomalies(openMRS_id):
    uuid = mr.get_uuid(openMRS_id)
    if uuid:
        connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
        engine = sal.create_engine(connection_uri)
        engine.connect()
        Table_names = ['accepted_anomalies', 'pended_anomalies', 'rejected_anomalies']
        data = {}
        d = pd.DataFrame()
        for table in Table_names:
            sql_query = pd.read_sql_query('SELECT * FROM {}'.format(table), engine)
            df = pd.DataFrame(sql_query, columns = ['ID', 'DateTime', 'Type', 'Patient_ID'])
            df = df[df['Type'] == 'DP']
            df = df[df['Patient_ID'] == uuid]
            df['Table_name'] = table
            d = d.append(df)
        
        print('*'*100)
        print(d)
        print('*'*100)
        if len(d) == 0:
            return {'accepted_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0],
            'pended_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0],
            'rejected_anomalies': [0,0,0,0,0,0,0,0,0,0,0,0]}
        year = d.sort_values('DateTime').iloc[-1]['DateTime'].year
        d = d.set_index('DateTime')
        d = d.loc[str(year)]
        for table in Table_names:
            d_curr = d[d['Table_name']==table].resample('M').count().reset_index()
            d_curr['Month'] = pd.DatetimeIndex(d_curr['DateTime']).month-1
            arr = [0 for i in range(12)]
            for i in d_curr[['Table_name', 'Month']].values:
                arr[i[1]] = int(i[0])
            data[table] = arr
        return data
    
    else:
        return None

def add_rule(seq_0,seq_1,type_):
    connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
    engine = sal.create_engine(connection_uri)
    engine.connect()
    result = engine.execute("INSERT INTO manual_rules (Seq_1,Seq_0,Type) VALUES('{}','{}','{}')".format(seq_0,seq_1,type_))
    return result

def accept_anomaly(anomaly_id,reason):
    connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
    engine = sal.create_engine(connection_uri)
    engine.connect()
    print("*"*100,reason)
    result = engine.execute('update current_anomalies set Description = "{}" where ID ={}'.format(reason,anomaly_id))
    result = engine.execute('Insert into accepted_anomalies (Visit_ID, Patient_ID, DateTime, Anomaly_On, Type,Reason) Select Visit_ID, Patient_ID, DateTime, Anomaly_On, Type, Description From current_anomalies Where ID = {}'.format(anomaly_id))
    result = engine.execute('DELETE FROM current_anomalies WHERE ID = {}'.format(anomaly_id))
    
    return result

def pend_anomaly(anomaly_id,reason):
    connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
    engine = sal.create_engine(connection_uri)
    engine.connect()
    result = engine.execute('update current_anomalies set Description = "{}" where ID ={}'.format(reason,anomaly_id))
    result = engine.execute('Insert into pended_anomalies (Visit_ID, Patient_ID, DateTime, Anomaly_On, Type,Reason) Select Visit_ID, Patient_ID, DateTime, Anomaly_On, Type,Description From current_anomalies Where ID = {}'.format(anomaly_id))
    result = engine.execute('DELETE FROM current_anomalies WHERE ID = {}'.format(anomaly_id))
    return result

def reject_anomaly(anomaly_id,reason):
    connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
    engine = sal.create_engine(connection_uri)
    engine.connect()
    result = engine.execute('update current_anomalies set Description = "{}" where ID ={}'.format(reason,anomaly_id))
    result = engine.execute('Insert into rejected_anomalies (Visit_ID, Patient_ID, DateTime, Anomaly_On, Type,Reason) Select Visit_ID, Patient_ID, DateTime, Anomaly_On, Type, Description From current_anomalies Where ID = {}'.format(anomaly_id))
    result = engine.execute('DELETE FROM current_anomalies WHERE ID = {}'.format(anomaly_id))

    return result

def Check_Anomaly(d):
    services = d['services']
    diagnosis = d['diagnosis']
    connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
    engine = sal.create_engine(connection_uri)
    engine.connect()
    for service in services:
        res = engine.execute("SELECT Frequency FROM frequency WHERE ICD_Code = '{}'".format(service))
        frequency = 0
        for r in res:
            frequency = r[0]
        print("*"*100,service)
        print("*"*100,frequency)
        print("*"*100,frequency>200)
        if frequency>200:
            res = engine.execute("SELECT COUNT(*) FROM manual_rules WHERE Seq_0 ='{}' AND Seq_1 in ({})".format(service, str(diagnosis)[1:-1]))
            count = 0
            for r in res:
                count = r[0]
            print("*"*100,count)
            if count == 0:
                res = engine.execute("SELECT COUNT(*) FROM generated_rules WHERE Seq_0 ='{}' AND Seq_1 in ({})".format(service, str(diagnosis)[1:-1]))
                count = 0      
                for r in res:
                    count = r[0]
                print("*"*100,count)
                if count == 0:
                    res = engine.execute("INSERT INTO current_anomalies (Visit_ID,Patient_ID,DateTime,Anomaly_On,Type)\
                    VALUES('{}','{}','{}','{}','{}')".format(d['visit_uuid'],d['patient_uuid'],datetime.datetime.now(), service, 'DP'))


def get_notifications():
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

    return mylist

def get_anomalyData(anomaly_id):
    
    connection_uri = "mysql+pymysql://root:2403@localhost:3306/ai_engine"
    engine = sal.create_engine(connection_uri)
    engine.connect()

    sql_query = pd.read_sql_query("select * from current_anomalies where ID = '{}'".format(7),engine)

    res = sql_query.transpose().to_dict()[0]

    return res
