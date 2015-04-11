from flask import Flask
import twilio.twiml
 
app = Flask(__name__)
 
INTRO_TEXT = '''
Press 1 for English, 2 for Amharic, 3 for Bengali, 4 for Hindi, 5 for Indonesian, 6 for Malayalam, 7 for Mandarin, 8 for Nepali, 9 for Sinhalese, 10 for Tagalog, 11 for Tamil, 12 for Telugu
'''

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():

	'''debugging'''
	print request

	'''Save data about user'''
	data_blob = {}
	data_blob["from_number"] = request.values.get('From', None)
	send_data(data_blob)

	'''Interact with user'''
    resp = twilio.twiml.Response()
    resp.say(INTRO_TEXT)
 
    return str(resp)
 
def send_data(blob):
	import json,httplib
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('POST', '/1/classes/GameScore', json.dumps(blob), {
	       "X-Parse-Application-Id": "2W6rB0trZRZNa0jyrcbvFGoI8yN7PXqs8L6z4DQi",
	       "X-Parse-REST-API-Key": "kK8riCXFGptYwPbrc100DSxFBe4aAijY1OctNEF6",
	       "Content-Type": "application/json"
	     })
	result = json.loads(connection.getresponse().read())
	print result



if __name__ == "__main__":
    app.run(debug=True)

