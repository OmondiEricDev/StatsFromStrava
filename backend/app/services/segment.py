from app.utils.auth import get_access_token
from app.services import strava as strava_service
from app.services import redis_service as redis_service

async def fetch_starred_segments_from_strava():
    access_token = await get_access_token()

    if not access_token:
        raise Exception("No access token, please log in!")

    try:
        starred_segments = await strava_service.get_starred_segments(access_token=access_token)
        formatted_segments = list()

        # Change to desired format
        for segment_item in starred_segments:
            athlete_pr_effort = segment_item.get("athlete_pr_effort")
            if not athlete_pr_effort:
                athlete_pr_effort = {
                    "id": "NA",
                    "activity_id": "NA",
                    "start_date": "NA",
                    "is_kom": False
                }
                segment_item["pr_time"] = "NA"
            segment_data = {
                "id": segment_item.get("id"),
                "name": segment_item.get("name"),
                "distance": segment_item.get("distance"),
                "climb_category": segment_item.get("climb_category"),
                "pr_time": segment_item.get("pr_time"),
                "pr_effort_id": athlete_pr_effort.get("id"),
                "pr_activity_id": athlete_pr_effort.get("activity_id"),
                "pr_date": athlete_pr_effort.get("start_date"),
                "K/QOM": str(athlete_pr_effort.get("is_kom"))
            }

            formatted_segments.append(segment_data)

        await save_starred_segments(formatted_segments) # TODO: Implement this as a background task
        return formatted_segments
    except Exception as e:
        raise Exception(f"Segment service :: Unable to fetch segments from Strava! {e}")

async def fetch_starred_segments():
    """Fetch starred segments data from redis, if not available fetch from strava
    """
    segments_data = await redis_service.get_starred_segments("starredSegments")
    if segments_data:
        return segments_data
    
    return await fetch_starred_segments_from_strava()

async def fetch_segment_by_id(segment_id: int):
    pass

async def save_starred_segments(segments: list):
    for segment_item in segments:
        segment_hash_key = f"starredSegment:{segment_item.get('id')}"

        try:
            redis_service.create_hash_set(
                name_key=segment_hash_key,
                data=segment_item,
                ttl=21600)

            redis_service.add_to_set(
                set_name="starredSegments",
                item=segment_item.get("id"),
                ttl=21600)
        except Exception as e:
            print(f"Unable to save data to redis -> {e}")