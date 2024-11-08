#!/bin/env python
 
import requests
import json
import hashlib
import base64
import time
import hmac
import csv

counter =0

#UpdateList
servers=[]

#Proxies
proxy = {
    'http': 'http://example.proxy.com'
}

#Account Info
AccessId  = 'accessid'
AccessKey = 'accesskey'
Company   = 'company'

##File Information
filename = "AllDevices.csv"


with open(filename) as f:
    reader = csv.DictReader(f)
    for row in reader:
        counter = counter +1
        item = eval(row["items"])
        id = item["id"]
        displayName = str(item["displayName"])

        if displayName not in servers:
            print("")
        else:
            #Request Info
            httpVerb ='PUT'
            resourcePath = '/device/devices/{}/properties/custom.property'.format(id)
            queryParams = ''
            data = '{"value": "value of custom property"}' 

            #Construct URL
            url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath +queryParams

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
            response = requests.put(url, data=data, headers=headers,proxies=proxy,verify=False)

            #Print status and body of response
            print('URL:', url)
            print('Response Status:',response.status_code)
            print('Response Body:',response.content)
    