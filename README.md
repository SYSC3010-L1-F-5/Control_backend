# Backend of the Control Centre

Author: Haoyu Xu (haoyu.xu@carleton.ca)

## Message Structure

```` json
}
    "message": message,
    "status_code": 200,
    "time": 1600895950363
}
````

- message: the message to read

- status_code: if the request is successful. It is based on HTTP status code, only `200` will reply requested message, other code will response error in the `message`

- time: Unix timestamp

## Routes

- `/`: currently for test only, working

- `/config`: `GET`, response server configuration file, working

- `/device/add`: `POST`, add a device to the system, details are sent by `application/x-www-form-urlencoded` using `ip=device_ip&port=device_port&zone=device_zone&type=device_type&name=device_name`. `message` will be the device access key. The key is required for any operations on device, working

- `/device/delete`: `DELETE`, delete a device from system, details are sent by `application/x-www-form-urlencoded` using `key=device_access_key`. `message` will be string type, `Device is deleted` and `200` is successful, `Device not found` and `404` otherwise, working

- `/device/update`: `PUT`, update a device, key is sent by `application/x-www-form-urlencoded` using `which=event_uuid&fields={"ip": device_ip, "port": device_port, "zone": device_zone, "type": device_type, "name"=device_name}`, in which `ip` is the `device ip`, `port` is the `device port`, `zone` is the `device zone`, `type` is the `device type`, and `name` is the `device name`; one or both of these parts must be presented. `message` will be `Device is updated` if the device is found and updated, otherwise `status_code` will be `401` and `message` will be `Device is not updated`, working

- `/device/<key>`: `GET`, get a specific data collecotr details from system. `message` will be json type or `null`, `200` is successful, `404` otherwise, working

- `/devices`: `GET`, provides all registered devices to the frontend, working

- `/pulse`: `PUT`, device pulse, key is sent by `application/x-www-form-urlencoded` using `who=device_access_key`. `message` will be `Pulsed` and `200` if the device is registered, `Device not found` and `200` otherwise, pulse timestamp will be based on server time, working

- `/events`: `GET`, provides all events to the frontend, working

- `/event/add`: `POST`, add a event to the system, details are sent by `application/x-www-form-urlencoded` using `who=device_access_key&what=event_details&when=unix_timestamp`, in which `what` requires a json, when a new event is recieved, depends on its type, plugin may turn on. `message` will be a uuid to identify the event. The uuid is required to delete or update the event, working

- `/event/delete`: `DELETE`, delete a event from system, details are sent by `application/x-www-form-urlencoded` using `which=event_uuid`. `message` will be string type, `Event is deleted` and `200` is successful, `Event not found` and `404` otherwise, working

- `/event/update`: `PUT`, update a event, key is sent by `application/x-www-form-urlencoded` using `which=event_uuid&fields={"what": data, "hidden": (0/1)}`, in which `what` is the `data` part of the `event_details`, and `hidden` equals `1` is to hide the event, `0` otherwise, one or both of these two parts must be presented. `message` will be a new event uuid if the event is found and updated, otherwise `status_code` will be `401` and `message` will be `Event is not updated`, working

- `/event/clear`: `PUT`, clear plugin status, working

- `/event/<uuid>`: `GET`, get a specific event details from system. `message` will be json type or `null`, `200` is successful, `404` otherwise, working

- `/user`: TBD, not in SYSC 3010 project scope


## Plugins

May add localhost modules to the system. Currently, SenseHAT plugin is being developed.

## Device Requirements

1. use `PUT` to send pulse data to `/pulse`, message structure: `who=device_access_key`
2. use `PUT` to send events to `/event/add`, message structure: `who=device_access_key&what=event_details&when=unix_timestamp`

### `what=event_details`

#### Camera

``` json
{
    "type": event_type,
    "data": replay_file_link
}
```

##### type

- `motion_detected`: Detected motion in the camera frame

##### data

The link to access the replay file

#### Temperature, Humidity, Pressure, Motion Sensors

``` json
{
    "type": event_type,
    "data": data
}
```

##### type

- `temperature`: for temperature sensors
- `humidity`: for humidity sensors
- `pressure`: for pressure sensors
- `motion`: for motion sensors

##### data

in string or numeric type 

## Examples

### `/device/add`

Used by **frontend**, the key needs to be entered to data collector

``` shell
$ curl -X POST http://10.1.0.1:5000/device/add -d "ip=10.0.0.1&port=90&zone=kitchen&type=camera&name=test12"
{
    "message": "MDY2TIQx7HoYL8bHfjszcuhUI-AlGMZPWa8qnysvlGY",
    "status_code": 200,
    "time": 1602096032774
}
```

### `/device/delete`

Used by **frontend**, to delete a data collector

``` shell
$ curl -X DELETE http://10.1.0.1:5000/device/delete -d "key=MDY2TIQx7HoYL8bHfjszcuhUI-AlGMZPWa8qnysvlGY"
{
    "message": "Device is deleted",
    "status_code": 200,
    "time": 1602096436404
}
```

### `/device/update`

Used by **frontend**, update an existing data collector

