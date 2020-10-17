"""

    This tests route.deivce by using flask test

    Tests includes:
        - route.device
        - lib.libdevice
        - lib.key
        - lib.database
        - lib.libevent

    Author: Haoyu Xu

"""

import json
import uuid
import hashlib

keys = {
    "test": "",
    "ip": "",
    "port": "",
    "zone": "",
    "type": "",
    "name": "",
    "dummy": "Ee_M7mT9wuoeOn8I1GYtC6NQ5EgXyKLZ6tGbyiTA_b0"
}

PRE_DEVICES = []

def test_setup(app, client):
    global PRE_DEVICES
    res = client.get('/devices')
    assert res.status_code == 200
    actual = json.loads(res.get_data(as_text=True))
    PRE_DEVICES = actual["message"]

# test routes
def test_route(app, client):
    res = client.get('/devices')
    assert res.status_code == 200

    res = client.get('/device1')
    assert res.status_code == 404

    res = client.get('/device/{}'.format(keys["dummy"]))
    assert res.status_code == 404

    res = client.post('/device/{}'.format(keys["dummy"]))
    assert res.status_code == 500

    res = client.post('/device/add')
    assert res.status_code == 400

    res = client.delete('/device/{}'.format(keys["dummy"]))
    assert res.status_code == 500

    res = client.delete('/device/delete')
    assert res.status_code == 400

    res = client.put('/device/{}'.format(keys["dummy"]))
    assert res.status_code == 500

    res = client.put('/pulse')
    assert res.status_code == 400

    res = client.put('/device/update')
    assert res.status_code == 400

    # test mismatched method and url
    res = client.get('/device/add')
    assert res.status_code == 400

    res = client.get('/device/delete')
    assert res.status_code == 400

    res = client.get('/pulse')
    assert res.status_code == 400

    res = client.get('/device/update')
    assert res.status_code == 400

    res = client.post('/devices')
    assert res.status_code == 400

    res = client.post("/device/{key}".format(key=keys["dummy"]))
    assert res.status_code == 500 # overrided by flask

    res = client.post('/device/delete')
    assert res.status_code == 400

    res = client.post('/pulse')
    assert res.status_code == 400

    res = client.post('/device/update')
    assert res.status_code == 400

    res = client.delete('/devices')
    assert res.status_code == 400

    res = client.delete("/device/{key}".format(key=keys["dummy"]))
    assert res.status_code == 500 # overrided by flask

    res = client.delete('/device/add')
    assert res.status_code == 400

    res = client.delete('/pulse')
    assert res.status_code == 400

    res = client.delete('/device/update')
    assert res.status_code == 400

    res = client.put('/devices')
    assert res.status_code == 400

    res = client.put("/device/{key}".format(key=keys["dummy"]))
    assert res.status_code == 500 # overrided by flask

    res = client.put('/device/add')
    assert res.status_code == 400

    res = client.put('/device/delete')
    assert res.status_code == 400

# test add device
def test_add(app, client):
    global keys
    # sufficient case
    res = client.post('/device/add', data=dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="camera",
        name="test"
    ))
    assert res.status_code == 200
    # test status_code
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    keys["test"] = actual["message"]

    # duplicated device
    res = client.post('/device/add', data=dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="camera",
        name="test"
    ))
    assert res.status_code == 403
    # test message
    expected = "Device exists"
    assert expected == json.loads(res.get_data(as_text=True))["message"]

    # new device with different ip
    res = client.post('/device/add', data=dict(
        ip="10.0.0.2",
        port=90,
        zone="kitchen",
        type="camera",
        name="test"
    ))
    assert res.status_code == 200
    # test status_code
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    keys["ip"] = actual["message"]

    # new device with different port
    res = client.post('/device/add', data=dict(
        ip="10.0.0.1",
        port=91,
        zone="kitchen",
        type="camera",
        name="test"
    ))
    assert res.status_code == 200
    # test status_code
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    keys["port"] = actual["message"]

    # new device with different zone
    res = client.post('/device/add', data=dict(
        ip="10.0.0.1",
        port=90,
        zone="bedroom",
        type="camera",
        name="test"
    ))
    assert res.status_code == 200
    # test status_code
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    keys["zone"] = actual["message"]

    # new device with different type
    res = client.post('/device/add', data=dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="temperature",
        name="test"
    ))
    assert res.status_code == 200
    # test status_code
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    keys["type"] = actual["message"]

    # new device with different name
    res = client.post('/device/add', data=dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="camera",
        name="test1"
    ))
    assert res.status_code == 200
    # test status_code
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    keys["name"] = actual["message"]

    # test non-int port
    res = client.post('/device/add', data=dict(
        ip="10.0.0.1",
        port="test",
        zone="kitchen",
        type="camera",
        name="test1"
    ))
    assert res.status_code == 400
    # test status_code
    expected = "Bad Request: The browser (or proxy) sent a request that this server could not understand."
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # test missing field
    res = client.post('/device/add', data=dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="camera"
    ))
    assert res.status_code == 400
    # test status_code
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # test empty field
    res = client.post('/device/add', data=dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="camera",
        name=""
    ))
    assert res.status_code == 400
    # test status_code
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

