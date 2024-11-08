#!/bin/env python
 
import requests
import json
import hashlib
import base64
import time
import hmac
import csv

count = 0

#Proxies
proxy = {
    'http': 'http://example.proxy.com'
}

#Account Info
AccessId  = 'accessid'
AccessKey = 'accesskey'
Company   = 'company'

##File Information
filename = "./AllAlertRules.csv"

with open(filename,encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        items = eval(row["items"])
        name = items["name"]
        id = items["id"]

        if "Error" not in name :
            print("do nothing")
        else:   
            count = count + 1
        #Request Info
            httpVerb ='PATCH'
            resourcePath = '/setting/alert/rules/%s' %(id)  
            ueryParams = ''
            data = '{"priority":%s}' %(count+201)

            #Construct URL
            url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath 

            #Get current time in milliseconds
            epoch = str(int(time.time() * 1000))

            #Concatenate Request details
            requestVars = httpVerb + epoch + data + resourcePath
            #print(requestVars)

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
            #
            #Print status and body of response
            print('URL:', url)
            print('Response Status:',response.status_code)
            print('Response Body:',response.content)