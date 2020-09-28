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

- `/device/delete`: `DELETE`, delete a device from system, details are sent by `application/x-www-form-urlencoded` using `key=device_access_key`. `message` will be boolean in string type, `true` is successful, `false` otherwise, working

- `/devices`: `GET`, provides all registered devices to the frontend, working

- `/pulse`: `PUT`, device pulse, key is sent by `application/x-www-form-urlencoded` using `who=device_access_key`. `message` will be `Pulsed` if the device is registered, otherwise `status_code` will be `403`, pulse timestamp will be based on server time, working

- `/events`: `GET`, provides all events to the frontend, working

- `/event/add`: `POST`, add a event to the system, details are sent by `application/x-www-form-urlencoded` using `who=device_access_key&what=event_details&when=unix_timestamp`, in which `what` requires a json. `message` will be a uuid to identify the event. The uuid is required to delete or update the event, working

- `/event/delete`: `DELETE`, delete a event from system, details are sent by `application/x-www-form-urlencoded` using `which=event_uuid`. `message` will be boolean in string type, `true` is successful, `false` otherwise, working

- `/event/update`: `PUT`, update a event, key is sent by `application/x-www-form-urlencoded` using `which=event_uuid&what=event_details&hidden=(0/1)`, in which `what` is the `data` part of the `event_details`, and `hidden` equals `1` is to hide the event, `0` otherwise, one or both of these two parts must be presented. `message` will be `Updated` if the event is found, otherwise `status_code` will be `403`, working

- `/user`: TBD


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