import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables
loaded = load_dotenv()
print(loaded)
# Strava OAuth URLs and parameters
STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
APPROVAL_PROMPT = "auto"
AUTH_SCOPE = "read"

# Get environment variables
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI")

"""Build and return the auth URL
"""
def build_strava_auth_url() -> str:
    return (
        f"{STRAVA_AUTH_URL}?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"approval_prompt={APPROVAL_PROMPT}&"
        f"scope={AUTH_SCOPE}"
    )

""" Exchanges strava one time access code for an access token
"""
async def get_strava_access_token(code: str):
    data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code"
        }
    try:
        response = requests.post(STRAVA_TOKEN_URL, data)
        response.raise_for_status() # Raises an error if any
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400,
                            detail=f"Failed to fetch access token: {e}")


""" Refresh the current user's access token for a new one
"""
async def refresh_access_token(refresh_token: str):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant__type": "refresh_token",
        "refresh_token": refresh_token
    }
    try:
        response = requests.post(STRAVA_TOKEN_URL, data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400,
                            detail=f"Failed to refresh access token: {e}")

