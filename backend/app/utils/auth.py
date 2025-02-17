import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException
from app.services import redis as redis_service

# Load environment variables
loaded = load_dotenv()
print(loaded)
# Strava OAuth URLs and parameters
STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
APPROVAL_PROMPT = "auto"
AUTH_SCOPE = "read_all,profile:read_all,activity:read,activity:read_all"

# Get environment variables
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI")

def build_strava_auth_url() -> str:
    """Build and return the auth URL
    """
    return (
        f"{STRAVA_AUTH_URL}?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"approval_prompt={APPROVAL_PROMPT}&"
        f"scope={AUTH_SCOPE}"
    )

async def init_access_token(code: str):
    """ Exchanges strava one time access code for an access token
    """
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


async def get_access_token():
    """ Returns access token if valid, otherwise returns a redreshed access token
    """
    user_id = 13974060 # Find a way to dynamically access this
    if await redis_service.access_token_exists(user_id):
        return await redis_service.get_access_token(user_id)
    
    refresh_token = await redis_service.get_refresh_token(user_id)
    refresh_response = await refresh_access_token(refresh_token)
    return refresh_response.get("access_token")


async def refresh_access_token(refresh_token: str):
    """ Refresh the current user's access token for a new one
    Tokens should be refreshed if the TTl is < 3600 seconds
    """
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant__type": "refresh_token",
        "refresh_token": refresh_token
    }
    try:
        response = requests.post(STRAVA_TOKEN_URL, data)
        response.raise_for_status()
        await redis_service.update_user_auth(response)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400,
                            detail=f"Failed to refresh access token: {e}")

