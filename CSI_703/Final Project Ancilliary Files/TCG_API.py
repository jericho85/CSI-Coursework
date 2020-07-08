#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:21:33 2019

@author: jmcleod
"""

import requests
import json
import http.client
import urllib
#%%

url = "http://api.tcgplayer.com/v1.19.0/app/authorize/authCode"

response = requests.request("POST", url)

print(response.text)



#%%
""" Requesting Bearer Token (weekly)"""

public_key= "1F19E386-4AEF-437E-9805-C403A8C022AC"
private_key= "4A59204B-E469-44DE-9099-17A958DA940D"

headers = {"application": "x-www-form-urlencoded"}
payload = {"grant_type": "client_credentials",
           "client_id": public_key,
           "client_secret": private_key
           }

r = requests.post("https://api.tcgplayer.com/token",data=payload,headers=headers)
#%%
print(r.text) #pull access token from this

#output with access token:
#{"access_token":"lFWhm-zoa9sGtAR39b_qwrjwIaWIHyXdvVnBUHs9MRSheAJDa2BFw7qJ89usP4HtiteQ5n1G9XjBWIyJgfkZwt5Gb6OA4V7ROTvcWRlkNR1sksWoMjD-5clGraiVL9-KujdGBluBO4vRfqORJI93nkt94u1v15ZvI2wv7msTEzokEnqNTjuuLI2P1GUSNBcwL3OX6cj75rSFarmm4jtE2i3gVCgMqcVRd-7uFcIhFqMVn181iX7NSeL8XPcsMZ0SWKBn7nOmT6UaRs6w-zkm45mgnco0pExG0cWmuNfbQv14MMzhco5TkHXo1xx3Bz_0muq9iQ",
# "token_type":"bearer",
# "expires_in":1209599,
# "userName":"1f19e386-4aef-437e-9805-c403a8c022ac",
# ".issued":"Sat, 13 Apr 2019 18:40:07 GMT",
# ".expires":"Sat, 27 Apr 2019 18:40:07 GMT"}

bearer_token = "0SpKwg10ZSLRRxcQNi9pfGPtdJqgIFB42mrHaXqzBzk1TWW2gLXzEvfEb1nCI42l2snA34awYPUqDpAH-nVgfyoCPXdsvQ134T8d3qy1-OvBuOu807lqL6NlfD4qAHilC4RcFf5FY7SSeqcLkrz8C8dfc-0YWFtlDFCGApChvV5rrWNPFmQA-n-UsbHt--pzdik2_l2rXgf-4Dr8eeenrD185dWEUbtWriWuTLvW5hIbQ32uZeC3-2Px6-3Anif2a7Ri4JBvheY0gPEOM6AbqTDdqRLiZGWEGmL_NSzIBciUi5qFy6HdokYRXPQNxH2Tl03Klg"


#%%

""" Requesting API connection"""
url = "http://api.tcgplayer.com/v1.19.0/app/authorize/" + bearer_token

response = requests.request("POST", url)

print(response.text)