import requests
import os
from dotenv import load_dotenv
from fastapi import HTTPException


""" Responsible for all interactions with the strava API"""
loaded = load_dotenv()

# Strava OAuth URLs and parameters
STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
APPROVAL_PROMPT = "auto"
AUTH_SCOPE = "read"

# Strava API base url
STRAVA_API_BASE_URL = "https://www.strava.com/api/v3/"

# Get environment variables
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI")

def get_strava_auth_url() -> str:
    """Builds and returns the url needed to authenticate with strava

    Returns:
        str: Strava auth url
    """
    return(
        f"{STRAVA_AUTH_URL}?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"approval_prompt={APPROVAL_PROMPT}&"
        f"scope={AUTH_SCOPE}"
    )

def get_activities(access_token: str):
    try:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        print("BEFORE sending get activities")
        response = requests.get(
            url=f"{STRAVA_API_BASE_URL}athlete/activities",
            headers=headers)
        print(f"From strava --> {response}")
        response.raise_for_status()
        return response
    except HTTPException as e:
        print(f"{e.status_code} -> Unable to get activities: {e.detail}")
        return None

def get_athlete(access_token: str):
    token = "233dff6328eca275c55a4d1eb75a4466ae2f41e2"
    try:
        _headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            url=f"{STRAVA_API_BASE_URL}athlete",
            headers=_headers
        )
        response.raise_for_status()
        return response
    except HTTPException as e:
        print(f"{e.status_code} --> Unable to get athlete: {e.detail}")
        return None