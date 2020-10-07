import json
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
    assert res.status_code == 401

    res = client.delete('/device/{}'.format(keys["dummy"]))
    assert res.status_code == 500

    res = client.delete('/device/delete')
    assert res.status_code == 401

    res = client.put('/device/{}'.format(keys["dummy"]))
    assert res.status_code == 500

    res = client.put('/pulse')
    assert res.status_code == 401

# test add device
def test_add(app, client):
    global keys
    # sufficient case
    res = client.post('/device/add', data=dict(
        ip="10.0.0.1",
        port="90",
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
    assert res.status_code == 500
    # test status_code
    expected = "400 Bad Request: The browser (or proxy) sent a request that this server could not understand."
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # test missing field
    res = client.post('/device/add', data=dict(
        ip="10.0.0.1",
        port="test",
        zone="kitchen",
        type="camera"
    ))
    assert res.status_code == 500
    # test status_code
    expected = "400 Bad Request: The browser (or proxy) sent a request that this server could not understand."
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # test empty field
    res = client.post('/device/add', data=dict(
        ip="10.0.0.1",
        port="test",
        zone="kitchen",
        type="camera",
        name=" "
    ))
    assert res.status_code == 500
    # test status_code
    expected = "400 Bad Request: The browser (or proxy) sent a request that this server could not understand."
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
    hash = str(hashlib.md5(str(device).encode('utf-8')).hexdigest())
    device["hash"] = hash
    device["key"] = keys["test"]
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]

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
    hash = str(hashlib.md5(str(device).encode('utf-8')).hexdigest())
    device["hash"] = hash
    device["key"] = keys["ip"]
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]

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
    hash = str(hashlib.md5(str(device).encode('utf-8')).hexdigest())
    device["hash"] = hash
    device["key"] = keys["port"]
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]

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
    hash = str(hashlib.md5(str(device).encode('utf-8')).hexdigest())
    device["hash"] = hash
    device["key"] = keys["zone"]
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]

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
    hash = str(hashlib.md5(str(device).encode('utf-8')).hexdigest())
    device["hash"] = hash
    device["key"] = keys["type"]
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]

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
    hash = str(hashlib.md5(str(device).encode('utf-8')).hexdigest())
    device["hash"] = hash
    device["key"] = keys["name"]
    device["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert device == actual["message"]

    # non-exist device
    res = client.get('/device/{}'.format(keys["dummy"]))
    assert res.status_code == 404
    # test message
    expected = "Device not found"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

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
    expected = []
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]