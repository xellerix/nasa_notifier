#!/usr/bin/env python3
from dotenv import load_dotenv, find_dotenv
import os
import getpass

# Load environment variables from .env file
load_dotenv(find_dotenv())

hec_endpoint = os.getenv('HEC_ENDPOINT')
hec_token = os.getenv('HEC_TOKEN')

if hec_endpoint is None:
    hec_endpoint = input('Enter the HEC endpoint: ')
    with open('.env', 'a') as f:
        f.write(f'HEC_ENDPOINT={hec_endpoint}\n')

if hec_token is None:
    hec_token = getpass.getpass('Enter your HEC token: ')
    with open('.env', 'a') as f:
        f.write(f'HEC_TOKEN={hec_token}\n')
