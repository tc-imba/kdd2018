# coding: utf-8

import requests

files = {'files': open('submission.csv', 'rb')}

data = {
    "user_id": "liuyh615",
    # user_id is your username which can be found on the top-right corner on our website when you logged in.
    "team_token": "19ae027935e8ab56a1a700e30a7991722303ca330951adb36c4d4fd9aaa9632b",  # your team_token.
    "description": 'liuyh615 submission',  # no more than 40 chars.
    "filename": "submission.csv",  # your filename
}

url = 'https://biendata.com/competition/kdd_2018_submit/'

response = requests.post(url, files=files, data=data)

print(response.text)
