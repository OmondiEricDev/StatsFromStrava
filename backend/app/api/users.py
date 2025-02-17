from fastapi import APIRouter, HTTPException
from app.services import redis as redis_service
from app.services import strava as strava_services
from app.utils import auth as auth_utils

router = APIRouter()

""" All user related endoints """

@router.get("/user/{user_id}")
async def get_user_profile(user_id: int):
    user_profile = await redis_service.get_all_hash_fields(f"userProfile:{user_id}")
    if not user_profile: # TODO: redirect back to auth
        raise HTTPException(status_code=404,
                            detail=f"User not found: {user_id}")
    
    return user_profile

@router.get("/athlete/{user_id}")
async def get_athlete(user_id: int):
    access_token = await redis_service.get_access_token(user_id=user_id)
    print(f"ACCESS TOKEN ----> {access_token}")
    if not access_token:
        raise Exception("No valid accesss token found")
    
    athlete = strava_services.get_athlete(access_token=access_token)
    return athlete
