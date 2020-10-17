"""

    This tests route.event by using flask test
    
    Tests includes:
        - route.event
        - lib.libdevice
        - lib.key
        - lib.database
        - lib.libevent

    Author: Haoyu Xu

"""

import json
from shutil import which
import uuid
import hashlib

uuids = {
    "who1": "",
    "who2": "",
    "what.type": "",
    "what.data": "",
    "when": "",
    "dummy": "6ef7798e-7b46-9193-1b01-7649c8e78104"
}

keys = {
    "test": "",
    "test1": ""
}

# Setup a device for test
DEVICES = [
    dict(
        ip="10.0.0.1",
        port=90,
        zone="kitchen",
        type="camera",
        name="test"
    ),
    dict(
        ip="10.0.0.2",
        port=90,
        zone="kitchen",
        type="temperature",
        name="test1"
    )
]

DEVICES_UUIDS = [
    str(uuid.UUID(hashlib.md5(str(DEVICES[0]).encode('utf-8')).hexdigest())),
    str(uuid.UUID(hashlib.md5(str(DEVICES[1]).encode('utf-8')).hexdigest()))
]

PRE_EVENTS = []

# test routes
def test_route(app, client):
    res = client.get('/events')
    assert res.status_code == 200

    res = client.get('/events1')
    assert res.status_code == 404

    res = client.get('/event/{}'.format(uuids["dummy"]))
    assert res.status_code == 404

    res = client.post('/event/{}'.format(uuids["dummy"]))
    assert res.status_code == 500

    res = client.post('/event/add')
    assert res.status_code == 400

    res = client.delete('/event/{}'.format(uuids["dummy"]))
    assert res.status_code == 500

    res = client.delete('/event/delete')
    assert res.status_code == 400

    res = client.put('/event/{}'.format(uuids["dummy"]))
    assert res.status_code == 500

    res = client.put('/event/clear')
    assert res.status_code == 200

    res = client.put('/event/update')
    assert res.status_code == 400

    # test mismatched method and url
    res = client.get('/event/add')
    assert res.status_code == 400

    res = client.get('/event/delete')
    assert res.status_code == 400

    res = client.get('/event/clear')
    assert res.status_code == 400

    res = client.get('/event/update')
    assert res.status_code == 400

    res = client.post('/events')
    assert res.status_code == 400

    res = client.post("/event/{uuid}".format(uuid=uuids["dummy"]))
    assert res.status_code == 500 # overrided by flask

    res = client.post('/event/delete')
    assert res.status_code == 400

    res = client.post('/event/clear')
    assert res.status_code == 400

    res = client.post('/event/update')
    assert res.status_code == 400

    res = client.delete('/events')
    assert res.status_code == 400

    res = client.delete("/event/{uuid}".format(uuid=uuids["dummy"]))
    assert res.status_code == 500 # overrided by flask

    res = client.delete('/event/add')
    assert res.status_code == 400

    res = client.delete('/event/clear')
    assert res.status_code == 400

    res = client.delete('/event/update')
    assert res.status_code == 400

    res = client.put('/events')
    assert res.status_code == 400

    res = client.put("/event/{uuid}".format(uuid=uuids["dummy"]))
    assert res.status_code == 500 # overrided by flask

    res = client.put('/event/add')
    assert res.status_code == 400

    res = client.put('/event/delete')
    assert res.status_code == 400

def test_setup(app, client):
    res = client.post('/device/add', data=DEVICES[0])
    assert res.status_code == 200
    # test status_code
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    keys["test"] = actual["message"]

    res = client.post('/device/add', data=DEVICES[1])
    assert res.status_code == 200
    # test status_code
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]
    keys["test1"] = actual["message"]

    global PRE_EVENTS
    res = client.get('/events')
    assert res.status_code == 200
    actual = json.loads(res.get_data(as_text=True))
    PRE_EVENTS = actual["message"]

