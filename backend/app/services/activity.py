import requests
from typing import List
from app.utils.auth import get_access_token
from app.services import strava as strava_service
from app.services import redis as redis_service
from app.services import segment as segment_service
from app.models.activitiy import Activity, Activities

""" Logic for fetching user related activities from the Strava API"""

async def fetch_all_activities_strava():
    access_token = await get_access_token()
    
    if not access_token:
        raise Exception("No access token found, please log in")
    
    activities = strava_service.get_activities(access_token=access_token)
    await save_activities(activities)
    return activities

async def fetch_all_activities():
    """From redis, if not available fetch from Strava"""
    activities_data = await redis_service.get_all_activities()
    
    if activities_data:
        return activities_data

    return await fetch_all_activities_strava()


async def fetch_activity_by_id_strava(activity_id: int):
    access_token = await get_access_token()
    
    if not access_token:
        raise Exception("No access token found, please log in")
    
    try:
        print("getting activity from strava!!!")
        activity_data = await strava_service.get_activity(access_token, activity_id)
        await save_activity(activity_data)
        print("activity saved")
    except Exception as e:
        raise Exception(f"Failed to get activity from Strava: id -> {activity_id} --> {e}")
        
async def fetch_activity_by_id(activity_id):
    access_token = await get_access_token()
    
    if not access_token:
        raise Exception("No access token found, please log in")
    
    activity_data = await redis_service.get_activity_by_id(activity_id)
    
    if not activity_data:
        print(f"Activity {activity_id} not found in local database, fetching from strava...")
        await fetch_activity_by_id_strava(activity_id)
        return await fetch_activity_by_id(activity_id)
    
    return activity_data

async def save_activities(activities: List[dict]):
    """Saves activity to local redis database

    Args:
        activities (List[dict]): List of activity data from Strava API

    Raises:
        Exception: Exception when unable to save to redis
    """
    if not activities:
        raise Exception("Invalid activity data")
    
    for activity_item in activities:
        activity_hash_key = f"activity:{activity_item.get('id')}"
        activity_date_time = activity_item.get("start_date") # 2025-07-17T10:01:49Z
        activity_date, activity_time = activity_date_time.split("T")
        
        activity_data = {
            "id": activity_item.get("id"),
            "type": activity_item.get("type"),
            "name": activity_item.get("name"),
            "distance": activity_item.get("distance"),
            "moving_time": activity_item.get("moving_time"),
            "elevation_gain": activity_item.get("total_elevation_gain"),
            "avg_speed": activity_item.get("average_speed"),
            "max_speed": activity_item.get("max_speed"),
            "avg_power": activity_item.get("average_watts"),
            "max_power": activity_item.get("max_watts"),
            "avg_heartrate": activity_item.get("average_heartrate"),
            "max_heartrate": activity_item.get("max_heartrate"),
            "kudos_count": activity_item.get("kudos_count"),
            "pr_count": activity_item.get("pr_count"),
            "achievements_count": activity_item.get("achievement_count"),
            "kudos_count": activity_item.get("kudos_count"),
            "date": activity_date,
            "time": activity_time
        }
        try:
            redis_service.create_hash_set(
                name_key=activity_hash_key,
                data=activity_data,
                ttl=420) # TODO REMOVE ADTER TESTING
            
            redis_service.add_to_set(
                set_name="activities",
                item=activity_item.get("id"),
                ttl=420) # TODO RMEOVE ADTER TESTING
        except Exception as e:
            print(f"Unable to save activity data to redis -> {e}")
            raise Exception(e)