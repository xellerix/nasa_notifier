#!/usr/bin/env python3

import os
import getpass

api_key_file = 'data/api.key'

# Save the API key to a file
def save_api_key(api_key):
    with open(api_key_file, 'w') as file:
        file.write(api_key)

# Load the API key from a file
def load_api_key():
    if not os.path.isfile(api_key_file):
        return None

    with open(api_key_file, 'r') as file:
        api_key = file.read().strip()
        return api_key

# Prompt the user to enter an API key and save it
def get_api_key():
    api_key = getpass.getpass('Enter your API key: ')
    save_api_key(api_key)