# test add events
def test_add(app, client):
    # sufficient case
    res = client.post('/event/add', data=dict(
        who=keys["test"],
        what="""{
            "type": "motion_detected",
            "data": "http://example.com"
        }""",
        when=1501240210993
    ))
    assert res.status_code == 200
    # test status_code
    event = {
        "device": keys["test"],
        "type": "motion_detected",
        "details": "http://example.com",
        "time": 1501240210993
    }
    expected = str(uuid.UUID(hashlib.md5(str(event).encode('utf-8')).hexdigest()))
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    uuids["who1"] = actual["message"]

    # duplicated event
    res = client.post('/event/add', data=dict(
        who=keys["test"],
        what="""{
            "type": "motion_detected",
            "data": "http://example.com"
        }""",
        when=1501240210993
    ))
    assert res.status_code == 403
    # test message
    expected = "Duplicated event"
    assert expected == json.loads(res.get_data(as_text=True))["message"]

    # new event with different device
    res = client.post('/event/add', data=dict(
        who=keys["test1"],
        what="""{
            "type": "temperature",
            "data": "30"
        }""",
        when=1501240210993
    ))
    assert res.status_code == 200
    # test status_code
    event = {
        "device": keys["test1"],
        "type": "temperature",
        "details": "30",
        "time": 1501240210993
    }
    expected = str(uuid.UUID(hashlib.md5(str(event).encode('utf-8')).hexdigest()))
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    uuids["who2"] = actual["message"]

    # new event with different what.type <- error case
    res = client.post('/event/add', data=dict(
        who=keys["test"],
        what="""{
            "type": "temperature",
            "data": "http://example.com"
        }""",
        when=1501240210993
    ))
    assert res.status_code == 400
    # test status_code
    expected = 400
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]

    # new event with different what.type <- normal
    res = client.post('/event/add', data=dict(
        who=keys["test"],
        what="""{
            "type": "temperature",
            "data": 10
        }""",
        when=1501240210993
    ))
    assert res.status_code == 200
    # test status_code
    event = {
        "device": keys["test"],
        "type": "temperature",
        "details": "10",
        "time": 1501240210993
    }
    expected = str(uuid.UUID(hashlib.md5(str(event).encode('utf-8')).hexdigest()))
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    uuids["what.type"] = actual["message"]

    # new event with different what.data
    res = client.post('/event/add', data=dict(
        who=keys["test"],
        what="""{
            "type": "motion_detected",
            "data": "http://example.org"
        }""",
        when=1501240210993
    ))
    assert res.status_code == 200
    # test status_code
    event = {
        "device": keys["test"],
        "type": "motion_detected",
        "details": "http://example.org",
        "time": 1501240210993
    }
    expected = str(uuid.UUID(hashlib.md5(str(event).encode('utf-8')).hexdigest()))
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    uuids["what.data"] = actual["message"]

    # new event with different when
    res = client.post('/event/add', data=dict(
        who=keys["test"],
        what="""{
            "type": "motion_detected",
            "data": "http://example.com"
        }""",
        when=1500000000000
    ))
    assert res.status_code == 200
    # test status_code
    event = {
        "device": keys["test"],
        "type": "motion_detected",
        "details": "http://example.com",
        "time": 1500000000000
    }
    expected = str(uuid.UUID(hashlib.md5(str(event).encode('utf-8')).hexdigest()))
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    uuids["when"] = actual["message"]

    # test non-numeric when
    res = client.post('/event/add', data=dict(
        who=keys["test"],
        what="""{
            "type": "motion_detected",
            "data": "http://example.com"
        }""",
        when="test"
    ))
    assert res.status_code == 400
    # test status_code
    expected = "Bad Request: The browser (or proxy) sent a request that this server could not understand."
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # test non-exist device
    res = client.post('/event/add', data=dict(
        who="Ee_M7mT9wuoeOn8I1GYtC6NQ5EgXyKLZ6tGbyiTA_b0",
        what="""{
            "type": "motion_detected",
            "data": "http://example.org"
        }""",
        when=1500000000000
    ))
    assert res.status_code == 404
    # test status_code
    expected = "Who are you?"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # test missing field
    res = client.post('/event/add', data=dict(
        who=keys["test"],
        when=1501240210993
    ))
    assert res.status_code == 400
    # test status_code
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # test empty field
    res = client.post('/event/add', data=dict(
        who="",
        what="""{
            "type": "motion_detected",
            "data": "http://example.com"
        }""",
        when=1501240210993
    ))
    assert res.status_code == 400
    # test status_code
    expected = "The request has unfulfilled fields"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

