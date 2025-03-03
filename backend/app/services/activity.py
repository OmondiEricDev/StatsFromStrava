import requests
from typing import List
from app.utils.auth import get_access_token
from app.services import strava as strava_service
from app.services import redis as redis_service
from app.models.activitiy import Activity, Activities

""" Logic for fetching user related activities from the Strava API"""

async def fetch_all_activities_strava():
    access_token = await get_access_token()
    
    if not access_token:
        raise Exception("No access token found, please log in")
    
    activities = strava_service.get_activities(access_token=access_token)
    return activities

async def fetch_all_activities():
    """From dataabse
    """

async def fetch_activity_by_id_strava(activity_id: int):
    access_token = await get_access_token()
    
    if not access_token:
        raise Exception("No access token found, please log in")
    
    try:
        activity_data = await strava_service.get_activity(access_token, activity_id)
        await save_activity(activity_data)
    except Exception as e:
        raise Exception(f"Failed to get activity from Strava: id -> {activity_id} --> {e}")
        
    
async def fetch_activity_by_id(activity_id):
    access_token = await get_access_token()
    
    if not access_token:
        raise Exception("No access token found, please log in")
    
    activity_data = redis_service.get_activity_by_id(activity_id)
    
    if not activity_data:
        print(f"Activity {activity_id} not found in local database, fetching from strava...")
        fetch_activity_by_id_strava(activity_id)
        fetch_activity_by_id(activity_id)
    
    return activity_data

async def save_activity(activity_item):
    """Saves activity to local redis database

    Args:
        activity_item (dict): Dict object containing activity data

    Raises:
        Exception: Exception when unable to save to redis
    """
    if not activity_item:
        raise Exception("Invalid activity data")
    
    activity_hash_key = f"activity:{activity_item.get('id')}"
    
    activity_data = {
        "id": activity_item.get("id"),
        "name": activity_item.get("name"),
        "distance": activity_item.get("distance"),
        "avg_speed": activity_item.get("average_speed"),
        "avg_power": activity_item.get("average_watts"),
        "avg_heartrate": activity_item.get("avergae_heartrate"),
        "kudos_count": activity_item.get("kudos_count")
    }
    
    try:
        redis_service.create_hash_set(
            name_key=activity_hash_key,
            data=activity_data,
            ttl=120) # TODO REMOVE ADTER TESTING
        
        redis_service.add_to_set(
            set_name="activities",
            item=activity_item.get("id"),
            ttl=120) # TODO RMEOVE ADTER TESTING
    except Exception as e:
        print(f"Unable to save activity data to redis -> {e}")