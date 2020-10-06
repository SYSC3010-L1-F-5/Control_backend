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

- `/device/<key>`: `GET`, get a specific data collecotr info from system. `message` will be json type or `null`, working

- `/devices`: `GET`, provides all registered devices to the frontend, working

- `/pulse`: `PUT`, device pulse, key is sent by `application/x-www-form-urlencoded` using `who=device_access_key`. `message` will be `Pulsed` and `200` if the device is registered, `Device not found` and `200` otherwise, pulse timestamp will be based on server time, working

- `/events`: `GET`, provides all events to the frontend, working

- `/event/add`: `POST`, add a event to the system, details are sent by `application/x-www-form-urlencoded` using `who=device_access_key&what=event_details&when=unix_timestamp`, in which `what` requires a json, when a new event is recieved, depends on its type, plugin may turn on. `message` will be a uuid to identify the event. The uuid is required to delete or update the event, working

- `/event/delete`: `DELETE`, delete a event from system, details are sent by `application/x-www-form-urlencoded` using `which=event_uuid`. `message` will be string type, `Event is deleted` and `200` is successful, `Event not found` and `404` otherwise, working

- `/event/update`: `PUT`, update a event, key is sent by `application/x-www-form-urlencoded` using `which=event_uuid&what=event_details&hidden=(0/1)`, in which `what` is the `data` part of the `event_details`, and `hidden` equals `1` is to hide the event, `0` otherwise, one or both of these two parts must be presented. `message` will be `Updated` if the event is found, otherwise `status_code` will be `403`, working

