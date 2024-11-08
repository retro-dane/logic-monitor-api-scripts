#!/bin/env python
 
import requests
import json
import hashlib
import base64
import time
import hmac
import csv
import pandas as pd

#Proxies
proxy = {
    'http': 'http://example.proxy.com'
}

#Account Info
AccessId  = 'accessid'
AccessKey = 'accesskey'
Company   = 'company'

##File Information
filename = "..\Dashboard\AllDashboards.csv"

with open(filename,encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:

        items = eval(row["items"])
        id = items['id']
        parent = items['parentId']
        name1 = str(items['name'])
        name = name1.replace(" ","_")

        if parent == 36 :
            #Request Info
            httpVerb ='POST'
            resourcePath = '/setting/roles'
            data  = '{"key": "value", "key1": "value2" }'  
            ##Construct URL
            url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath 

            ##Get current time in   
            epoch = str(int(time.time() * 1000))

            ##Concatenate Request details
            requestVars = httpVerb + epoch + data + resourcePath
            print(requestVars)

            ##Construct signature 
            digest = hmac.new(
            AccessKey.encode('utf-8'),
            msg=requestVars.encode('utf-8'),
            digestmod=hashlib.sha256).hexdigest()
            signature = base64.b64encode(digest.encode('utf-8')).decode('utf-8')  

            ##Construct headers
            auth = 'LMv1 ' + AccessId + ':' + str(signature) + ':' + epoch
            headers = {'Content-Type':'application/json','Authorization':auth,'X-Version':'3'}

            #Make request
            response = requests.post(url, data=data, headers=headers,proxies=proxy,verify=False)

            #Print status and body of response
            #print('URL:', url)
            print('Response Status:',response.status_code)
            print('Response Body:',response.content)