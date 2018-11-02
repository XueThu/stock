#coding: utf-8
import json

from aip import AipNlp
import requests


APP_ID = '14261689'
API_KEY = 'uAVTwlOtligLGj6h18ifWFi0'
SECRET_KEY = 'FqIVKEGN1u4TMGjtfD7Q5l3bkZZpfrpU'
bd_client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

urltoken ='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials'\
          +'&client_id=' + API_KEY\
          +'&client_secret=' + SECRET_KEY

req = requests.get(urltoken) 
access_token = json.loads(req.text)["access_token"]
print(access_token)

# req = requests.get(urltoken)    #ascii
# req_utf8 = req.text.encode("utf-8")  #ascii to utf-8
# # access_token = json.loads(req_utf8).__getitem__("access_token")  #utf-8 to dict
# print(req.text)