# test events list
def test_events_full(app, client):
    res = client.get('/events')
    assert res.status_code == 200
    # test status_code
    expected = 200
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["status_code"]

def test_event_key(app, client):
    # sufficient case
    res = client.get('/event/{}'.format(uuids["who1"]))
    assert res.status_code == 200
    # test message
    event = dict(
        uuid=uuids["who1"],
        device=DEVICES[0],
        time=1501240210993,
        type="motion_detected",
        details="http://example.com",
        hidden=0
    )
    event["device"]["uuid"] = DEVICES_UUIDS[0]
    event["device"]["key"] = ""
    event["device"]["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert event == actual["message"]

    # event with different device
    res = client.get('/event/{}'.format(uuids["who2"]))
    assert res.status_code == 200
    # test message
    event = dict(
        uuid=uuids["who2"],
        device=DEVICES[1],
        time=1501240210993,
        type="temperature",
        details="30",
        hidden=0
    )
    event["device"]["uuid"] = DEVICES_UUIDS[1]
    event["device"]["key"] = ""
    event["device"]["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert event == actual["message"]

    # event with different what.type
    res = client.get('/event/{}'.format(uuids["what.type"]))
    assert res.status_code == 200
    # test message
    event = dict(
        uuid=uuids["what.type"],
        device=DEVICES[0],
        time=1501240210993,
        type="temperature",
        details="10", # <- str
        hidden=0
    )
    event["device"]["uuid"] = DEVICES_UUIDS[0]
    event["device"]["key"] = ""
    event["device"]["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert event == actual["message"]

    # event with different what.data
    res = client.get('/event/{}'.format(uuids["what.data"]))
    assert res.status_code == 200
    # test message
    event = dict(
        uuid=uuids["what.data"],
        device=DEVICES[0],
        time=1501240210993,
        type="motion_detected",
        details="http://example.org",
        hidden=0
    )
    event["device"]["uuid"] = DEVICES_UUIDS[0]
    event["device"]["key"] = ""
    event["device"]["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert event == actual["message"]

    # event with different when
    res = client.get('/event/{}'.format(uuids["when"]))
    assert res.status_code == 200
    # test message
    event = dict(
        uuid=uuids["when"],
        device=DEVICES[0],
        time=1500000000000,
        type="motion_detected",
        details="http://example.com",
        hidden=0
    )
    event["device"]["uuid"] = DEVICES_UUIDS[0]
    event["device"]["key"] = ""
    event["device"]["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert event == actual["message"]

    # non-exist event
    res = client.get('/event/{}'.format(uuids["dummy"]))
    assert res.status_code == 404
    # test message
    expected = "Event not found"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

def test_event_clear(app, client):
    res = client.put('/event/clear')
    assert res.status_code == 200

def test_event_update(app, client):
    # empty field
    res = client.put('/event/update', data=dict(
        which=uuids["who1"],
        fields=""
    ))
    assert res.status_code == 400
    # test message
    expected = "Event is not updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # non-exist field
    res = client.put('/event/update', data=dict(
        which=uuids["who1"]
    ))
    assert res.status_code == 400
    # test message
    expected = "Event is not updated"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # non-exist event
    res = client.put('/event/update', data=dict(
        which=uuids["dummy"]
    ))
    assert res.status_code == 404
    # test message
    expected = "Event not found"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # sufficient full case
    fields = dict(
        what="https://example.com/1",
        hidden=1
    )
    res = client.put('/event/update', data=dict(
        which=uuids["who1"],
        fields=str(json.dumps(fields))
    ))
    assert res.status_code == 200
    # test message
    event = {
        "device": keys["test"],
        "type": "motion_detected",
        "details": "https://example.com/1",
        "time": 1501240210993
    }
    expected = str(uuid.UUID(hashlib.md5(str(event).encode('utf-8')).hexdigest()))
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    uuids["who1"] = actual["message"]
    res = client.get('/event/{}'.format(uuids["who1"]))
    assert res.status_code == 200
    # test message
    event = dict(
        uuid=uuids["who1"],
        device=DEVICES[0],
        time=1501240210993,
        type="motion_detected",
        details="https://example.com/1",
        hidden=1
    )
    event["device"]["uuid"] = DEVICES_UUIDS[0]
    event["device"]["key"] = ""
    event["device"]["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert event == actual["message"]

    # sufficient who2 case
    fields = dict(
        what="10"
    )
    res = client.put('/event/update', data=dict(
        which=uuids["who2"],
        fields=str(json.dumps(fields))
    ))
    assert res.status_code == 200
    # test message
    event = {
        "device": keys["test1"],
        "type": "temperature",
        "details": "10",
        "time": 1501240210993
    }
    expected = str(uuid.UUID(hashlib.md5(str(event).encode('utf-8')).hexdigest()))
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    uuids["who2"] = actual["message"]
    res = client.get('/event/{}'.format(uuids["who2"]))
    assert res.status_code == 200
    # test message
    event = dict(
        uuid=uuids["who2"],
        device=DEVICES[1],
        time=1501240210993,
        type="temperature",
        details="10",
        hidden=0
    )
    event["device"]["uuid"] = DEVICES_UUIDS[1]
    event["device"]["key"] = ""
    event["device"]["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert event == actual["message"]

    # sufficient what.type
    fields = dict(
        what="30",
        hidden=0
    )
    res = client.put('/event/update', data=dict(
        which=uuids["what.type"],
        fields=str(json.dumps(fields))
    ))
    assert res.status_code == 200
    # test message
    event = {
        "device": keys["test"],
        "type": "temperature",
        "details": "30",
        "time": 1501240210993
    }
    expected = str(uuid.UUID(hashlib.md5(str(event).encode('utf-8')).hexdigest()))
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    uuids["what.type"] = actual["message"]
    res = client.get('/event/{}'.format(uuids["what.type"]))
    assert res.status_code == 200
    # test message
    event = dict(
        uuid=uuids["what.type"],
        device=DEVICES[0],
        time=1501240210993,
        type="temperature",
        details="30",
        hidden=0
    )
    event["device"]["uuid"] = DEVICES_UUIDS[0]
    event["device"]["key"] = ""
    event["device"]["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert event == actual["message"]

    # sufficient what.data
    fields = dict(
        what="https://example.org/1",
        hidden=1
    )
    res = client.put('/event/update', data=dict(
        which=uuids["what.data"],
        fields=str(json.dumps(fields))
    ))
    assert res.status_code == 200
    # test message
    event = {
        "device": keys["test"],
        "type": "motion_detected",
        "details": "https://example.org/1",
        "time": 1501240210993
    }
    expected = str(uuid.UUID(hashlib.md5(str(event).encode('utf-8')).hexdigest()))
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]
    uuids["what.data"] = actual["message"]
    res = client.get('/event/{}'.format(uuids["what.data"]))
    assert res.status_code == 200
    # test message
    event = dict(
        uuid=uuids["what.data"],
        device=DEVICES[0],
        time=1501240210993,
        type="motion_detected",
        details="https://example.org/1",
        hidden=1
    )
    event["device"]["uuid"] = DEVICES_UUIDS[0]
    event["device"]["key"] = ""
    event["device"]["pulse"] = -1
    actual = json.loads(res.get_data(as_text=True))
    assert event == actual["message"]

# should be the last test
def test_delete(app, client):
    res = client.delete('/event/delete', data=dict(
        which=uuids["who1"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Event is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.delete('/event/delete', data=dict(
        which=uuids["who2"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Event is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.delete('/event/delete', data=dict(
        which=uuids["what.type"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Event is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.delete('/event/delete', data=dict(
        which=uuids["what.data"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Event is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.delete('/event/delete', data=dict(
        which=uuids["when"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Event is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    # delete non-exist case
    res = client.delete('/event/delete', data=dict(
        which=uuids["dummy"]
    ))
    assert res.status_code == 404
    # test status_code
    expected = "Event not found"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

def test_teardown(app, client):
    res = client.delete('/device/delete', data=dict(
        key=keys["test"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Device is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

    res = client.delete('/device/delete', data=dict(
        key=keys["test1"]
    ))
    assert res.status_code == 200
    # test status_code
    expected = "Device is deleted"
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]

# test empty events list
def test_events_empty(app, client):
    res = client.get('/events')
    assert res.status_code == 200
    # test status_code
    expected = PRE_EVENTS
    actual = json.loads(res.get_data(as_text=True))
    assert expected == actual["message"]