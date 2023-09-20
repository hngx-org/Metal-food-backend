#!/usr/bin/python3
import requests
from getpass import getpass

password = getpass("Please enter your password ")

endpoint= "http://localhost:8000/api/users/signup/"

get_response = requests.post(endpoint, json={"first_name": "test",
                                             "last_name": "test me",
                                             "email": "whodeycheck@otp.com",
                                             "password": password})

print(get_response.json())
