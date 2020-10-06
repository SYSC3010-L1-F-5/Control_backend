"""

    All email related methods will be here

    Platform: Mailjet
    Emails WILL BE IN THE JUNK/SPAM FOLDER

    Author: Haoyu Xu

"""
import requests
import json
import time

from route.device import Device

from .configs import Configs
CONFIG = Configs().get()

EMAIL = {
    "user": "5bfd66678de399dab6322c0cfb0f972b",
    "pass": "cc293aefb02f9e5d3b53264f124810a2",
    "url": "https://api.mailjet.com/v3.1/send",
    "template": """{{
                    "Messages":[
                        {{
                        "From": {{
                            "Email": "mailjet@halyul.party",
                            "Name": "Home Surveillance System"
                        }},
                        "To": [
                            {{
                            "Email": "{user_email}",
                            "Name": "{username}"
                            }}
                        ],
                        "Subject": "[HSS] {subject}",
                        "TextPart": "{content}",
                        "HTMLPart": "<h3>Dear {username}, {subject}</h3><br />{content}",
                        "CustomID": "{username}"
                        }}
                    ]
                }}"""
}

class Email:
    
    def __init__(self, email=None):
        """

            self.email: user to recieve email

        """
        self.email = CONFIG["email"]

    def send(self, event):
        """

            This method sends an email to the email address defined in config.yml

            Args:
                self: access global variables
                event: event json
            
            Returns:
                int: 200 if success

        """
        content = "{device} {event} at {time}.Raw json: {raw}".format(device=self.__get_device(event["device"]), event=self.__get_event(event["type"]), time=self.__get_time(event["time"]), raw=event)

        template = json.loads(EMAIL["template"].format(user_email=self.email, username="Admin", subject=self.__get_event(event["type"]), content=content))

        response = requests.post(EMAIL["url"], json=template, headers={"'Content-Type":"application/json"}, auth=requests.auth.HTTPBasicAuth(EMAIL["user"], EMAIL["pass"]))

        return response.status_code
        

    def __get_event(self, type):
        """

            This method returns a string related to event type

            Args:
                self: access global variables
                type: event type

            Returns:
                str: a string related to event type

        """
        
        if type == ("motion_detected" or "motion"):
            return "a motion has been detected"
        elif type == "temperature":
            return "temperature has reached threshold"
        elif type == "humidity":
            return "humidity has reached threshold"
        elif type == "pressure":
            return "pressure has reached threshold"

    def __get_device(self, key):
        """

            This method returns a string related to device type

            
            Args:
                self: access global variables
                key: device key

            Returns:
                str: a string related to the device

        """

        settings = Device().settings(key)
        template = "{type} {name} at {ip}:{port} located in {zone} informs that"
        type = None
        zone = settings["zone"]
        name = settings["name"]
        ip = settings["ip"]
        port = settings["port"]
        if settings["type"] == "camera":
            type = "Camera"
        elif settings["type"] == "temperature":
            type = "Temperature sensor"
        elif settings["type"] == "humidity":
            type = "Humidity sensor"
        elif settings["type"] == "pressure":
            type = "Pressure sensor"
        elif settings["type"] == "motion":
            type = "Motion sensor"
        return template.format(type=type, name=name, ip=ip, port=port, zone=zone)

    def __get_time(self, timestamp):
        """

            This method returns a human readable time
            
            Args:
                self: access global variables
                timestamp: unix timestamp

            Returns:
                str: a human readable time

        """
        return time.ctime(int(timestamp / 1000))
        