# test devices list
def test_devices_full(app, client):
    res = client.get('/devices')
    assert res.status_code == 200
    # test status_code
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]

def test_device_key(app, client):
    # sufficient case
    res = client.get('/device/{}'.format(keys["test"]))
    assert res.status_code == 200
    # test message
    device = dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="camera",
        name="test"
    )
    device_uuid = str(uuid.UUID(hashlib.md5(str(device).encode('utf-8')).hexdigest()))
    device["uuid"] = device_uuid
    device["key"] = ""
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]["device"]

    # device with different ip
    res = client.get('/device/{}'.format(keys["ip"]))
    assert res.status_code == 200
    # test message
    device = dict(
        ip="10.0.0.2",
        port=90,
        zone="kitchen",
        type="camera",
        name="test"
    )
    device_uuid = str(uuid.UUID(hashlib.md5(str(device).encode('utf-8')).hexdigest()))
    device["uuid"] = device_uuid
    device["key"] = ""
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]["device"]

    # device with different port
    res = client.get('/device/{}'.format(keys["port"]))
    assert res.status_code == 200
    # test message
    device = dict(
        ip="10.0.0.1",
        port=91,
        zone="kitchen",
        type="camera",
        name="test"
    )
    device_uuid = str(uuid.UUID(hashlib.md5(str(device).encode('utf-8')).hexdigest()))
    device["uuid"] = device_uuid
    device["key"] = ""
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]["device"]

    # device with different zone
    res = client.get('/device/{}'.format(keys["zone"]))
    assert res.status_code == 200
    # test message
    device = dict(
        ip="10.0.0.1",
        port=90,
        zone="bedroom",
        type="camera",
        name="test"
    )
    device_uuid = str(uuid.UUID(hashlib.md5(str(device).encode('utf-8')).hexdigest()))
    device["uuid"] = device_uuid
    device["key"] = ""
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]["device"]

    # device with different type
    res = client.get('/device/{}'.format(keys["type"]))
    assert res.status_code == 200
    # test message
    device = dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="temperature",
        name="test"
    )
    device_uuid = str(uuid.UUID(hashlib.md5(str(device).encode('utf-8')).hexdigest()))
    device["uuid"] = device_uuid
    device["key"] = ""
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]["device"]

    # device with different name
    res = client.get('/device/{}'.format(keys["name"]))
    assert res.status_code == 200
    # test message
    device = dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="camera",
        name="test1"
    )
    device_uuid = str(uuid.UUID(hashlib.md5(str(device).encode('utf-8')).hexdigest()))
    device["uuid"] = device_uuid
    device["key"] = ""
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]["device"]

    # non-exist device
    res = client.get('/device/{}'.format(keys["dummy"]))
    assert res.status_code == 404
    # test message
    expected = "Device not found"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

