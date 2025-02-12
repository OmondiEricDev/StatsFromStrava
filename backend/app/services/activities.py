import requests
from typing import List
from app.utils.auth import get_access_token
from app.models.activitiy import Activity

""" Logic for fetching user related activities from the Strava API"""

async def fetch_user_activities() -> List[Activity]:
    access_token = await get_access_token()
    
    if not access_token:
        raise Exception("No access token found, please log in")
    return True