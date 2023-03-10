import os
from dotenv import load_dotenv
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    data = {"grant_type" : "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token



def get_auth_header(token):

    return {"Authorization" : "Bearer " + token}



def search_for_artist(token, artist_name):

    headers = get_auth_header(token)
    q_url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    
    result = get(q_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']

    return json_result[0]



def spsearch(token, search, type, limit=1):
    
    headers = get_auth_header(token)
    url = "https://api.spotify.com/v1/search?"

    if isinstance(type, str):

        query = f"q={search}&type={type}&limit={limit}"

    else:

        query = f"q={search}&type={','.join(type)}&limit={limit}"

    q_url = url + query

    result = get(q_url, headers=headers)
    json_result = json.loads(result.content)

    return json_result




token = get_token()

types = ['artist']
json_package = spsearch(token, "beebadobe", types)

print(json_package['artists']['items'][0]['name'])


#print(token)