"""

    This tests route.user by using flask test
    
    Tests includes:
        - route.user
        - lib.libuser
        - lib.key
        - lib.database
        - lib.libdevice
        - lib.libevent

    Author: Haoyu Xu

"""

import json
import hashlib

from lib.libconfig import LibConfig
CONFIG = LibConfig(config="test.yml").fetch()
USERS = CONFIG["users"]
admins = {
    "admin": {
        "uuid": "dummy",
        "otp": "dummy"
    },
    "root": {
        "uuid": "dummy",
        "otp": "dummy"
    },
    "dummy": {
        "uuid": "f9a5fdd11746e324bb664d6e80025b7d97959aa4f8052f5327127de1094954d2",
        "otp": "dummy"
    }
}
users = {
    "jack": {
        "password": "imjack",
        "uuid": "dummy",
        "otp": "dummy"
    },
    "lisa": {
        "password": "imlisa",
        "uuid": "dummy",
        "otp": "dummy"
    },
    "dummy": {
        "password": "dummy",
        "uuid": "dummy",
        "otp": "dummy"
    }
}

def test_setup(app, client):

    for key, value in USERS.items():
        user = {
            "username": key,
            "password": str(hashlib.md5(str(value).encode('utf-8')).hexdigest())
        }
        admins[key]["uuid"] = str(hashlib.sha256(str(";".join("{field_key}:{field_value}".format(field_key=field_key, field_value=field_value) for field_key, field_value in user.items())).encode('utf-8')).hexdigest())