def test_device_update(app, client):
    # empty field
    res = client.put('/device/update', data=dict(
        key=keys["test"],
        fields=""
    ))
    assert res.status_code == 400
    # test message
    expected = "Device is not updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # non-exist field
    res = client.put('/device/update', data=dict(
        key=keys["test"]
    ))
    assert res.status_code == 400
    # test message
    expected = "Device is not updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # non-exist device
    res = client.put('/device/update', data=dict(
        key=keys["dummy"]
    ))
    assert res.status_code == 404
    # test message
    expected = "Device not found"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # sufficient full case
    fields = dict(
        ip="10.0.0.2",
        port=91,
        zone="bedroom",
        type="temperature",
        name="test1"
    )
    res = client.put('/device/update', data=dict(
        key=keys["test"],
        fields=str(json.dumps(fields))
    ))
    assert res.status_code == 200
    # test message
    expected = "Device is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    res = client.get('/device/{}'.format(keys["test"]))
    assert res.status_code == 200
    # test message
    device = fields
    device_uuid = str(uuid.UUID(hashlib.md5(str(device).encode('utf-8')).hexdigest()))
    device["uuid"] = device_uuid
    device["key"] = ""
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]["device"]

    # sufficient ip case
    fields = dict(
        ip="10.0.0.1"
    )
    res = client.put('/device/update', data=dict(
        key=keys["test"],
        fields=str(json.dumps(fields))
    ))
    assert res.status_code == 200
    # test message
    expected = "Device is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    res = client.get('/device/{}'.format(keys["test"]))
    assert res.status_code == 200
    # test message
    device = dict(
        ip="10.0.0.1",
        port=91,
        zone="bedroom",
        type="temperature",
        name="test1"
    )
    device_uuid = str(uuid.UUID(hashlib.md5(str(device).encode('utf-8')).hexdigest()))
    device["uuid"] = device_uuid
    device["key"] = ""
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]["device"]

    # sufficient port case
    fields = dict(
        port=90
    )
    res = client.put('/device/update', data=dict(
        key=keys["test"],
        fields=str(json.dumps(fields))
    ))
    assert res.status_code == 200
    # test message
    expected = "Device is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    res = client.get('/device/{}'.format(keys["test"]))
    assert res.status_code == 200
    # test message
    device = dict(
        ip="10.0.0.1",
        port=90,
        zone="bedroom",
        type="temperature",
        name="test1"
    )
    device_uuid = str(uuid.UUID(hashlib.md5(str(device).encode('utf-8')).hexdigest()))
    device["uuid"] = device_uuid
    device["key"] = ""
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]["device"]

    # sufficient zone case
    fields = dict(
        zone="kitchen"
    )
    res = client.put('/device/update', data=dict(
        key=keys["test"],
        fields=str(json.dumps(fields))
    ))
    assert res.status_code == 200
    # test message
    expected = "Device is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    res = client.get('/device/{}'.format(keys["test"]))
    assert res.status_code == 200
    # test message
    device = device = dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="temperature",
        name="test1"
    )
    device_uuid = str(uuid.UUID(hashlib.md5(str(device).encode('utf-8')).hexdigest()))
    device["uuid"] = device_uuid
    device["key"] = ""
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]["device"]

    # sufficient type case
    fields = dict(
        type="camera"
    )
    res = client.put('/device/update', data=dict(
        key=keys["test"],
        fields=str(json.dumps(fields))
    ))
    assert res.status_code == 200
    # test message
    expected = "Device is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    res = client.get('/device/{}'.format(keys["test"]))
    assert res.status_code == 200
    # test message
    device = device = dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="camera",
        name="test1"
    )
    device_uuid = str(uuid.UUID(hashlib.md5(str(device).encode('utf-8')).hexdigest()))
    device["uuid"] = device_uuid
    device["key"] = ""
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]["device"]

    # sufficient name case
    fields = dict(
        name="test"
    )
    res = client.put('/device/update', data=dict(
        key=keys["test"],
        fields=str(json.dumps(fields))
    ))
    assert res.status_code == 200
    # test message
    expected = "Device is updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    res = client.get('/device/{}'.format(keys["test"]))
    assert res.status_code == 200
    # test message
    device = device = device = dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="camera",
        name="test"
    )
    device_uuid = str(uuid.UUID(hashlib.md5(str(device).encode('utf-8')).hexdigest()))
    device["uuid"] = device_uuid
    device["key"] = ""
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]["device"]

