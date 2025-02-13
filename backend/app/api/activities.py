from fastapi import APIRouter, Depends, HTTPException
from app.services.activities import fetch_user_activities


router = APIRouter()
"""
All endpoints for fetching user related acticity data
"""

@router.get("/user/activities")
async def get_user_activities():
    """Fetch all activities for the logged in user

    Returns:
        _type_: _description_
    """
    try:
        user_activities = await fetch_user_activities()
        return user_activities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch activities: {e}")    
