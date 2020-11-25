"""

    This hardware test tests Sense HAT by using flask test

    Author: Haoyu Xu

"""

from plugins.alert import Alert
from time import sleep
from lib.libconfig import LibConfig
CONFIG = LibConfig(config="test.yml").fetch()

alert = Alert(CONFIG)

def test_on(app, client):
    alert.on(
        dict(
            type="motion_detected"
        )
    )
    sleep(5)

def test_off(app, client):
    alert.off(None)