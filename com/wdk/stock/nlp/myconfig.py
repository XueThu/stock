#coding: utf-8
import json

from aip import AipNlp
import requests


APP_ID = '11198235'
API_KEY = 'cgRgGeh2X4RMZLNWYCP3IEva'
SECRET_KEY = 'ROMQxxOeyd6O2NLGpyZlw6lA24Qa6uAx'
bd_client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

urltoken ='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials'\
          +'&client_id=' + API_KEY\
          +'&client_secret=' + SECRET_KEY

req = requests.get(urltoken) 
access_token = json.loads(req.text)["access_token"]

# req = requests.get(urltoken)    #ascii
# req_utf8 = req.text.encode("utf-8")  #ascii to utf-8
# # access_token = json.loads(req_utf8).__getitem__("access_token")  #utf-8 to dict
# print(req.text)