def test_before_login(app, client):
    res = client.get('/user', headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 401

    res = client.get('/users', headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 401

    res = client.get('/user/{uuid}'.format(uuid=admins["root"]["uuid"]), headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 401

    res = client.delete('/user/logout', headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 401

    res = client.delete('/user/delete', headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 401

    res = client.post('/user/add', headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    }, data=dict(
        fields="dummy"
    ))
    assert res.status_code == 401

    res = client.put('/user/update', headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    }, data=dict(
        fields="dummy"
    ))
    assert res.status_code == 401

def test_login(app, client):
    res = client.post("/user/login", headers={
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 200
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    admins["admin"]["otp"] = actual["message"]

    res = client.post("/user/login", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-PERM": True
    })
    assert res.status_code == 200
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    admins["admin"]["otp"] = actual["message"]

    res = client.post("/user/login", headers={
        "X-UUID": admins["root"]["uuid"],
        "X-PERM": False
    })
    assert res.status_code == 200
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    admins["root"]["otp"] = actual["message"]

    res = client.post("/user/login", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-PERM": False
    })
    assert res.status_code == 401
    expected = "Either username or password is incorrect"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    
# test routes
def test_route(app, client):
    res = client.get('/user1')
    assert res.status_code == 404

    # GET /user
    res = client.get('/user')
    assert res.status_code == 400

    res = client.post('/user', headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 400

    res = client.post('/user')
    assert res.status_code == 400

    res = client.delete('/user', headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 400

    res = client.delete('/user')
    assert res.status_code == 400

    res = client.put('/user', headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 400

    res = client.put('/user')
    assert res.status_code == 400

    # GET /user/<uuid>
    res = client.get('/user/{}'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 401

    res = client.get('/user/{}'.format(admins["dummy"]["uuid"]))
    assert res.status_code == 400

    res = client.post('/user/{}'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 500

    res = client.post('/user/{}'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 500

    res = client.post('/user/{}'.format(admins["dummy"]["uuid"]))
    assert res.status_code == 500

    res = client.delete('/user/{}'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 500

    res = client.delete('/user/{}'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 500

    res = client.delete('/user/{}'.format(admins["dummy"]["uuid"]))
    assert res.status_code == 500

    res = client.put('/user/{}'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 500

    res = client.put('/user/{}'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 500

    res = client.put('/user/{}'.format(admins["dummy"]["uuid"]))
    assert res.status_code == 500

    # GET /users
    res = client.get('/users')
    assert res.status_code == 400

    res = client.get('/users'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 401

    res = client.post('/users')
    assert res.status_code == 400

    res = client.post('/users'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    res = client.delete('/users')
    assert res.status_code == 400

    res = client.delete('/users'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    res = client.put('/users')
    assert res.status_code == 400

    res = client.put('/users'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    # DELETE /user/logout
    res = client.delete('/user/logout')
    assert res.status_code == 400

    res = client.delete('/user/logout'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 401

    res = client.get('/user/logout')
    assert res.status_code == 400

    res = client.get('/user/logout'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    res = client.post('/user/logout')
    assert res.status_code == 400

    res = client.post('/user/logout'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    res = client.put('/user/logout')
    assert res.status_code == 400

    res = client.put('/user/logout'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    # DELETE /user/delete
    res = client.delete('/user/logout')
    assert res.status_code == 400

    res = client.delete('/user/logout'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    }, data={
        "uuid": admins["dummy"]["uuid"]
    })
    assert res.status_code == 401

    res = client.get('/user/delete')
    assert res.status_code == 400

    res = client.get('/user/delete'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    res = client.post('/user/delete')
    assert res.status_code == 400

    res = client.post('/user/delete'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    res = client.put('/user/delete')
    assert res.status_code == 400

    res = client.put('/user/delete'.format(admins["dummy"]["uuid"]), headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    # POST /user/login
    res = client.post("/user/login", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-PERM": True
    })
    assert res.status_code == 401

    res = client.post("/user/login")
    assert res.status_code == 400

    res = client.get("/user/login", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-PERM": True
    })
    assert res.status_code == 400

    res = client.get("/user/login")
    assert res.status_code == 400

    res = client.delete("/user/login", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-PERM": True
    })
    assert res.status_code == 400

    res = client.delete("/user/login")
    assert res.status_code == 400

    res = client.put("/user/login", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-PERM": True
    })
    assert res.status_code == 400

    res = client.put("/user/login")
    assert res.status_code == 400

    # POST /user/add
    res = client.post("/user/add", headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    }, data={
        "fields": str(dict(
            username="admin",
            password="fake",
            type="normal"
        ))
    })
    assert res.status_code == 401

    res = client.post("/user/add")
    assert res.status_code == 400

    res = client.get("/user/add", headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    res = client.get("/user/add")
    assert res.status_code == 400

    res = client.delete("/user/add", headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    res = client.delete("/user/add")
    assert res.status_code == 400

    res = client.put("/user/add", headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    res = client.put("/user/add")
    assert res.status_code == 400

    # PUT /user/update
    res = client.put("/user/update", headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    }, data={
        "fields": str(dict(
            username="admin",
            password="fake",
            type="normal"
        ))
    })
    assert res.status_code == 401

    res = client.put("/user/update")
    assert res.status_code == 400

    res = client.get("/user/update", headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    res = client.get("/user/update")
    assert res.status_code == 400

    res = client.delete("/user/update", headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    res = client.delete("/user/update")
    assert res.status_code == 400

    res = client.post("/user/update", headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 400

    res = client.post("/user/update")
    assert res.status_code == 400

# does not invoke permission check
def test_user(app, client):
    # sufficient case
    res = client.get("/user", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 200
    expected = {
        "username": "admin",
        "password": "",
        "uuid": admins["admin"]["uuid"],
        "email": "",
        "type": "admin",
        "otp": "",
        "otp_time": ""
    }
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # no uuid
    res = client.get("/user", headers={
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # no otp
    res = client.get("/user", headers={
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing both
    res = client.get("/user")
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid uuid
    res = client.get("/user", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid otp
    res = client.get("/user", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid user
    res = client.get("/user", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

# invoke permission check
def test_permission_setup(app, client):
    # add two normal user
    res = client.post("/user/add", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="jack",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()),
            type="normal"
        ))
    ))
    assert res.status_code == 200
    expected = "User is added"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.post("/user/add", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="lisa",
            password=str(hashlib.md5(str(users["lisa"]["password"]).encode('utf-8')).hexdigest()),
            type="normal"
        ))
    ))
    assert res.status_code == 200
    expected = "User is added"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # acquire user uuid
    users["jack"]["uuid"] = str(hashlib.sha256("username:{username};password:{password}".format(username="jack", password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest())).encode('utf-8')).hexdigest())
    users["lisa"]["uuid"] = str(hashlib.sha256("username:{username};password:{password}".format(username="lisa", password=str(hashlib.md5(str(users["lisa"]["password"]).encode('utf-8')).hexdigest())).encode('utf-8')).hexdigest())

    # login
    res = client.post("/user/login", headers={
        "X-UUID": users["jack"]["uuid"],
        "X-PERM": True
    })
    assert res.status_code == 200
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    users["jack"]["otp"] = actual["message"]

    res = client.post("/user/login", headers={
        "X-UUID": users["lisa"]["uuid"],
        "X-PERM": False
    })
    assert res.status_code == 200
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    users["lisa"]["otp"] = actual["message"]
    
def test_users(app, client):
    expected_template = [
        {
            "uuid": admins["admin"]["uuid"],
            "username": "admin",
            "password": "",
            "email": "",
            "type": "admin",
            "otp": "",
            "otp_time": ""
        },
        {
            "uuid": users["jack"]["uuid"],
            "username": "jack",
            "password": "",
            "email": "",
            "type": "normal",
            "otp": "",
            "otp_time": ""
        },{
            "uuid": users["lisa"]["uuid"],
            "username": "lisa",
            "password": "",
            "email": "",
            "type": "normal",
            "otp": "",
            "otp_time": ""
        },
        {
            "uuid": admins["root"]["uuid"],
            "username": "root",
            "password": "",
            "email": "",
            "type": "admin",
            "otp": "",
            "otp_time": ""
        }
    ]
    # sufficient case
    res = client.get("/users", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected_template == actual["message"]
    
    # sufficient case
    res = client.get("/users", headers={
        "X-UUID": admins["root"]["uuid"],
        "X-OTP": admins["root"]["otp"]
    })
    assert res.status_code == 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected_template == actual["message"]

    # invalid uuid
    res = client.get("/users", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid otp
    res = client.get("/users", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid user
    res = client.get("/users", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing uuid
    res = client.get("/users", headers={
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing otp
    res = client.get("/users", headers={
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing both
    res = client.get("/users")
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # user that does not have permission
    res = client.get("/users", headers={
        "X-UUID": users["jack"]["uuid"],
        "X-OTP": users["jack"]["otp"]
    })
    assert res.status_code == 403
    expected = "You don't have this permission"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.get("/users", headers={
        "X-UUID": users["lisa"]["uuid"],
        "X-OTP": users["lisa"]["otp"]
    })
    assert res.status_code == 403
    expected = "You don't have this permission"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

def test_user_uuid(app, client):
    expected_template = {
        "uuid": users["jack"]["uuid"],
        "username": "jack",
        "password": "",
        "email": "",
        "type": "normal",
        "otp": "",
        "otp_time": ""
    }
    # sufficient case
    res = client.get("/user/{}".format(users["jack"]["uuid"]), headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected_template == actual["message"]
    
    # sufficient case
    res = client.get("/user/{}".format(users["jack"]["uuid"]), headers={
        "X-UUID": admins["root"]["uuid"],
        "X-OTP": admins["root"]["otp"]
    })
    assert res.status_code == 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected_template == actual["message"]

    # invalid uuid
    res = client.get("/user/{}".format(users["jack"]["uuid"]), headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid otp
    res = client.get("/user/{}".format(users["jack"]["uuid"]), headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid user
    res = client.get("/user/{}".format(users["jack"]["uuid"]), headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing uuid
    res = client.get("/user/{}".format(users["jack"]["uuid"]), headers={
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing otp
    res = client.get("/user/{}".format(users["jack"]["uuid"]), headers={
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing both
    res = client.get("/user/{}".format(users["jack"]["uuid"]))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # user that does not have permission
    res = client.get("/user/{}".format(users["jack"]["uuid"]), headers={
        "X-UUID": users["jack"]["uuid"],
        "X-OTP": users["jack"]["otp"]
    })
    assert res.status_code == 403
    expected = "You don't have this permission"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.get("/user/{}".format(users["jack"]["uuid"]), headers={
        "X-UUID": users["lisa"]["uuid"],
        "X-OTP": users["lisa"]["otp"]
    })
    assert res.status_code == 403
    expected = "You don't have this permission"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

def test_add(app, client):
    # invalid uuid
    res = client.post("/user/add", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="jack",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()),
            type="normal"
        ))
    ))
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid otp
    res = client.post("/user/add", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="jack",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()),
            type="normal"
        ))
    ))
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid user
    res = client.post("/user/add", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="jack",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()),
            type="normal"
        ))
    ))
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing uuid
    res = client.post("/user/add", headers={
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="jack",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()),
            type="normal"
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing otp
    res = client.post("/user/add", headers={
        "X-UUID": admins["admin"]["uuid"]
    }, data=dict(
        fields=str(dict(
            username="jack",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()),
            type="normal"
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing both
    res = client.post("/user/add", data=dict(
        fields=str(dict(
            username="jack",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()),
            type="normal"
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing username
    res = client.post("/user/add", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()),
            type="normal"
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing password
    res = client.post("/user/add", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="jack",
            type="normal"
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing type
    res = client.post("/user/add", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="jack",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest())
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing all
    res = client.post("/user/add", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # empty username
    res = client.post("/user/add", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="              ",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()),
            type="normal"
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # empty password
    res = client.post("/user/add", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="jack",
            password="              ",
            type="normal"
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # empty type
    res = client.post("/user/add", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="jack",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()),
            type="          "
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # all empty
    res = client.post("/user/add", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="      ",
            password="      ",
            type="          "
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # use who does not have permission
    res = client.post("/user/add", headers={
        "X-UUID": users["jack"]["uuid"],
        "X-OTP": users["jack"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="jack",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()),
            type="normal"
        ))
    ))
    assert res.status_code == 403
    expected = "You don't have this permission"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

def test_update(app, client):
    update_template = {
        "admin": {
            "username": "admin-test",
            "password": str(hashlib.md5(str("00000000000000").encode('utf-8')).hexdigest())
        }
    }
    # sufficient case, update themselves
    res = client.put("/user/update", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username=update_template["admin"]["username"],
            password=update_template["admin"]["password"]
        ))
    ))
    assert res.status_code == 200
    expected = "User is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    # get new uuid
    new_uuid = str(hashlib.sha256(str("username:{username};password:{password}".format(username=update_template["admin"]["username"], password=update_template["admin"]["password"])).encode('utf-8')).hexdigest())
    # check update status
    res = client.get("/user", headers={
        "X-UUID": new_uuid,
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 200
    expected = {
        "username": update_template["admin"]["username"],
        "password": "",
        "uuid": new_uuid,
        "email": "",
        "type": "admin",
        "otp": "",
        "otp_time": ""
    }
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    # change back
    res = client.put("/user/update", headers={
        "X-UUID": new_uuid,
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="admin",
            password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()),
            type="admin"
        ))
    ))
    assert res.status_code == 200
    expected = "User is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # sufficient case, update username
    res = client.put("/user/update", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username=update_template["admin"]["username"]
        ))
    ))
    assert res.status_code == 200
    expected = "User is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    # get new uuid
    new_uuid = str(hashlib.sha256(str("username:{username};password:{password}".format(username=update_template["admin"]["username"], password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()))).encode('utf-8')).hexdigest())
    # check update status
    res = client.get("/user", headers={
        "X-UUID": new_uuid,
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 200
    expected = {
        "username": update_template["admin"]["username"],
        "password": "",
        "uuid": new_uuid,
        "email": "",
        "type": "admin",
        "otp": "",
        "otp_time": ""
    }
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    # change back
    res = client.put("/user/update", headers={
        "X-UUID": new_uuid,
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="admin",
            password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()),
            type="admin"
        ))
    ))
    assert res.status_code == 200
    expected = "User is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # sufficient case, update password
    res = client.put("/user/update", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            password=update_template["admin"]["password"]
        ))
    ))
    assert res.status_code == 200
    expected = "User is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    # get new uuid
    new_uuid = new_uuid = str(hashlib.sha256(str("username:{username};password:{password}".format(username="admin", password=update_template["admin"]["password"])).encode('utf-8')).hexdigest())
    # check update status
    res = client.get("/user", headers={
        "X-UUID": new_uuid,
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 200
    expected = {
        "username": "admin",
        "password": "",
        "uuid": new_uuid,
        "email": "",
        "type": "admin",
        "otp": "",
        "otp_time": ""
    }
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    # change back
    res = client.put("/user/update", headers={
        "X-UUID": new_uuid,
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="admin",
            password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()),
            type="admin"
        ))
    ))
    assert res.status_code == 200
    expected = "User is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # sufficient case, update type
    res = client.put("/user/update", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data=dict(
        fields=str(dict(
            type="normal"
        ))
    ))
    assert res.status_code == 200
    expected = "User is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    # check update status
    res = client.get("/users", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 403
    expected = "You don't have this permission"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    # change back
    res = client.put("/user/update", headers={
        "X-UUID": admins["root"]["uuid"],
        "X-OTP": admins["root"]["otp"]
    }, data=dict(
        fields=str(dict(
            uuid=admins["admin"]["uuid"],
            type="admin"
        ))
    ))
    assert res.status_code == 200
    expected = "User is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid uuid in fields
    res = client.put("/user/update", headers={
        "X-UUID": admins["root"]["uuid"],
        "X-OTP": admins["root"]["otp"]
    }, data=dict(
        fields=str(dict(
            uuid=admins["dummy"]["uuid"],
            username="admin",
            password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()),
            type="admin"
        ))
    ))
    assert res.status_code == 400
    expected = "Invalid UUID"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid username in fields
    res = client.put("/user/update", headers={
        "X-UUID": admins["root"]["uuid"],
        "X-OTP": admins["root"]["otp"]
    }, data=dict(
        fields=str(dict(
            uuid=admins["admin"]["uuid"],
            username="               ",
            password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()),
            type="admin"
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid password in fields
    res = client.put("/user/update", headers={
        "X-UUID": admins["root"]["uuid"],
        "X-OTP": admins["root"]["otp"]
    }, data=dict(
        fields=str(dict(
            uuid=admins["admin"]["uuid"],
            username="admin",
            password="              ",
            type="admin"
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid type in fields
    res = client.put("/user/update", headers={
        "X-UUID": admins["root"]["uuid"],
        "X-OTP": admins["root"]["otp"]
    }, data=dict(
        fields=str(dict(
            uuid=admins["admin"]["uuid"],
            username="admin",
            password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()),
            type="                 "
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid uuid
    res = client.put("/user/update", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["root"]["otp"]
    }, data=dict(
        fields=str(dict(
            uuid=admins["admin"]["uuid"],
            username="admin",
            password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()),
            type="admin"
        ))
    ))
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid otp
    res = client.put("/user/update", headers={
        "X-UUID": admins["root"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    }, data=dict(
        fields=str(dict(
            uuid=admins["admin"]["uuid"],
            username="admin",
            password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()),
            type="admin"
        ))
    ))
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid user
    res = client.put("/user/update", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    }, data=dict(
        fields=str(dict(
            uuid=admins["admin"]["uuid"],
            username="admin",
            password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()),
            type="admin"
        ))
    ))
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing uuid
    res = client.put("/user/update", headers={
        "X-OTP": admins["root"]["otp"]
    }, data=dict(
        fields=str(dict(
            uuid=admins["admin"]["uuid"],
            username="admin",
            password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()),
            type="admin"
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing otp
    res = client.put("/user/update", headers={
        "X-UUID": admins["root"]["uuid"]
    }, data=dict(
        fields=str(dict(
            uuid=admins["admin"]["uuid"],
            username="admin",
            password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()),
            type="admin"
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing both
    res = client.put("/user/update", data=dict(
        fields=str(dict(
            uuid=admins["admin"]["uuid"],
            username="admin",
            password=str(hashlib.md5(str(USERS["admin"]).encode('utf-8')).hexdigest()),
            type="admin"
        ))
    ))
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # user who does not have this permission can only update themselves
    res = client.put("/user/update", headers={
        "X-UUID": users["jack"]["uuid"],
        "X-OTP": users["jack"]["otp"]
    }, data=dict(
        fields=str(dict(
            uuid=admins["admin"]["uuid"],
            username="jack-test",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()),
            type="admin"
        ))
    ))
    assert res.status_code == 200
    expected = "User is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    # get new uuid
    new_uuid = new_uuid = str(hashlib.sha256(str("username:{username};password:{password}".format(username="jack-test", password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest()))).encode('utf-8')).hexdigest())
    # check update status
    res = client.get("/user", headers={
        "X-UUID": new_uuid,
        "X-OTP": users["jack"]["otp"]
    })
    assert res.status_code == 200
    expected = {
        "username": "jack-test",
        "password": "",
        "uuid": new_uuid,
        "email": "",
        "type": "normal",
        "otp": "",
        "otp_time": ""
    }
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    # change back
    res = client.put("/user/update", headers={
        "X-UUID": new_uuid,
        "X-OTP": users["jack"]["otp"]
    }, data=dict(
        fields=str(dict(
            username="jack",
            password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest())
        ))
    ))
    assert res.status_code == 200
    expected = "User is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    
def test_delete(app, client):
    # sufficient case
    res = client.delete("/user/delete", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data={
        "uuid": users["jack"]["uuid"]
    })
    assert res.status_code == 200
    expected = "User is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # check if jack exists
    res = client.post("/user/login", headers={
        "X-UUID": users["jack"]["uuid"],
        "X-PERM": False
    })
    assert res.status_code == 401
    expected = "Either username or password is incorrect"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid x-uuid
    res = client.delete("/user/delete", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    }, data={
        "uuid": users["lisa"]["uuid"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid x-otp
    res = client.delete("/user/delete", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    }, data={
        "uuid": users["lisa"]["uuid"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing x-uuid
    res = client.delete("/user/delete", headers={
        "X-OTP": admins["admin"]["otp"]
    }, data={
        "uuid": users["lisa"]["uuid"]
    })
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing x-otp
    res = client.delete("/user/delete", headers={
        "X-UUID": admins["admin"]["uuid"]
    }, data={
        "uuid": users["lisa"]["uuid"]
    })
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # admin user to delete themselves
    res = client.delete("/user/delete", headers={
        "X-UUID": admins["root"]["uuid"],
        "X-OTP": admins["root"]["otp"]
    })
    assert res.status_code == 200
    expected = "User is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # normal user to delete other users, can only delete themselves
    res = client.delete("/user/delete", headers={
        "X-UUID": users["lisa"]["uuid"],
        "X-OTP": users["lisa"]["otp"]
    }, data={
        "uuid": users["jack"]["uuid"]
    })
    assert res.status_code == 200
    expected = "User is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # check if lisa exists
    res = client.post("/user/login", headers={
        "X-UUID": users["lisa"]["uuid"],
        "X-PERM": False
    })
    assert res.status_code == 401
    expected = "Either username or password is incorrect"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

def test_logout(app, client):
    res = client.delete("/user/logout", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 200
    expected = "You are logged out"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # logged out again, makes no difference
    res = client.delete("/user/logout", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid uuid
    res = client.delete("/user/logout", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["root"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid otp
    res = client.delete("/user/logout", headers={
        "X-UUID": admins["root"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # invalid user
    res = client.delete("/user/logout", headers={
        "X-UUID": admins["dummy"]["uuid"],
        "X-OTP": admins["dummy"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing uuid
    res = client.delete("/user/logout", headers={
        "X-OTP": admins["root"]["otp"]
    })
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # missing otp
    res = client.delete("/user/logout", headers={
        "X-UUID": admins["root"]["uuid"]
    })
    assert res.status_code == 400
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.delete("/user/logout", headers={
        "X-UUID": users["jack"]["uuid"],
        "X-OTP": users["jack"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.delete("/user/logout", headers={
        "X-UUID": users["lisa"]["uuid"],
        "X-OTP": users["lisa"]["otp"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

def test_teardown(app, client):
    res = client.post("/user/login", headers={
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 200
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    admins["admin"]["otp"] = actual["message"]

    res = client.post("/user/login", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-PERM": True
    })
    assert res.status_code == 200
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    admins["admin"]["otp"] = actual["message"]

    res = client.delete("/user/delete", headers={
        "X-UUID": admins["admin"]["uuid"],
        "X-OTP": admins["admin"]["otp"]
    })
    assert res.status_code == 200
    expected = "User is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]