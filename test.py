import json,httplib,urllib


LANGUAGEID_TO_LANGUAGE = ['English', 'Amharic', 'Bengali', 'Hindi', 'Indonesian', 'Malayalam', 'Mandarin', 'Nepali', 'Sinhalese', 'Tagalog', 'Tamil', 'Telugu']

CATEGORYID_TO_CATEGORY = ['Intro', 'Visa', 'Slavery', 'Salary', 'Working Conditions', 'Job Loss', 'Going Home', 'Lawful Rights', 'Domestic Work', 'All' ]



import random
import time

def status(lasttime): 


    data_blob = {}
    data_blob['CallDuration'] = str(random.randint(10, 100))
    data_blob['RecordingUrl'] = None
    data_blob['RecordingSid'] = None
    data_blob['RecordingDuration'] = None
    data_blob['From'] = '+'+str(971507902840+random.randint(-10000, 10000))
    data_blob['Language'] = random.sample(LANGUAGEID_TO_LANGUAGE,1)[0]
    data_blob['Category'] = random.sample(CATEGORYID_TO_CATEGORY,1)[0]

    ntime = lasttime+random.randint(0, 86400/2)
    # ntime = 1
    data_blob['Timestamp'] = int(ntime)
    # print data_blob

    send_analytics(data_blob)
    send_data(data_blob, 'Call_Status')
    return ntime

def send_analytics(data):
    import json,httplib
    connection = httplib.HTTPSConnection('61756c73.ngrok.com')
    # connection = httplib.HTTPSConnection('arshidni.meteor.com')

    connection.connect()
    connection.request('POST', '/complaint', json.dumps(data), {
           "Content-Type": "application/json"
         })
    result = json.loads(connection.getresponse().read())
    print result

def send_data(data, obj):
    import json,httplib
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/classes/'+obj, json.dumps(data), {
           "X-Parse-Application-Id": "2W6rB0trZRZNa0jyrcbvFGoI8yN7PXqs8L6z4DQi",
           "X-Parse-REST-API-Key": "kK8riCXFGptYwPbrc100DSxFBe4aAijY1OctNEF6",
           "Content-Type": "application/json"
         })
    result = json.loads(connection.getresponse().read())
    print result

ftime=int(time.time())
for i in range(1000):
	ftime = status(ftime)