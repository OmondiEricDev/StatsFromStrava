from fastapi import APIRouter, HTTPException
from app.services import redis as redis_service

router = APIRouter()

""" All user related endoints """

@router.get("/user/{user_id}")
async def get_user_profile(user_id: int):
    user_profile = await redis_service.get_all_hash_fields(f"userProfile:{user_id}")
    if not user_profile: # TODO: redirect back to auth
        raise HTTPException(status_code=404,
                            detail=f"User not found: {user_id}")
    
    return user_profile