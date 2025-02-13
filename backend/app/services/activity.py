import requests
from typing import List
from app.utils.auth import get_access_token
from app.services import strava as strava_service
from app.models.activitiy import Activity, Activities

""" Logic for fetching user related activities from the Strava API"""

async def fetch_all_activities():
    access_token = await get_access_token()
    
    if not access_token:
        raise Exception("No access token found, please log in")
    
    activities = strava_service.get_activities(access_token=access_token)
    return activities


async def fetch_activity(activity_id: int):
    access_token = await get_access_token()