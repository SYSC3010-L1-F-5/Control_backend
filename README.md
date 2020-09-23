# Backend of the Control Centre

Author: Haoyu Xu (haoyu.xu@carleton.ca)

## Message structure

```` json
}
    "message": "message",
    "status_code": 200,
    "time": 1600895950363
}
````

- message: the message to read

- status_code: if the request is successful. It is based on HTTP status code, only `200` will reply requested message, other code will response error in the `message`

- time: Unix timestamp

## Routes

- `/`: currently for test only

- `/config`: response configuration file

- `/device/add/<string:zone>/<string:type>/<string:name>`: add a device to the system. `message` will be the device access key. The key is required for any operations on device.

- `/device/delete/<string:key>`: delete a device from system. `message` will be boolean in string type, `true` is successful, `false` otherwise

- `/device/pulse/<string:key>`: device pulse. `message` will be `OK` if the device is registered, otherwise `status_code` will be `403`

- `/devices`: provides all registered devices to the frontend

- `/user`: TBD

- `/event`: TBD

- `/email`: TBD

## Plugins

May add localhost modules to the system. Currently, SenseHAT plugin is being developed.

