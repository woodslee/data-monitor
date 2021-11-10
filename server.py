from fastapi import FastAPI

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

app = FastAPI()


@app.post('/vue-admin-template/user/login')
def login(req):
    token = req.get('username')
    if token and tokens.get(token):
        return {
            'code': 20000,
            'data': tokens.get(token)
        }
    return {
        'code': 60204,
        'message': 'Account and password are incorrect.'
    }


@app.get('/vue-admin-template/user/info/{token}')
def info(token):
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
def logout(req):
    print('logout,request:%s' % req)
    return {
        'code': 20000,
        'data': 'success'
    }
