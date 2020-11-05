# The Central System

Author: Haoyu Xu (haoyu.xu@carleton.ca)

Current the User Interface is running under [http://10.1.0.1:5000](http://10.1.0.1:5000])

## Run

### Direct host

Requirements:

- Python 3.0+

``` bash
$ pip install -r requirements.txt
$ flask run --no-debugger --host=0.0.0.0 --port=5000
```

The Central System will be up and running at [http://localhost:5000](http://localhost:5000]) and listen to [http://0.0.0.0:5000](http://0.0.0.0:5000)


### Docker-compose

``` yaml
version: "3.8"
services:
  hss-backend:
    build: ./hss/backend
    container_name: hss_backend_container
    environment:
      - TZ=America/Toronto
    volumes:
      - ./hss/backend:/backend:rw
    expose:
      - "5000"
    ports:
      - "5000:5000"
    restart: always
```

## Test

Requirements:

- PyTest

``` bash
$ python -m pytest --disable-warnings -vv
```

## Development

### Message Structure

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

### Routes

| URL | Medthod | Description | Requestion Formate | Response Formate |
|---|---| --------- | ---| --- |
| / | GET | currently for test only | N/A | string: "Hello world" |
| /config | GET | response server configuration file, working | `X-UUID` and `X-OTP` in `Headers` with `admin` user permission | JSON/null: system config | 
| /devices | GET | provides a list all registered devices | `X-UUID` and `X-OTP` in `Headers` | list/null: a list of devices |
| /device/<key> | GET | get a specific data collecotr details | `X-UUID` and `X-OTP` in `Headers` | JSON/null: details of one device |
| /device/add | POST | add a device to the system | `X-UUID` and `X-OTP` in `Headers` with `admin` user permission; `ip: device_ip`, `port: device_port`, `zone: device_zone`, `type: device_type`, `name: device_name` in `Form` field | string: device access `key` |
| /device/delete | DELETE | delete a device from system | `X-UUID` and `X-OTP` in `Headers` with `admin` user permission; `key: device key` in `form` field | string: "Device is deleted"; "Device not found" |
| /device/update | PUT | update a device | `X-UUID` and `X-OTP` in `Headers` with `admin` user permission; `which: device key`, `fields: '{"ip": device_ip, "port": device_port, "zone": device_zone, "type": device_type, "name"=device_name, is_enabled: (0/1)}'` in `Form` field | string: "Device is updated"; "Device is not updated" |
| /pulse | PUT | device pulse | `who: device key` in `Form` field | string/int: "Device not found"; `1` or `0` if the device is found and `is_enabled` is set to true/false |
| /events | GET | provides all events | `X-UUID` and `X-OTP` in `Headers` | list/null: a list of events |
| /event/<uuid> | GET | get a specific event details |  `X-UUID` and `X-OTP` in `Headers` | JSON/null: details of an event | 
| /event/add | POST | add a event | `who: device_access_key`, `what: '{"type": event_type, "data": event_detail}'`, `when: unix_timestamp` in `Form` field | string: uuid of the event |
| /event/delete | DELETE | delete an event | `X-UUID` and `X-OTP` in `Headers` with `admin` user permission; `which: event_uuid` in `Form` field | string: "Event is deleted"; "Event not found" |
| /event/update | PUT | update a event | `X-UUID` and `X-OTP` in `Headers` with `admin` user permission; `which: event_uuid`, `fields: '{"what": event_details, "hidden": (0/1)}'` in `Form` field | string: a new event uuid; "Event is not updated" |
| /event/clear | PUT | clear plugin status | `X-UUID` and `X-OTP` in `Headers` with `admin` user permission | string: "OK" |
| /user | GET | get details of a user | `X-UUID` and `X-OTP` in `Headers` | JSON: user details |
| /users | GET | get a list of all users | `X-UUID` and `X-OTP` in `Headers` with `admin` user permission | list: a list of all users |
| /user/<uuid> | GET | get details of a user | `X-UUID` and `X-OTP` in `Headers` with `admin` user permission | JSON: user details |
| /user/login | POST | login a user | `X-UUID` and `X-PERM: true/false, remember the login status or not` in `Headers` | string: one-time user password |
| /user/add | POST | add a new user | `X-UUID` and `X-OTP` in `Headers` with `admin` user permission; `username`, `password: md5 hashed`, `type: admin/regular, user permission type` in `Form` field | string: "User is added"; "User either exists or unexpected error happened" |
| /user/logout | DELETE | logout a user | `X-UUID` and `X-OTP` in `Headers` | string: "You are logged out" |
| /user/delete | DELETE | delete a user | `X-UUID` and `X-OTP` in `Headers` with `admin` user permission; `uuid: the uuid of the user to delete` in `Form` field | string: "User is deleted"; "User not found"|
| /user/update | PUT | update a user | `X-UUID` and `X-OTP` in `Headers`; `fields: '{"uuid": user_uuid ("admin" permission is required if presented), "type": "admin"/"regular" ("admin" permission is required if presented), "username": username, "password": md5-hashed_password}'` in `Form` field | string: "<fields> has/have been updated"; "<fields> is/are not being updated" |

`X-UUID`: sha256-hashed `username:<username>;password:<md5-hashed password>`
`X-OTP`: one-time user password

### Plugins

May add localhost modules to the system. Currently, SenseHAT plugin is being developed.

### Device Requirements

1. use `PUT` to send pulse data to `/pulse`, message structure: `who=device_access_key`
2. use `PUT` to send events to `/event/add`, message structure: `who=device_access_key&what=event_details&when=unix_timestamp`

#### `what=event_details`

##### Camera

``` json
{
    "type": event_type,
    "data": replay_file_link
}
```

###### type

- `motion_detected`: Detected motion in the camera frame

###### data

The link to access the replay file

##### Temperature, Humidity, Pressure, Motion Sensors

``` json
{
    "type": event_type,
    "data": data
}
```

###### type

- `temperature`: for temperature sensors
- `humidity`: for humidity sensors
- `pressure`: for pressure sensors
- `motion`: for motion sensors

###### data

in string or numeric type 
