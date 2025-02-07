import os
import redis
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException


loaded = load_dotenv()
router = APIRouter()

address = os.getenv("REDIS_ADDRESS")
reddis_client = redis.Redis(host=address, port=os.getenv("REDIS_PORT"), db=0)

""" All user related endoints """

@router.get("/user/{user_id}")
def get_user_profile(user_id: int):
    user_profile = reddis_client.hgetall(f"userProfile:{user_id}")
    
    if not user_profile: # TODO: redirect back to auth
        raise HTTPException(status_code=404,
                            detail=f"User not found: {user_id}")
    
    return user_profile