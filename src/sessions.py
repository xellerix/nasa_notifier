#!/usr/bin/env python3

import requests
import socket
import json
from datetime import datetime
from config.hec_config import hec_endpoint, hec_token

# Create an authenticated session using the API key
def get_authenticated_session(api_key):
    session = requests.Session()
    session.params['api_key'] = api_key
    return session

def send_to_splunk(event):
    headers = {
            'Authorization': f'Splunk {hec_token}',
            'Content-Type': 'application/json',
            }

    # Get the current hostname
    host = socket.gethostname()

    # Extract the event time in the desired format
    event_time = str(int(datetime.strptime(event["messageIssueTime"], "%Y-%m-%dT%H:%MZ").timestamp()))

    # Customize the JSON event format to match the desired fields and values
    json_event = {
        "time": event_time,
        "host": host,
        "source": "nasa_api",
        "sourcetype": "nasa:notification",
        "event": {
            "message": event["messageBody"],
            },
        "index": "nasa",
        "fields": {
            "messageType": event["messageType"]
        }
    }

    response = requests.post(hec_endpoint, headers=headers, json=json_event, verify=False)
    if response.status_code == 200:
        print('Event sent to Splunk successfully')
    else:
        print(f'Failed to send event to Splunk. Status code: {response.status_code}')
