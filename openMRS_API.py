import datetime,json
import requests
from requests.auth import HTTPBasicAuth
import json
import pickle
RECENT_DATETIME = pickle.load( open( "RecentDateTime.p", "rb" ) )


def get_uuid(openMRS_id):
    patient_openMRS_id = openMRS_id
    get_uuid = 'http://localhost:8080/openmrs-standalone/ws/rest/v1/patient?q={}&&v=custom:uuid'.format(patient_openMRS_id)
    res = requests.get(get_uuid,auth=HTTPBasicAuth('meullah', 'Ehsan@123')).json()

    if res['results'] == []:
        return None
    else:
        return res['results'][0]['uuid']

def getPatientsVisits(openMRS_id):

    patient_openMRS_id = openMRS_id
    # get_uuid = 'http://localhost:8080/openmrs-standalone/ws/rest/v1/patient?q={}&&v=custom:uuid'.format(patient_openMRS_id)
    # res = requests.get(get_uuid,auth=HTTPBasicAuth('meullah', 'Ehsan@123')).json()

    patient_uuid = get_uuid(openMRS_id)

    # print("** "*100,patient_uuid)
    if patient_uuid !=  None:
        visits_url = "http://localhost:8080/openmrs-standalone/ws/rest/v1/visit?patient={}&&v=full".format(patient_uuid)
        res = requests.get(visits_url,auth=HTTPBasicAuth('meullah', 'Ehsan@123')).json()
        # data = res['results'][0]['encounters']

        # visit = [patient_uuid,patient_openMRS_id]
        visit = []
        for data in res['results']:
            temp = {}
            diagnosis_links  =[]
            providers_list=[]
            
            temp['visit_id'] = data['uuid']
            temp['start_date'] = data['startDatetime']
            temp['end_date'] = data['stopDatetime']
            temp['services'] = []
            temp['symptoms'] = []
            temp['diagnosis'] = []
            for encounter in data['encounters']:
                print('%^%'*100,encounter)
                for provider in encounter['encounterProviders']:
                    if provider['display'].split(':')[0] not in providers_list:
                        providers_list.append(provider['display'].split(':')[0]) 
                        
                if not encounter['form'] is None:
                    if encounter['form']['display']=='Lab Exam':
                        temp['services']+= encounter['obs'][0]['display'][24:].split(',')
                    elif encounter['form']['display']=='Visit Note':
                        if encounter['obs'] != []:
                            temp['symptoms'] += encounter['obs'][0]['display'][24:].split(',')
                        for j in encounter['diagnoses']:
                            diagnosis_links.append(j['links'][0]['uri'])
                else:
                    if encounter['obs'] != []:
                        temp['symptoms'] += encounter['obs'][0]['display'][24:].split(',')
                    for j in encounter['diagnoses']:
                        diagnosis_links.append(j['links'][0]['uri'])


                for url in diagnosis_links:
                    res = requests.get(url,auth=HTTPBasicAuth('meullah', 'Ehsan@123')).json()
                    # print(url)
                    if 'coded' in res['diagnosis']:
                        for i in res['diagnosis']['coded']['mappings']:
                            if i['display'][:3] == 'ICD':
                                temp['diagnosis'].append(i['display'][12:])
                    else:
                        temp['diagnosis'].append(res['diagnosis']['nonCoded'])

                                

            temp['providers'] = providers_list

            visit.append(temp)

        return visit
    else:
        return "none"

def getCompletedVisits():

    global RECENT_DATETIME
    newVisits = []

    req_url = 'http://localhost:8080/openmrs-standalone/ws/rest/v1/visit?includeInactive=true&fromStartDate={}&&v=full'.format(RECENT_DATETIME)
    
    RECENT_DATETIME = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

    pickle.dump(RECENT_DATETIME, open( "RecentDateTime.p", "wb" ))

    res = requests.get(req_url,auth=HTTPBasicAuth('meullah', 'Ehsan@123')).json()

    # print(res['results'][0].keys())

    for visit in res['results']:
        visit_dict = {'visit_uuid' : visit['uuid'],'patient_uuid' : visit['patient']['uuid']} 
        visit_dict['start_datetime'] = visit['startDatetime']
        visit_dict['stop_datetime'] = visit['stopDatetime']
        visit_dict['services'] = []
        visit_dict['symptoms'] = []
        visit_dict['diagnosis'] = []
        diagnosis_links = []
        for encounter in visit['encounters']:
            if encounter['form']['display']=='Lab Exam':
                visit_dict['services'] += encounter['obs'][0]['display'][24:].split(',')
            elif encounter['form']['display']=='Visit Note':
                if encounter['obs'] != []:
                    visit_dict['symptoms'] += encounter['obs'][0]['display'][24:].split(',')
                for j in encounter['diagnoses']:
                    diagnosis_links.append(j['links'][0]['uri'])
        
        for url in diagnosis_links:
                res = requests.get(url,auth=HTTPBasicAuth('meullah', 'Ehsan@123')).json()
                # print(url)
                if 'coded' in res['diagnosis']:
                    for i in res['diagnosis']['coded']['mappings']:
                        if i['display'][:3] == 'ICD':
                            visit_dict['diagnosis'].append(i['display'][12:])

                else:
                    visit_dict['diagnosis'].append(res['diagnosis']['nonCoded'])
        

        newVisits.append(visit_dict)

    completedVists = []

    for data in newVisits:
        if data['stop_datetime'] is not None:
            completedVists.append(data)


    return completedVists