``` shell
$ curl -X PUT http://10.1.0.1:5000/device/update -d 'key=Si88Eb9DhyMN93s49DGIWKKlOs6YebMqTX6lem8_Kgg&fields={"ip":"10.0.0.2","port":"90","zone":"bedroom","type":"temperature","name":"test1"}'
{
    "message": "Device is updated",
    "status_code": 200,
    "time": 1602096282155
}
```

### `/device/<key>`

Used by **frontend**, to get a specific data collecotr details

``` shell
$ curl -X GET http://10.1.0.1:5000/device/MDY2TIQx7HoYL8bHfjszcuhUI-AlGMZPWa8qnysvlGY
{
    "message": {
        "device": {
            "ip": "10.0.0.1",
            "port": 90,
            "zone": "kitchen",
            "type": "camera",
            "name": "test12",
            "uuid": "aef0f39d-2aca-7520-7c89-fb3350075e74",
            "key": "",
            "pulse": 1602096165307
        },
        "events": [
            {
                "uuid": "f0a2a6b4-50d5-a045-58d4-8c321c7bdebe",
                "device": "",
                "time": 1501240210990,
                "type": "motion_detected",
                "details": "https://example.com/1",
                "hidden": 1
            }
        ]
    },
    "status_code": 200,
    "time": 1602096291861
}
```

### `/pulse`

Used by **data collector**, update it status to prevent unexpected offline

``` shell
$ curl -X PUT http://10.1.0.1:5000/pulse -d "who=MDY2TIQx7HoYL8bHfjszcuhUI-AlGMZPWa8qnysvlGY"
{
    "message": "Pulsed",
    "status_code": 200,
    "time": 1602096165548
}
```

### `/event/add`

Used by **data collector**, add an event to the system when a new event is triggered

``` shell
$ curl -X POST http://10.1.0.1:5000/event/add -d "who=MDY2TIQx7HoYL8bHfjszcuhUI-AlGMZPWa8qnysvlGY&what={\"type\":\"motion_detected\",\"data\":\"https://example.com/123\"}&when=1501240210990"
{
    "message": "6ef7798e-7b46-9193-1b01-7649c8e78104",
    "status_code": 200,
    "time": 1602096190335
}
```

### `/event/update`

Used by **data collector** or **frontend**, update an existing event

``` shell
$ curl -X PUT http://10.1.0.1:5000/event/update -d 'which=6ef7798e-7b46-9193-1b01-7649c8e78104&fields={"what": "https://example.com/1", "hidden": 1}'
{
    "message": "f0a2a6b4-50d5-a045-58d4-8c321c7bdebe",
    "status_code": 200,
    "time": 1602096282155
}
```

### `/event/delete`

Used by **data collector** or **frontend**, delete an existing event

``` shell
$ curl -X DELETE http://10.1.0.1:5000/event/delete -d "which=67a87a35-5508-4dba-9b40-d810a9af3992"
{
    "message": "Event is deleted",
    "status_code": 200,
    "time": 1602096332450
}
```

### `/event/clear`

Used by **frontend**, clear plugin status on the central system

``` shell
$ curl -X PUT http://10.1.0.1:5000/event/clear
{
    "message": "OK",
    "status_code": 200,
    "time": 1602096308789
}
```

### `/event/<uuid>`

Used by **frontend**, to get a specific event details

``` shell
$ curl -X GET http://10.1.0.1:5000/event/f0a2a6b4-50d5-a045-58d4-8c321c7bdebe
{
    "message": {
        "uuid": "f0a2a6b4-50d5-a045-58d4-8c321c7bdebe",
        "device": {
            "ip": "10.0.0.1",
            "port": 90,
            "zone": "kitchen",
            "type": "camera",
            "name": "test12",
            "uuid": "aef0f39d-2aca-7520-7c89-fb3350075e74",
            "key": "",
            "pulse": 1602096165307
        },
        "time": 1501240210990,
        "type": "motion_detected",
        "details": "https://example.com/1",
        "hidden": 1
    },
    "status_code": 200,
    "time": 1602096366890
}
```

### `/events`

Used by **frontend**, receive a list of events 

``` shell
$ curl -X GET http://10.1.0.1:5000/events
{
    "message": [
        {
            "uuid": "f0a2a6b4-50d5-a045-58d4-8c321c7bdebe",
            "device": {
                "ip": "10.0.0.1",
                "port": 90,
                "zone": "kitchen",
                "type": "camera",
                "name": "test12",
                "uuid": "aef0f39d-2aca-7520-7c89-fb3350075e74",
                "key": "",
                "pulse": 1602096165307
            },
            "time": 1501240210990,
            "type": "motion_detected",
            "details": "https://example.com/1",
            "hidden": 1
        }
    ],
    "status_code": 200,
    "time": 1602096377209
}
```

### `/devices`

Used by **frontend**, receive a list of data collectors

``` shell
$ curl -X GET http://10.1.0.1:5000/devices
{
    "message": [
        {
            "ip": "10.0.0.1",
            "port": 90,
            "zone": "kitchen",
            "type": "camera",
            "name": "test12",
            "uuid": "aef0f39d-2aca-7520-7c89-fb3350075e74",
            "key": "",
            "pulse": 1602096165307
        }
    ],
    "status_code": 200,
    "time": 1602096390337
}
```