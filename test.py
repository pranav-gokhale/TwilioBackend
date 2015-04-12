'''

def fetch_language(phone_string):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('GET', '/1/classes/'+'Language',json.dumps({1:1}) , { ##########
	       "X-Parse-Application-Id": "2W6rB0trZRZNa0jyrcbvFGoI8yN7PXqs8L6z4DQi",
	       "X-Parse-REST-API-Key": "kK8riCXFGptYwPbrc100DSxFBe4aAijY1OctNEF6",
	})
	res = json.loads(connection.getresponse().read())['results']
	for r in res:
		if (str(r.get(u'from_number',None)) == unicode(phone_string)):
			return r.get(u'lang_id',False)

print fetch_language('+971507902840')
'''
import json,httplib,urllib

def fetch_language(phone_string):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    params = urllib.urlencode({"order":"-createdAt"})
    # params=''
    connection.connect()
    connection.request('GET', '/1/classes/'+'Language?%s' % params, '' , { 
           "X-Parse-Application-Id": "2W6rB0trZRZNa0jyrcbvFGoI8yN7PXqs8L6z4DQi",
           "X-Parse-REST-API-Key": "kK8riCXFGptYwPbrc100DSxFBe4aAijY1OctNEF6",
    })
    res = json.loads(connection.getresponse().read())['results']
    for r in res:
    	print r
        if (str(r.get(u'from_number',None)) == unicode(phone_string)):
            return r.get(u'lang_id',False)


print fetch_language('client:Anonymous')