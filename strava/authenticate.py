import time
import pickle
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from stravalib.client import Client

import os

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URL = 'http://localhost:8000/authorized'

app = FastAPI()
client = Client()

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


@app.get("/")
def read_root():
    authorize_url = client.authorization_url(client_id=CLIENT_ID, redirect_uri=REDIRECT_URL)
    return RedirectResponse(authorize_url)


@app.get("/authorized/")
def get_code(state=None, code=None, scope=None):
    token_response = client.exchange_code_for_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=code)
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    expires_at = token_response['expires_at']
    client.access_token = access_token
    client.refresh_token = refresh_token
    client.token_expires_at = expires_at
    save_object(client, 'auth/client.pkl')
    return {"state": state, "code": code, "scope": scope}
