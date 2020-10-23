"""

    This tests route.config by using flask test
    Tests includes route.config and lib.libconfig (used in route.config)

    Author: Haoyu Xu

"""

import json
import os
import pathlib
import yaml
import sys
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

    # login
    res = client.post("/user/login", headers={
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 200
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    admins["admin"]["otp"] = actual["message"]

    # add normal user
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

    users["jack"]["uuid"] = str(hashlib.sha256("username:{username};password:{password}".format(username="jack", password=str(hashlib.md5(str(users["jack"]["password"]).encode('utf-8')).hexdigest())).encode('utf-8')).hexdigest())

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

def test_config(app, client):
    # admin access
    res = client.get('/config', headers={
        "X-OTP": admins["admin"]["otp"],
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 200
    expected = __get_config()
    assert expected == json.loads(res.get_data(as_text=True))["message"]

    # normal user access
    res = client.get('/config', headers={
        "X-OTP": users["jack"]["otp"],
        "X-UUID": users["jack"]["uuid"]
    })
    assert res.status_code == 403
    expected = "You don't have this permission"
    assert expected == json.loads(res.get_data(as_text=True))["message"]

    # invalid user access
    res = client.get('/config', headers={
        "X-OTP": admins["dummy"]["otp"],
        "X-UUID": admins["dummy"]["uuid"]
    })
    assert res.status_code == 401
    expected = "You are unauthorized"
    assert expected == json.loads(res.get_data(as_text=True))["message"]

def test_teardown(app, client):
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

    res = client.post("/user/login", headers={
        "X-UUID": admins["admin"]["uuid"]
    })
    assert res.status_code == 200
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    admins["admin"]["otp"] = actual["message"]

def __get_config():
    path = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "test.yml")
    try:
        config = yaml.safe_load(open(path, "r"))
    except yaml.YAMLError as e:
        print(e)
        sys.exit()
    return config
