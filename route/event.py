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

    Todos:
        - limit the number of output events on database level on /events
        - hidden events slection on /events
        - SenseHAT

    - GET: The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
    - POST: The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.
    - PUT: The PUT method replaces all current representations of the target resource with the request payload.
    - DELETE: The DELETE method deletes the specified resource.

"""

import json
from flask_restful import Resource, reqparse, request
from lib.database import Database
from lib.key import Key

from lib.message import Message
message = Message()

from .device import Device
device = Device()

from lib.configs import Configs
config = Configs().get()

if config["plugins"]["SenseHAT"] is True:
    from plugins.sensehat import SenseHAT
    plugin = SenseHAT()

parser = reqparse.RequestParser()

class Event(Resource):

    def __init__(self):
        self.database = Database("events")
        self.who = None
        self.what = None
        self.when = None
        self.uuid = None
        self.hidden = 0

    @message.response
    def get(self):
        """

            This method provides all event details
            to frontend requires user access key

            Returns:
                list: event list
                int: status code

        """

        if request.path.split("/")[1] != "events":
            return "", 404
        
        return self.database.get(), 200

    @message.response
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

        if request.path.split("/")[2] != "add":
            return "", 404

        parser.add_argument('who', type=str, help='Device Access Key')
        parser.add_argument('what', type=str, help='Event details in json')
        parser.add_argument('when', type=int, help='Unix Timestamp')
        args = parser.parse_args(strict=True)

        self.who = args["who"]
        self.what = json.loads(args["what"])
        self.when = args["when"]
        self.uuid = Key().uuid()
        is_exists = device.is_exists(self.who)

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
            plugin.on(event=event)
            return self.uuid, 200
        else:
            return "Duplicated event", 403

    @message.response
    def delete(self):
        """
        
            This method deletes specific event

            Args:
                self: access global variables
            
            Returns:
                string: deleted or not
                int: status code
        
        """
        if request.path.split("/")[2] != "delete":
            return "", 404

        parser.add_argument('which', type=str, help='Event UUID')
        args = parser.parse_args(strict=True)

        self.uuid = args["which"]
        status = self.database.remove(self.uuid)

        if status is True:
            return "Event is deleted", 200
        else:
            return "Event not found", 404

    @message.response
    def put(self):
        """
        
            This method updates specfic event

            Args:
                self: access global variables
                uuid: event uuid
            
            Returns:
                string: updated or not
                int: status code
        
        """
        path = request.path.split("/")[2]
        if path != "update" and path != "clear":
            return "", 404

        parser.add_argument('which', type=str, help='Event UUID')
        parser.add_argument('what', type=str, help='Event details')
        parser.add_argument('hidden', type=int, help='Hide event')
        args = parser.parse_args(strict=True)

        # /event/clear
        if path == "clear":
            plugin.off()
            return "OK", 200

        # /event/update
        self.uuid = args["which"]
        if args["what"] is not None:
            self.what = args["what"]
        if args["hidden"] is not None:
            self.hidden = args["hidden"]

        status = self.is_exists(self.uuid)

        if status is True:
            data = {
                    "uuid": self.uuid,
                    "hidden": self.hidden,
                    "type": "hidden"
            }
            self.database.update(data)
            if self.what is not None:
                data["details"] = self.what
                data["type"] = "details"
                self.database.update(data)
            
            return "Updated", 200
        else:
            return "Event not found", 404

    def is_exists(self, uuid):
        """

            Check if a event exists in the database

            Args:
                self: access global variables
                uuid: event uuid
            
            Returns: True if exists, False otherwise

        """

        where = {
            "name": "uuid",
            "value": uuid
        }

        # only one entity should be returnd
        data = self.database.get(where=where)

        if len(data) == 0:
            return False
        else:
            return True

    