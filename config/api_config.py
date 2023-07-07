#!/usr/bin/env python3

from dotenv import load_dotenv, find_dotenv
import os
import getpass

# Load environment variables from .env file
load_dotenv(find_dotenv())

url = os.getenv('URL')

def get_api_key():
    api_key = os.getenv('API_KEY')
    if api_key is None:
        api_key = getpass.getpass('Enter your API key: ')
        save_api_key(api_key)
    return api_key

def save_api_key(api_key):
    with open('.env', 'a') as f:
        f.write(f'API_KEY={api_key}\n')
