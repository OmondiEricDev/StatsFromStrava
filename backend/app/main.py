# from typing import Union
import os
import redis
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from app.utils.auth import build_strava_auth_url, init_access_token

from app.api.router_configs import configure_routers

loaded = load_dotenv()
app = FastAPI()
address = os.getenv("REDIS_ADDRESS")
reddis_client = redis.Redis(host=address, port=os.getenv("REDIS_PORT"), db=0)

configure_routers(app)

@app.get("/")
def read_root():
    return {"Hello": "world"}

@app.get("/auth/login")
async def login():
    """ Redirect users to Strava's 3rd party app authorization page
    """
    auth_url = build_strava_auth_url()
    print(auth_url)
    return RedirectResponse(url=auth_url)

@app.get("/auth/callback")
async def callback(code: str):
    """ Called by Strava in response to authorization request

    Args:
        code (str): Strava provided authorization code needed to obtain access token
        NOTE: code can only be used once
    """
    token_data = await init_access_token(code)
    if not token_data:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token!!!")
    
    access_token = token_data.get("access_token")
    expires_at = token_data.get("expires_at")
    expires_in = token_data.get("expires_in")
    refresh_token = token_data.get("refresh_token")
    athlete = token_data.get("athlete")
    athlete_id = athlete.get("id")
    
    user_profile = {
        "username": athlete.get("username"),
        "firstName": athlete.get("firstname"),
        "lastName": athlete.get("lastname"),
        "bio": athlete.get("bio"),
        "city": athlete.get("city"),
        "state": athlete.get("state"),
        "country": athlete.get("country"),
        "sex": athlete.get("sex"),
        "createdAt": athlete.get("created_at"),
        "updatedAt": athlete.get("updated_at"),
        "profileMedium": athlete.get("profile_medium"),
        "profileLarge": athlete.get("profile"),
    }
    
    # Store access token in Redis    
    reddis_client.hset(f"userAuth:{athlete_id}",
               mapping={
                   "access_token": access_token,
                   "refresh_token": refresh_token,
                   "expires_at": expires_at,
                   "expires_in": expires_in,
               },
               )
    
    # Set expiry of current access token to original time - 60 seconds
    ttl = expires_in - 60
    reddis_client.hexpire(f"userAuth:{athlete_id}", ttl, "access_token")
    
    set_ttl = reddis_client.httl(f"userAuth:{athlete_id}", "access_token")
    print(f"Access token TTL: {set_ttl}")
    
    reddis_client.hset(f"userProfile:{athlete_id}",
                       mapping=user_profile)

    return RedirectResponse(url=f"/user/{athlete_id}")
