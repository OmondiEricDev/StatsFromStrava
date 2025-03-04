from fastapi import APIRouter, Depends, HTTPException
from app.services import activity as activity_service


router = APIRouter()
"""
All endpoints for fetching user related activity data
"""

# @router.get("/activities")
# async def get_all_activities():
#     """Fetch all activities for the logged in user
#     """
#     try:
#         user_activities = await activity_service.fetch_all_activities()
#         return user_activities
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to fetch activities: {e}")

@router.get("/activities/{activity_id}")
async def get_activity(activity_id: int):
    """Fetch activity with the given id

    Args:
        activity_id (int): activity id_
    """
    try:
        print(f"fetching activity {activity_id} in activities.py")
        activity_data = await activity_service.fetch_activity_by_id(activity_id)
        return activity_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get activity with id: {activity_id} -> {e}")