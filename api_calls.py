# This file will hold all of the api calls for Spotify that we may want.

from dotenv import load_dotenv
import os
import requests
from datetime import datetime 

BASE_URL = 'https://api.spotify.com/v1/'



def configure():
    load_dotenv()



def authenticate():
    configure()
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()
    # Save the access token.
    access_token = auth_response_data['access_token']   
    
    return access_token



""" GET Requests for individual artists """
def get_artist(artist_id, access_token):
    # if (datetime.utcnow() - last_authentication).total_seconds() > 3300:
    #     access_key = authenticate()
    #     last_authentication = datetime.utcnow()
    
    headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    r = requests.get(f'{BASE_URL}artists/{artist_id}', headers=headers)

    return r.json()