- `/event/clear`: `PUT`, clear plugin status, working

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
    "message": "Ee_M7mT9wuoeOn8I1GYtC6NQ5EgXyKLZ6tGbyiTA_b0",
    "status_code": 200,
    "time": 1601333473239
}
```

### `/device/delete`

Used by **frontend**, to delete a data collector

``` shell
$ curl -X DELETE http://10.1.0.1:5000/device/delete -d "key=Ee_M7mT9wuoeOn8I1GYtC6NQ5EgXyKLZ6tGbyiTA_b0"
{
    "message": "Device is deleted",
    "status_code": 200,
    "time": 1601334029682
}
```

### `/device/Ee_M7mT9wuoeOn8I1GYtC6NQ5EgXyKLZ6tGbyiTA_b0`

Used by **frontend**, to get a specific data collecotr info

``` shell
$ curl -X DELETE http://10.1.0.1:5000/device/delete -d "key=Ee_M7mT9wuoeOn8I1GYtC6NQ5EgXyKLZ6tGbyiTA_b0"
{
    "message": {
                "ip": "10.0.0.1",
                "port": 90,
                "zone": "kitchen",
                "type": "camera",
                "name": "test1",
                "key": "HaNQ3xeKcnj416E3PZGD35-OMTziKZ78W15bT1JDBC4",
                "pulse": 1601256444500
            },
    "status_code": 200,
    "time": 1601334029682
}
```

### `/pulse`

Used by **data collector**, update it status to prevent unexpected offline

``` shell
$ curl -X PUT http://10.1.0.1:5000/pulse -d "who=Ee_M7mT9wuoeOn8I1GYtC6NQ5EgXyKLZ6tGbyiTA_b0"
{
    "message": "Pulsed",
    "status_code": 200,
    "time": 1601333626575
}
```

### `/event/add`

Used by **data collector**, add an event to the system when a new event is triggered

``` shell
$ curl -X POST http://10.1.0.1:5000/event/add -d "who=Ee_M7mT9wuoeOn8I1GYtC6NQ5EgXyKLZ6tGbyiTA_b0&what={\"type\":\"motion_detected\",\"data\":\"https://example.com/123\"}&when=1501240210990"
{
    "message": "67a87a35-5508-4dba-9b40-d810a9af3992",
    "status_code": 200,
    "time": 1601333715823
}
```

### `/event/update`

Used by **data collector** or **frontend**, update an existing event

``` shell
$ curl -X PUT http://10.1.0.1:5000/event/update -d "which=67a87a35-5508-4dba-9b40-d810a9af3992&what=https://example.org&hidden=1"
{
    "message": "Updated",
    "status_code": 200,
    "time": 1601333830783
}
```

### `/event/delete`

Used by **data collector** or **frontend**, delete an existing event

``` shell
$ curl -X DELETE http://10.1.0.1:5000/event/delete -d "which=67a87a35-5508-4dba-9b40-d810a9af3992"
{
    "message": "Event is deleted",
    "status_code": 200,
    "time": 1601333878427
}
```

### `/event/clear`

Used by **frontend**, clear plugin status on the central system

``` shell
$ curl -X PUT http://10.1.0.1:5000/event/clear
{
    "message": "OK",
    "status_code": 200,
    "time": 1601333900393
}
```

### `/events`

Used by **frontend**, receive a list of events 

``` shell
$ curl -X GET http://10.1.0.1:5000/events
{
    "message": [
        {
            "uuid": "0698143b-ed44-4f07-96a0-077264501497",
            "device": "HaNQ3xeKcnj416E3PZGD35-OMTziKZ78W15bT1JDBC4",
            "time": 1601248329679,
            "type": "motion_detected",
            "details": "https://example.org/123",
            "hidden": 1
        },
        {
            "uuid": "df3c65b0-c51e-4172-9a96-975a602fe4a0",
            "device": "Na5adCHPj7p4X35Od_hQ8oQkDq8uImV_yGfPQ_3--UU",
            "time": 1601240112209,
            "type": "temperature",
            "details": "10",
            "hidden": 0
        },
        {
            "uuid": "61ab4260-122c-4125-bc72-4de29a8e4c82",
            "device": "Na5adCHPj7p4X35Od_hQ8oQkDq8uImV_yGfPQ_3--UU",
            "time": 1601240112209,
            "type": "temperature",
            "details": "100",
            "hidden": 0
        },
        {
            "uuid": "c82af6f8-d41a-40e9-a5fe-f2fc7cef6a92",
            "device": "Na5adCHPj7p4X35Od_hQ8oQkDq8uImV_yGfPQ_3--UU",
            "time": 1601240112209,
            "type": "humidity",
            "details": "100",
            "hidden": 0
        },
        {
            "uuid": "31ce8ed3-2904-42a0-9745-ec7d51ed43d5",
            "device": "Na5adCHPj7p4X35Od_hQ8oQkDq8uImV_yGfPQ_3--UU",
            "time": 1601240112209,
            "type": "humidity",
            "details": "1300",
            "hidden": 0
        },
        {
            "uuid": "bcf578db-c750-459a-8384-72de9def8fcd",
            "device": "Na5adCHPj7p4X35Od_hQ8oQkDq8uImV_yGfPQ_3--UU",
            "time": 1601240112209,
            "type": "pressure",
            "details": "1300",
            "hidden": 0
        },
        {
            "uuid": "772b2ee1-ae8b-4a1f-a8af-9af72d155aae",
            "device": "Na5adCHPj7p4X35Od_hQ8oQkDq8uImV_yGfPQ_3--UU",
            "time": 1601240312296,
            "type": "motion_detected",
            "details": "https://example.com/123",
            "hidden": 0
        },
        {
            "uuid": "0a05ac60-7442-42bf-8433-5f557d363c7e",
            "device": "Na5adCHPj7p4X35Od_hQ8oQkDq8uImV_yGfPQ_3--UU",
            "time": 1501240210990,
            "type": "motion_detected",
            "details": "https://example.com/123",
            "hidden": 0
        }
    ],
    "status_code": 200,
    "time": 1601333948566
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
            "name": "test1",
            "key": "HaNQ3xeKcnj416E3PZGD35-OMTziKZ78W15bT1JDBC4",
            "pulse": 1601256444500
        },
        {
            "ip": "10.0.0.1",
            "port": 90,
            "zone": "kitchen",
            "type": "camera",
            "name": "test10",
            "key": "Na5adCHPj7p4X35Od_hQ8oQkDq8uImV_yGfPQ_3--UU",
            "pulse": -1
        }
    ],
    "status_code": 200,
    "time": 1601334054916
}
```