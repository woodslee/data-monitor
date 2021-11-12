from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import requests
import json
tokens = {
    'admin': {
        'token': 'admin-token'
    },
    'editor': {
        'token': 'editor-token'
    }
}

users = {
    'admin-token': {
        'roles': ['admin'],
        'introduction': 'I am a super administrator',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': 'Super Admin'
    },
    'editor-token': {
        'roles': ['editor'],
        'introduction': 'I am an editor',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': 'Normal Editor'
    }
}


class User(BaseModel):
    username: Optional[str]


app = FastAPI()

def http_get(req_url: str):
    response = requests.get(req_url)
    if response.status_code==200:
        return response.json()
    return  json.loads('{}')


@app.post('/vue-admin-template/user/login')
def login(user: User):
    username = user.username
    if username and tokens.get(username):
        return {
            'code': 20000,
            'data': tokens.get(username)
        }
    return {
        'code': 60204,
        'message': 'Account and password are incorrect.'
    }


@app.get('/vue-admin-template/user/info')
def info(token: str):
    user = users.get(token)
    if user:
        return {
            'code': 20000,
            'data': user
        }
    return {
        'code': 50008,
        'message': 'Login failed, unable to get user details.'
    }


@app.post('/vue-admin-template/user/logout')
def logout(user: Optional[User] = None):
    return {
        'code': 20000,
        'data': 'success'
    }

@app.get('/vue-admin-template/flink/job/list')
def job_list():
    return http_get('http://192.168.3.221:8088/ws/v1/cluster/apps?state=RUNNING')
