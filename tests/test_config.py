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

def test_config(app, client):
    res = client.get('/config')
    assert res.status_code == 200
    expected = __get_config()
    # any message with decorator @message.response only tests message part
    assert expected == json.loads(res.get_data(as_text=True))["message"]

def __get_config():
    path = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "config.yml")
    try:
        config = yaml.safe_load(open(path, "r"))
    except yaml.YAMLError as e:
        print(e)
        sys.exit()
    return config
