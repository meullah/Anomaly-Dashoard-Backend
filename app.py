from flask import Flask, jsonify,request
from flask_restful import Api, Resource
from flask_cors import CORS
import DataBase as db
import openMRS_API as mr
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

class Home(Resource):
    def get(self):
        # data = db.accept_anomaly(7)
        return jsonify("Hello")


class Home_MonthlyAnomalies(Resource):
    def get(self):
        data = db.home_get_monthly_anomalies()
        return jsonify({"data":data})


class Home_TotalAnomalies(Resource):
    def get(self):
        data = db.home_get_total_anomalies()
        return jsonify(data)


class Home_SymptomToDiagnosisAnomalies(Resource):
    def get(self):
        data = db.home_symptom_diagnosis_anomalies()
        return jsonify(data)

class Home_DiagnosisToProcedureAnomalies(Resource):
    def get(self):
        data = db.home_diagnosis_procedure_anomalies()
        return jsonify(data)


class Patient(Resource):
    def get(self):
        return jsonify({"name":"Hamza","age":22})


class Patient_SymptomToDiagnosisAnomalies(Resource):
    def get(self,uuid):
        data = db.patient_symptom_diagnosis_anomalies(uuid)
        return jsonify(data)



class Patient_DiagnosisToProcedureAnomalies(Resource):
    def get(self,uuid):
        data = db.patient_diagnosis_procedure_anomalies(uuid)
        return jsonify(data)

        


class Patient_EncouterRecords(Resource):
    def get(self,openMRS_id):
        if openMRS_id != 'null':
            if not openMRS_id.isnumeric():
                res = mr.getPatientsVisits(openMRS_id)
                return jsonify(res)
            else:
                return jsonify("invalid patient ID")
        

class AddRule(Resource):  ##Manage Add Rule Here
    def post(self):
        data = request.get_json(force=True)
        Type = ''
        if data['tor'] == 'Symptom to Diagnosis Rule':
            Type = 'SD'
        else:
            Type = 'DP'
        
        seq_0 = data['rules']['SDR']  
        seq_1 = data['rules']['DSR']

        # print("*"*100,seq_0,seq_1,Type)
        db.add_rule(seq_0, seq_1, Type)

        return jsonify("OK")

class Accept_Anomaly(Resource):
    def post(self):
        data = request.get_json(force=True)
        print(data)
        ID = data['anomaly_id']
        comment = data['reason']

        if data['explanation']['accept'] == 'true':
            res = db.accept_anomaly(ID,comment)
        elif data['explanation']['pend'] == 'true':
            res = db.pend_anomaly(ID,comment)        
        else:
            res = db.reject_anomaly(ID,comment)
    

        # ID = request.form['id']
        # comment = request.form['comment']
        # data = db.accept_anomaly(ID)
        return jsonify("Done")
        

# class Reject_Anomaly(Resource):
#     def post(self):
#         data = request.get_json(force=True)
#         print(data)
#         # ID = request.form['id']
#         # comment = request.form['comment']
#         # data = db.pend_anomaly(ID)
#         return jsonify("Done")

# class Pend_Anomaly(Resource):
#     def post(self):
#         data = request.get_json(force=True)
#         print(data)
#         # ID = request.form['id']
#         # comment = request.form['comment']
#         # data = db.reject_anomaly(ID)
#         return jsonify("Done")

class generate_anomalies(Resource):
    def get(self):
        res = mr.getCompletedVisits()
        for myDict in res:
            db.Check_Anomaly(myDict)
    
        return res


class get_Notifications(Resource):
    def get(self):
        notifications = db.get_notifications()

        return jsonify(notifications)

class get_Anomaly(Resource):
    def get(self,id):
        data = request.get_json()
        print(data)
        res = db.get_anomalyData(id)

        return jsonify(res)



api.add_resource(Home,'/home')
api.add_resource(Home_MonthlyAnomalies,'/HMA')
api.add_resource(Home_TotalAnomalies,'/HTA')
api.add_resource(Home_SymptomToDiagnosisAnomalies,'/HSDA')
api.add_resource(Home_DiagnosisToProcedureAnomalies,'/HDPA')
api.add_resource(Patient_SymptomToDiagnosisAnomalies,'/PSDA/uuid/<string:uuid>')
api.add_resource(AddRule,'/add/rule')
api.add_resource(Accept_Anomaly,'/performedAction')


api.add_resource(Patient_DiagnosisToProcedureAnomalies,'/PDSA/uuid/<string:uuid>')

api.add_resource(Patient_EncouterRecords,'/PER/patient_id/<string:openMRS_id>')
api.add_resource(generate_anomalies,'/generateanomalies')
api.add_resource(get_Notifications,'/getnotifications')
api.add_resource(get_Anomaly,'/getanomalydata/anomaly_id/<int:id>')



if __name__ == "__main__":
    app.run(host="localhost", debug=True)