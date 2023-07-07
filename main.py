#!/usr/bin/env python3

import time
import json
from datetime import datetime
from config.api_config import get_api_key, url
from src.checkpoint import load_checkpoint, save_checkpoint
from src.sessions import get_authenticated_session, send_to_splunk

def poll_api():
    checkpoint_id = load_checkpoint()
    api_key = get_api_key()

#    # If API key is not found, prompt the user to enter it
#    if api_key is None:
#        get_api_key()
#        api_key = load_api_key()

    session = get_authenticated_session(api_key)

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

        time.sleep(300)

if __name__ == "__main__":
    poll_api()
