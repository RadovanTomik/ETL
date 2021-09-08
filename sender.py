import requests
from crontab import CronTab

with CronTab(user='radot') as cron:
    job = cron.new(command='echo hello_world')
    job.minute.every(1)
print('cron.write() was just executed')

def sendData():
    headers = {
        'Content-Type': 'application/json',
    }

    data = './FHIRs/export.json'

    response = requests.post('http://localhost:8080/fhir', headers=headers, data=data)
    return response