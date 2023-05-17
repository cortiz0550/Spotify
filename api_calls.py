# This file will hold all of the api calls for Spotify that we may want.

from dotenv import load_dotenv
import os
import requests

def configure():
    load_dotenv()

configure()
CLIENT_ID = os.getenv('client_id')
CLIENT_SECRET = os.getenv('client_secret')

AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
})

 # convert the response to JSON
auth_response_data = auth_response.json()

# Save the access token.
access_token = auth_response_data['access_token']

""" Pull some data for an artist """
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

artist_id = '46gyXjRIvN1NL1eCB8GBxo'

r = requests.get(BASE_URL + 'artists/' + artist_id, headers=headers)

r = r.json()

print(r)


