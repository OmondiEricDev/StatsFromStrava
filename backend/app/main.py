# from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from app.utils.auth import build_strava_auth_url, get_strava_access_token

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "world"}

@app.get("/auth/login")
async def login():
    """ Redirect users to Strava's 3rd party app authorization page
    """
    auth_url = build_strava_auth_url()
    return RedirectResponse(url=auth_url)

@app.get("/auth/callback")
async def callback(code: str):
    """ Called by Strava in response to authorization request

    Args:
        code (str): Strava provided authorization code needed to obtain access token
        NOTE: code can only be used once
    """
    token_data = await get_strava_access_token(code)
    if not token_data:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token!!!")
    
    # TODO: store access token in redis database and associate it with specific athlete
    # ** Example token_data response
    #     {
    #       "token_type": "Bearer",
    #       "expires_at": 1568775134,
    #       "expires_in": 21600,
    #       "refresh_token": "e5n567567...",
    #       "access_token": "a4b945687g...",
    #       "athlete": {
    #           #{summary athlete representation}
    #       }
    #      }
    #
    # ** NOTE: token expiry details --> need to store refresh needed to obtain the next access token
    # ** NOTE: what kind of athlete info is in the summary???
    
    access_token = token_data.get("access_token")
    token_type = token_data.get("token_type")
    expires_at = token_data.get("expires_at")
    refresh_token = token_data.get("refresh_token")
    athlete = token_data.get("athlete")
    
    return token_data
    return {"access_token": access_token,
            "athlete": athlete}