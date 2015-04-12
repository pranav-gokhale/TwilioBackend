from flask import Flask, request, redirect
import twilio.twiml
import json,httplib,urllib
import time


app = Flask(__name__)
 
BELL_URL = 'https://www.dropbox.com/s/jz0k7w09cleuglk/Bell.mp3?dl=1'
INTRO_URL = ['https://www.dropbox.com/s/keclu5q8sesy685/Press_1_for_English.mp3?dl=1',
             'https://www.dropbox.com/s/h348n615w6kcknz/Press_2_In_Amharic.mp3?dl=1',
             'https://www.dropbox.com/s/tqeetjtvl69b2h5/Press_3_For_Bengali.mp3?dl=1',
             'https://www.dropbox.com/s/7l9j0ieexvwfkt6/Press4forHindi.mp3?dl=1']

INTRO_TEXT = '''5 for Indonesian, 6 for Malayalam, 7 for Mandarin, 8 for Nepali, 9 for Sinhalese, 10 for Tagalog, 11 for Tamil, 12 for Telugu'''

FURTHER_INFO_TEXT_URL = { 
'1' : 'https://www.dropbox.com/s/s5rkrkosjzwxf9d/EnglishOptions.mp3?dl=1',
'4' : 'https://www.dropbox.com/s/dql9uif9dyfp3vh/HindiOptions.mp3?dl=1'
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

THANKS_URL = {
        1 : 'https://www.dropbox.com/s/6trf9qmfe2dqkyf/ThanksEnglish.mp3?dl=1',
        4 : 'https://www.dropbox.com/s/9g33rvbsffe68x7/ThanksHindi.mp3?dl=1'
}

LANGUAGEID_TO_LANGUAGE = ['','English', 'Amharic', 'Bengali', 'Hindi', 'Indonesian', 'Malayalam', 'Mandarin', 'Nepali', 'Sinhalese', 'Tagalog', 'Tamil', 'Telugu']

CATEGORYID_TO_CATEGORY = ['Intro', 'Visa', 'Slavery', 'Salary', 'Working Conditions', 'Job Loss', 'Going Home', 'Lawful Rights', 'Domestic Work', 'All' ]

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

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    '''Save data about user'''
    data_blob = {}
    data_blob["new_session"] = True
    data_blob["from_number"] = request.values.get('From', None)
    send_data(data_blob, 'Call')
    '''Interact with user'''
    resp = twilio.twiml.Response()

    with resp.gather(numDigits=1, action="/handle-lang", method="POST") as g:
        resp.pause()
        resp.play(BELL_URL)
        for s in INTRO_URL:
            g.play(s)
        g.say(INTRO_TEXT) 
    return str(resp)

@app.route("/handle-lang", methods=['GET', 'POST'])
def handle_lang():
    """Handle key press from a user."""
    digit_pressed = request.values.get('Digits', None)
    '''Save data about user'''
    data_blob = {}
    data_blob["from_number"] = request.values.get('From', None)
    data_blob["lang_id"] = digit_pressed
    send_data(data_blob, 'Language')

    # Get the digit pressed by the user
    resp = twilio.twiml.Response()
    if (digit_pressed is None):
        return redirect("/")
    if int(digit_pressed) <= 12: 
        with resp.gather(numDigits=1, action="/handle-further-info/"+digit_pressed, method="POST") as g:
            g.play(FURTHER_INFO_TEXT_URL[digit_pressed])
        print FURTHER_INFO_TEXT_URL[digit_pressed]
        return str(resp)
    else :
        return redirect("/")

@app.route("/handle-further-info/<int:lang_id>", methods=['GET', 'POST'])
def handle_further_info(lang_id): 
    digit_pressed = request.values.get('Digits', None)
    '''Save data about user'''
    data_blob = {}
    data_blob["from_number"] = request.values.get('From', None)
    data_blob["category_id"] = digit_pressed
    send_data(data_blob, 'Category')


    resp = twilio.twiml.Response()
    if (digit_pressed is None):
        return redirect("/")    
    if (int(digit_pressed)==0):
        resp.say('Volunteer')
        return str(resp)
    elif (int(digit_pressed)==9):
        for i in range(1, 9):
            resp.play(AUDIO[lang_id][i])
    else:
        resp.play(AUDIO[lang_id][int(digit_pressed)])
    resp.play(AUDIO[lang_id][int(9)])
    resp.play(AUDIO[lang_id][int(0)])
    resp.play(THANKS_URL[lang_id])
    return str(resp)

@app.route("/status", methods=['GET', 'POST'])
def status(): 
    '''Save data about user'''
    if (request.values.get('From', None) is None):
        return redirect("/") 
    data_blob = {}
    data_blob['CallDuration'] = request.values.get('CallDuration', None)
    data_blob['RecordingUrl'] = request.values.get('RecordingUrl', None)
    data_blob['RecordingSid'] = request.values.get('RecordingSid', None)
    data_blob['RecordingDuration'] = request.values.get('RecordingDuration', None)
    data_blob['From'] = request.values.get('From', None)
    data_blob['Language'] = LANGUAGEID_TO_LANGUAGE[int(fetch_language(request.values.get('From', None)))]
    data_blob['Category'] = CATEGORYID_TO_CATEGORY[int(fetch_category(request.values.get('From', None)))]
    data_blob['Timestamp'] = int(time.time())

    send_analytics(data_blob)
    send_data(data_blob, 'Call_Status')
    return None

'''Send data to parse'''
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

def send_analytics(data):
    import json,httplib
    connection = httplib.HTTPSConnection('arshidni.meteor.com')
    connection.connect()
    connection.request('POST', '/complaint', json.dumps(data), {
           "Content-Type": "application/json"
         })
    result = json.loads(connection.getresponse().read())
    print result


def fetch_language(phone_string):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    params = urllib.urlencode({"order":"-createdAt"})
    connection.connect()
    connection.request('GET', '/1/classes/'+'Language?%s' % params, '' , { 
           "X-Parse-Application-Id": "2W6rB0trZRZNa0jyrcbvFGoI8yN7PXqs8L6z4DQi",
           "X-Parse-REST-API-Key": "kK8riCXFGptYwPbrc100DSxFBe4aAijY1OctNEF6",
    })
    res = json.loads(connection.getresponse().read())['results']
    for r in res:
        if (str(r.get(u'from_number',None)) == unicode(phone_string)):
            return r.get(u'lang_id',False)            

def fetch_category(phone_string):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    params = urllib.urlencode({"order":"-createdAt"})
    connection.connect()
    connection.request('GET', '/1/classes/'+'Category?%s' % params, '' , {
           "X-Parse-Application-Id": "2W6rB0trZRZNa0jyrcbvFGoI8yN7PXqs8L6z4DQi",
           "X-Parse-REST-API-Key": "kK8riCXFGptYwPbrc100DSxFBe4aAijY1OctNEF6",
    })
    res = json.loads(connection.getresponse().read())['results']
    for r in res:
        if (str(r.get(u'from_number',None)) == unicode(phone_string)):
            return r.get(u'category_id',False)

if __name__ == "__main__":
    app.run(debug=True)
