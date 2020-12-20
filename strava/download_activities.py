import os
import pickle
import time

import jsonlines

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def check_token():
    if time.time() > client.token_expires_at:
        refresh_response = client.refresh_access_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                       refresh_token=client.refresh_token)
        access_token = refresh_response['access_token']
        refresh_token = refresh_response['refresh_token']
        expires_at = refresh_response['expires_at']
        client.access_token = access_token
        client.refresh_token = refresh_token
        client.token_expires_at = expires_at


def load_object(filename):
    with open(filename, 'rb') as input:
        loaded_object = pickle.load(input)
        return loaded_object


try:
    client = load_object('auth/client.pkl')
    check_token()
    athlete = client.get_athlete()
    print("For {id}, I now have an access token {token}".format(id=athlete.id, token=client.access_token))

    with jsonlines.open('data/activities-all.json', mode='w') as writer:
        for activity in client.get_activities():
            writer.write({
                "id": activity.id,
                "distance": activity.distance.get_num(),
                "moving_time": activity.moving_time.seconds,
                "elapsed_time": activity.elapsed_time.seconds,
                "total_elevation_gain": activity.total_elevation_gain.get_num(),
                "elev_high": activity.elev_high,
                "elev_low": activity.elev_low,
                "average_speed": activity.average_speed.get_num(),
                "max_speed": activity.max_speed.get_num(),
                "average_heartrate": activity.average_heartrate,
                "max_heartrate": activity.max_heartrate,
                "start_date": str(activity.start_date)
            })

except FileNotFoundError:
    print(
        "No access token stored yet, run uvicorn authenticate:app --reload and visit http://localhost:8000/ to get it")
    print("After visiting that url, a pickle file is stored, run this file again to download your activities")
