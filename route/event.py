"""

    All eventrelated methods will be here

    - GET /events: show a list of logged events
    - POST /event/add: add a event
    - DELETE /event/delete: user can delete a event by uuid
    - PUT /event/update: user can update the event details

    Message structure: {
        "who": device_access_key,
        "what": event_details,
        "when": unix_timestamp
    }

    Author: Haoyu Xu

    TODO:
        - limit the number of output events on database level on /events

    - GET: The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
    - POST: The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.
    - PUT: The PUT method replaces all current representations of the target resource with the request payload.
    - DELETE: The DELETE method deletes the specified resource.

"""

import json
from flask_restful import Resource, reqparse, request
from lib.database import Database
from lib.key import Key

from lib.email import Email
EMAIL = Email()

from lib.message import Message
MESSAGE = Message()

from lib.libdevice import LibDevice
LIBDEVICE = LibDevice()

from lib.libevent import LibEvent
LIBEVENT = LibEvent()

from lib.plugin import Plugin
PLUGIN = Plugin()

PARASER = reqparse.RequestParser()

class Event(Resource):

    def __init__(self):
        """

            self.database: connects to event table in the database
            self.who: device key
            self.what: event details
            self.when: unix timestamp
            self.uuid: evnet uuid
            self.hidden: 0 for not hidden, 1 for hidden

        """
        self.database = Database("events")
        self.who = None
        self.what = None
        self.when = None
        self.uuid = None
        self.hidden = 0

    @MESSAGE.response
    def get(self, uuid=None):
        """

            This method provides all event details
            to frontend in ascending order

            Args:
                self: access global variables
                uuid: event uuid

            Returns:
                list: event list
                int: status code

        """

        # check url
        urls = [
            "/events",
            "/event/{uuid}".format(uuid=uuid)
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400

        # /events
        if path.split("/")[1] == "events":

            order = {
                "name": "time",
                "value": "DESC"
            }

            events = self.database.get(order=order)
            if events is not None:
                for item in events:
                    item["device"] = LIBDEVICE.details(item["device"])
                    if item["device"] is not None:
                        item["device"]["key"] = ""

            return events, 200
        
        # /event/<uuid>
        if path.split("/")[2] == uuid:
            details = LIBEVENT.details(uuid)
            if details is not None:
                details["device"] = LIBDEVICE.details(details["device"])
                # Hide the key
                details["device"]["key"] = ""
                return details, 200
            else:
                return "Event not found", 404
        
        return "", 404

    @MESSAGE.response
    def post(self):
        """
        
            This method is used by flask restful to 
            provide api access

            Args:
                self: access global variables
            
            Returns:
                string: uuid to identify event
                int: status code
        
        """

        # check url
        urls = [
            "/event/add"
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400

        if path.split("/")[2] != "add":
            return "", 404

        PARASER.add_argument('who', type=str, help='Device Access Key')
        PARASER.add_argument('what', type=str, help='Event details in json')
        PARASER.add_argument('when', type=int, help='Unix Timestamp')
        args = PARASER.parse_args(strict=True)

        self.who = args["who"]
        self.what = json.loads(args["what"])
        self.when = args["when"]

        event = {
            "device": self.who,
            "type": self.what["type"],
            "details": self.what["data"],
            "time": self.when
        }

        self.uuid = Key().uuid(event)
        is_exists = LIBDEVICE.is_exists(self.who)

        if is_exists is False:
            return "Who are you?", 404
        else:
            event = {
                "uuid": self.uuid,
                "device": self.who,
                "type": self.what["type"],
                "details": self.what["data"],
                "time": self.when,
                "hidden": self.hidden
            }

        flag = self.database.insert(data=event)

        if flag is True:
            PLUGIN.on(event=event)
            EMAIL.send(event=event)
            return self.uuid, 200
        else:
            return "Duplicated event", 403

    @MESSAGE.response
    def delete(self):
        """
        
            This method deletes specific event

            Args:
                self: access global variables
            
            Returns:
                string: deleted or not
                int: status code
        
        """
        # check url
        urls = [
            "/event/delete"
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400

        if path.split("/")[2] != "delete":
            return "", 404

        PARASER.add_argument('which', type=str, help='Event UUID')
        args = PARASER.parse_args(strict=True)

        self.uuid = args["which"]
        status = self.database.remove(self.uuid)

        if status is True:
            return "Event is deleted", 200
        else:
            return "Event not found", 404

    @MESSAGE.response
    def put(self):
        """
        
            This method updates specfic event

            TODO:
                - need a better way to update event

            Args:
                self: access global variables
                uuid: event uuid
            
            Returns:
                string: updated or not
                int: status code
        
        """
        # check url
        urls = [
            "/event/clear",
            "/event/update"
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400

        path =  path.split("/")[2]
        if path != "update" and path != "clear":
            return "", 404

        PARASER.add_argument('which', type=str, help='Event UUID')
        PARASER.add_argument('fields', type=str, help='Fields to be updated')
        args = PARASER.parse_args(strict=True)

        # /event/clear
        if path == "clear":
            PLUGIN.off()
            return "OK", 200

        # /event/update
        self.uuid = args["which"]

        status = LIBEVENT.is_exists(self.uuid)

        if status is True:
            where = {
                    "name": "uuid",
                    "value": self.uuid
            }
            if args["fields"] is not None and args["fields"] != "":
                fields = json.loads(args["fields"])
                if "hidden" in fields:
                    self.hidden = fields["hidden"]
                    set = {
                        "name": "hidden",
                        "value": self.hidden
                    }
                    self.database.update(where=where, set=set)
                if "what" in fields:
                    self.what = fields["what"]
                    set = {
                        "name": "details",
                        "value": self.what
                    }
                    self.database.update(where=where, set=set)
                # update event uuid
                details = LibEvent().details(self.uuid)
                event = {
                    "device": details["device"],
                    "type": details["type"],
                    "details": details["details"],
                    "time": details["time"]
                }
                self.uuid = Key().uuid(event)
                set = {
                        "name": "uuid",
                        "value": self.uuid
                    }
                self.database.update(where=where, set=set)
            else:
                return "Event is not updated", 401

            return self.uuid, 200
        else:
            return "Event not found", 404