def test_pulse(app, client):
    # sufficient case
    res = client.put('/pulse', data=dict(
        who=keys["test"]
    ))
    assert res.status_code == 200
    # test message
    expected = "Pulsed"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # device with different ip
    res = client.put('/pulse', data=dict(
        who=keys["ip"]
    ))
    assert res.status_code == 200
    # test message
    expected = "Pulsed"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # device with different port
    res = client.put('/pulse', data=dict(
        who=keys["port"]
    ))
    assert res.status_code == 200
    # test message
    expected = "Pulsed"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # device with different zone
    res = client.put('/pulse', data=dict(
        who=keys["zone"]
    ))
    assert res.status_code == 200
    # test message
    expected = "Pulsed"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # device with different type
    res = client.put('/pulse', data=dict(
        who=keys["type"]
    ))
    assert res.status_code == 200
    # test message
    expected = "Pulsed"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # device with different name
    res = client.put('/pulse', data=dict(
        who=keys["name"]
    ))
    assert res.status_code == 200
    # test message
    expected = "Pulsed"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # non-exist device
    res = client.put('/pulse', data=dict(
        who=keys["dummy"]
    ))
    assert res.status_code == 404
    # test message
    expected = "Device not found"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

def test_device_event(app, client):
    # setup
    events = [
        dict(
            who=keys["test"],
            what="""{
                "type": "motion_detected",
                "data": "http://example.com"
            }""",
            when=1501240210993
        ),
        dict(
            who=keys["test"],
            what="""{
                "type": "temperature",
                "data": 30
            }""",
            when=1501240210990
        ),
    ]

    # sufficient case
    # add events
    res = client.post('/event/add', data=events[0])
    assert res.status_code == 200
    events[0]["uuid"] = json.loads(res.get_data(as_text=True))["message"]
    res = client.post('/event/add', data=events[1])
    assert res.status_code == 200
    events[1]["uuid"] = json.loads(res.get_data(as_text=True))["message"]

    # test events
    res = client.get('/device/{}'.format(keys["test"]))
    assert res.status_code == 200
    # test message
    test_events = [
        dict(
            uuid=events[0]["uuid"],
            device="",
            time=events[0]["when"],
            type=json.loads(events[0]["what"])["type"],
            details=json.loads(events[0]["what"])["data"],
            hidden=0
        ),
        dict(
            uuid=events[1]["uuid"],
            device="",
            time=events[1]["when"],
            type=json.loads(events[1]["what"])["type"],
            details=str(json.loads(events[1]["what"])["data"]),
            hidden=0
        )
    ]
    actual = json.loads(res.get_data(as_text=True))
    assert test_events == actual["message"]["events"]

    # tear down
    res = client.delete('/event/delete', data=dict(
        which=events[0]["uuid"]
    ))
    assert res.status_code == 200
    res = client.delete('/event/delete', data=dict(
        which=events[1]["uuid"]
    ))
    assert res.status_code == 200

    res = client.put('/event/clear')
    assert res.status_code == 200

# should be the last test
def test_delete(app, client):
    global keys
    # delete sufficient case
    res = client.delete('/device/delete', data=dict(
        key=keys["test"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Device is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.delete('/device/delete', data=dict(
        key=keys["ip"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Device is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.delete('/device/delete', data=dict(
        key=keys["port"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Device is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.delete('/device/delete', data=dict(
        key=keys["zone"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Device is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.delete('/device/delete', data=dict(
        key=keys["type"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Device is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.delete('/device/delete', data=dict(
        key=keys["name"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Device is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # delete non-exist case
    res = client.delete('/device/delete', data=dict(
        key=keys["dummy"]
    ))
    assert res.status_code == 404
    # test status_code
    expected = "Device not found"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

# test empty devices list
def test_devices_empty(app, client):
    res = client.get('/devices')
    assert res.status_code == 200
    # test status_code
    expected = PRE_DEVICES
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]