#!/bin/env python
 
import requests
import json
import hashlib
import base64
import time
import hmac
import csv

#Proxies
proxy = {
    'http': 'http://example.proxy.com'
}

#Account Info
AccessId  = 'accessid'
AccessKey = 'accesskey'
Company   = 'company'

##File Information
filename = "AllEscelationChains.csv"


with open(filename, encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        items = eval(row["items"])
        id = items['id']

        #Request Info
        httpVerb ='PATCH'
        resourcePath = '/setting/alert/chains/%s'%(id)
        
        #update rate limit period and alert amount
        data = '{"key": "value", "key1": "value2" }'
        
        #Construct URL
        url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath
        
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
        response = requests.patch(url, data=data, headers=headers,proxies=proxy,verify=False)

        #Print status and body of response
        print('URL:', url)
        print('Response Status:',response.status_code)
        print('Response Body:',response.content)