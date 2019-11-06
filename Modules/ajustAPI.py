
import sys
import requests

AJUST_ADMIN_ID = "ajustmin"
AJUST_ADMIN_PW = "ajust0000"

AJUST_LOGIN_URL = 'http://18.182.122.117:8000/api/auth/login/'
AJUSTER_POST_URL = 'http://18.182.122.117:8000/api/ajuster/'

headers = {'Authorization': 'token [YOUR_ACCESS_TOKEN]'}


def ajustReq(method, data={}):
    url = AJUSTER_POST_URL

    print('HTTP Method: %s' % method)
    print('Request URL: %s' % url)
    print('data: %s' % data)
    print('Headers: %s' % headers)

    if method == 'GET':
        return requests.get(url, headers=headers)
    else:
        return requests.post(url, headers=headers, data=data)


def ajustLogin(userID=AJUST_ADMIN_ID, userPW=AJUST_ADMIN_PW):
    userData = {
        "username": userID,
        "password": userPW,
    }

    res = requests.post(AJUST_LOGIN_URL, data=userData)
    if res.status_code == 200:
        headers['Authorization'] = "token {}".format(res.json()['token'])
        print("Server Login Success.")
    else:
        print("Server Login Falied.")

    return res.status_code


def ajustLogUpdate(data):
    res = ajustReq('POST', data)

    return res.status_code
