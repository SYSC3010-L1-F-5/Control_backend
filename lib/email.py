"""

    All email related methods will be here

    Emails WILL BE IN THE JUNK/SPAM FOLDER
    curl -s --user 'api:YOUR_API_KEY' \
    https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages \
    -F from='Excited User <mailgun@YOUR_DOMAIN_NAME>' \
    -F to=YOU@YOUR_DOMAIN_NAME \
    -F to=bar@example.com \
    -F subject='Hello' \
    -F text='Testing some Mailgun awesomeness!'
    Author: Haoyu Xu

"""
import requests
import json
import time

from lib.libdevice import LibDevice

from lib.libconfig import LibConfig
CONFIG = LibConfig().fetch()

EMAIL = {
    "user": "api",
    "pass": "key-49668c4d190eba07505acf7afb620399",
    "url": "https://api.mailgun.net/v3/sender-b.mail.railgun.co/messages",
    "template": """{{
                    "from": "Home Surveillance System <hx-hss@sender-b.mail.railgun.co>",
                    "to": "{username} <{user_email}>",
                    "subject": "[HSS] {subject}",
                    "text": "{content}",
                    "html": "<html><h3>Dear {username}, {subject}</h3><br />{content}</html>"
                }}"""
}

class Email:
    
    def __init__(self, email=None):
        """

            self.email: user to recieve email

        """
        self.email = email or CONFIG["email"]

    def send(self, event):
        """

            This method sends an email to the email address defined in config.yml

            Args:
                self: access global variables
                event: event json
            
            Returns:
                int: 200 if success

        """
        if self.email != "" and self.email is not None:
            content = "{device} {event} at {time}.Raw json: {raw}".format(device=self.__get_device(event["device"]), event=self.__get_event(event["type"]), time=self.__get_time(event["time"]), raw=event)

            template = json.loads(EMAIL["template"].format(user_email=self.email, username="Admin", subject=self.__get_event(event["type"]), content=content))

            response = requests.post(EMAIL["url"], data=template, auth=(EMAIL["user"], EMAIL["pass"]))

            return response.status_code
        else:
            return 302
        

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
        else:
            return type

    def __get_device(self, key):
        """

            This method returns a string related to device type

            
            Args:
                self: access global variables
                key: device key

            Returns:
                str: a string related to the device

        """

        details = LibDevice().details(key)
        if details is None:
            return key
        template = "{type} {name} at {ip}:{port} located in {zone} informs that"
        type = None
        zone = details["zone"]
        name = details["name"]
        ip = details["ip"]
        port = details["port"]
        if details["type"] == "camera":
            type = "Camera"
        elif details["type"] == "temperature":
            type = "Temperature sensor"
        elif details["type"] == "humidity":
            type = "Humidity sensor"
        elif details["type"] == "pressure":
            type = "Pressure sensor"
        elif details["type"] == "motion":
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
        