#!/usr/bin/env python3

import time
import json
from datetime import datetime
from config.hec_config import url
from src.api_key import load_api_key, get_api_key
from src.checkpoint import load_checkpoint, save_checkpoint
from src.api import get_authenticated_session, send_to_splunk

def poll_api():
    checkpoint_id = load_checkpoint()
    api_key = load_api_key()

    # If API key is not found, prompt the user to enter it
    if api_key is None:
        get_api_key()
        api_key = load_api_key()

    session = get_authenticated_session(api_key)

    # for url in ['https://api.nasa.gov/DONKI/notifications?startDate=2023-04-15&endDate=2023-05-31&type=all', 'https://api.nasa.gov/DONKI/notifications?startDate=2023-05-16&endDate=2023-06-15&type=all', 'https://api.nasa.gov/DONKI/notifications?startDate=2023-06-01&endDate=2023-07-01&type=all']:
    while True:
        response = session.get(url)
        data = response.json()
        current_time = datetime.utcnow()

        valid_events = []
        for item in data:
            if item['messageID'] == checkpoint_id:
                break
            else:
                valid_events.append(item)

        if valid_events:
            # Process the valid events
            first_event = valid_events[0]
            first_event_id = first_event['messageID']
            for event in valid_events:
                selected_fields = {
                    "messageIssueTime": event["messageIssueTime"],
                    "messageType": event["messageType"],
                    "messageBody": event["messageBody"]
                }
                json_object = json.dumps(selected_fields, indent=4)
                print(json_object)

                send_to_splunk(selected_fields)

            checkpoint_id = first_event_id
            save_checkpoint(checkpoint_id)

        time.sleep(10)

if __name__ == "__main__":
    poll_api()
