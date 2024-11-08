#!/bin/env python
 
import requests
import json
import hashlib
import base64
import time
import hmac
import pandas as pd


#Proxies
proxy = {
    'http': 'http://example.proxy.com'
}

#Account Info
AccessId  = 'accessid'
AccessKey = 'accesskey'
Company   = 'company'

#Request Info
httpVerb ='GET'
resourcePath = '/dashboard/groups/'
queryParams = '?size=100'
data = ''
 
#Construct URL
url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath + queryParams
 
#Get current time in milliseconds
epoch = str(int(time.time() * 1000))
 
#Concatenate Request details
requestVars = httpVerb + epoch + data + resourcePath
 
#Construct signature 
digest = hmac.new(
        AccessKey.encode('utf-8'),
        msg=requestVars.encode('utf-8'),
        digestmod=hashlib.sha256).hexdigest()
signature = base64.b64encode(digest.encode('utf-8')).decode('utf-8')  
 
#Construct headers
auth = 'LMv1 ' + AccessId + ':' + str(signature) + ':' + epoch
headers = {'Content-Type':'application/json','Authorization':auth,'X-Version':'3'}
 
#Make request
response = requests.get(url, data=data, headers=headers,proxies=proxy,verify=False)
data = response.json()
devices = pd.DataFrame(data)

#Writes data to a .csv file , filtering for specific column(s)
devices.to_csv("./AllDashboards.csv",columns=['items'])

#Print status and body of response
#print('DATA',devices)
print('Response Status:',response.status_code)
print('Response Body:',data)