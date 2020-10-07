import time

from lib.email import Email
from lib.key import Key

# def test_email_full(app, client):
#     email = Email(email="hx-spam@outlook.com")
#     event = {
#         "uuid": Key().uuid("test"),
#         "device": "Central System",
#         "type": "test",
#         "details": "The Central System is running tests!",
#         "time": int(time.time() * 1000),
#         "hidden": 0
#     }
#     status_code = email.send(event=event)
#     assert status_code == 200

def test_email_empty(app, client):
    email = Email(email="")
    event = {
        "uuid": Key().uuid("test"),
        "device": "Central System",
        "type": "test",
        "details": "The Central System is running tests!",
        "time": int(time.time() * 1000),
        "hidden": 0
    }
    status_code = email.send(event=event)
    assert status_code == 302
