from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)
 
BELL_URL = 'https://www.dropbox.com/s/jz0k7w09cleuglk/Bell.mp3?dl=1'
INTRO_URL = ['https://www.dropbox.com/s/keclu5q8sesy685/Press_1_for_English.mp3?dl=1',
             'https://www.dropbox.com/s/h348n615w6kcknz/Press_2_In_Amharic.mp3?dl=1',
             'https://www.dropbox.com/s/tqeetjtvl69b2h5/Press_3_For_Bengali.mp3?dl=1']

INTRO_TEXT = '''
, 4 for Hindi, 5 for Indonesian, 6 for Malayalam, 7 for Mandarin, 8 for Nepali, 9 for Sinhalese, 10 for Tagalog, 11 for Tamil, 12 for Telugu
'''

FURTHER_INFO_TEXT = { 
'1' :
'''
Press 1 for information about Visa, 2 for Slavery information, 3 for Salary information, 4 for Working Conditions, 5 for Losing your job, 6 for Going home, 7 for Rights under law, 8 for Domestic law, 9 for all of the above, 0 for an agent
'''
}

AUDIO = {
    1: [
 '''https://www.dropbox.com/s/xxqui8c0vosdt6r/1-Intro-English.mp3?dl=1''',
 '''https://www.dropbox.com/s/bcxtt9zwp02a3yf/2-Visa-English.mp3?dl=1''',
 '''https://www.dropbox.com/s/3i4zzrfhfr2ylb6/3-Slavery-English.mp3?dl=1''',
 '''https://www.dropbox.com/s/cvxuf2s9y6iqxko/4-Salary-English.mp3?dl=1''',
 '''https://www.dropbox.com/s/na0h40u1p93btrn/5-WorkingConditions-English.mp3?dl=1''',
 '''https://www.dropbox.com/s/rnvydahvggtmpy2/6-LosingYourJob-English.mp3?dl=1''',
 '''https://www.dropbox.com/s/mn1g54b9fdv966a/7-GoingHome-English.mp3?dl=1''',
 '''https://www.dropbox.com/s/s5gd5yiqj4razt5/8-RightsUnderLaw-English.mp3?dl=1''',
 '''https://www.dropbox.com/s/id3x4dx7jyz5ecq/9-Domestic-English.mp3?dl=1''',
 '''https://www.dropbox.com/s/ldt0h0xebcx8sen/10-Contact-English.mp3?dl=1''',
    ],
    4: [
 '''https://www.dropbox.com/s/34bycyegs2z7m38/1-Intro-Hindi.mp3?dl=1''',
 '''https://www.dropbox.com/s/pfyhnjrbimbqhx4/2-Visa-Hindi.mp3?dl=1''',
 '''https://www.dropbox.com/s/f8lw65o3mw0r1u3/3-Slavery-Hindi.mp3?dl=1''',
 '''https://www.dropbox.com/s/bm9nobauq1n5pbk/4-Salary-Hindi.mp3?dl=1''',
 '''https://www.dropbox.com/s/hzbkxxb80eukdz2/5-WorkingConditions-Hindi.mp3?dl=1''',
 '''https://www.dropbox.com/s/xa127eu437gq8z3/6-LosingYourJob-Hindi.mp3?dl=1''',
 '''https://www.dropbox.com/s/esotjrd7gbxi3xg/7-GoingHome-Hindi.mp3?dl=1''',
 '''https://www.dropbox.com/s/e8ht5ifgoc8cft3/8-RightsUnderLaw-Hindi.mp3?dl=1''',
 '''https://www.dropbox.com/s/eyskz82mg9eqyb4/9-Domestic-Hindi.mp3?dl=1''',
 '''https://www.dropbox.com/s/bwjdw220vpgbzyi/10-Contact-Hindi.mp3?dl=1'''
 ]
    
}


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    '''Save data about user'''
    data_blob = {}
    data_blob["new_session"] = True
    data_blob["from_number"] = request.values.get('From', None)
    send_data(data_blob, call)

    '''Interact with user'''
    resp = twilio.twiml.Response()
    resp.play(BELL_URL)

    # Say a command, and listen for the caller to press a key. When they press
    # a key, redirect them to /handle-key.
    with resp.gather(numDigits=2, action="/handle-lang", method="POST") as g:
        for s in INTRO_URL:
            g.play(s)
        g.say(INTRO_TEXT)

    return str(resp)

@app.route("/handle-lang", methods=['GET', 'POST'])
def handle_lang(): 
    digit_pressed = request.values.get('Digits', None)
    '''Save data about user'''
    data_blob = {}
    data_blob["from_number"] = request.values.get('From', None)
    data_blob["digit_pressed"] = digit_pressed
    send_data(data_blob, 'Call')
    # Get the digit pressed by the user
    resp = twilio.twiml.Response()
    if int(digit_pressed) <= 12: 
        with resp.gather(numDigits=1, action="/handle-further-info/"+digit_pressed, method="POST") as g:
            g.say(FURTHER_INFO_TEXT[digit_pressed])
        print FURTHER_INFO_TEXT[digit_pressed]
        return str(resp)
    else :
        return redirect("/")

@app.route("/handle-further-info/<int:lang_id>", methods=['GET', 'POST'])
def handle_further_info(lang_id): 
    print request
    digit_pressed = request.values.get('Digits', None)
    resp = twilio.twiml.Response()
    if (int(digit_pressed)==0):
        resp.say('Volunteer')
        return str(resp)
    elif (int(digit_pressed)==9):
        for i in range(1, 9):
            resp.play(AUDIO[lang_id][int(digit_pressed)])
    else:
        resp.play(AUDIO[lang_id][int(digit_pressed)])
    resp.play(AUDIO[lang_id][int(9)])
    resp.play(AUDIO[lang_id][int(0)])
    return str(resp)

@app.route("/status", methods=['GET', 'POST'])
def status(): 
    '''Save data about user'''
    data_blob = {}
    data_blob['CallDuration'] = request.values.get('CallDuration', None)
    data_blob['RecordingUrl'] = request.values.get('RecordingUrl', None)
    data_blob['RecordingSid'] = request.values.get('RecordingSid', None)
    data_blob['RecordingDuration'] = request.values.get('RecordingDuration', None)
    send_data(data_blob, 'Call_Status')
    return None

'''Send data to parse'''
def send_data(data, obj):
    import json,httplib
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/classes/'+CallAnalytics, json.dumps(data), {
           "X-Parse-Application-Id": "2W6rB0trZRZNa0jyrcbvFGoI8yN7PXqs8L6z4DQi",
           "X-Parse-REST-API-Key": "kK8riCXFGptYwPbrc100DSxFBe4aAijY1OctNEF6",
           "Content-Type": "application/json"
         })
    result = json.loads(connection.getresponse().read())
    print result

def send_analytics(blob):
    pass

if __name__ == "__main__":
    app.run(debug=True)
