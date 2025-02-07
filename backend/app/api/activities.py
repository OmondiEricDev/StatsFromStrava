import os
import redis
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException


loaded = load_dotenv()
router = APIRouter()

address = os.getenv("REDIS_ADDRESS")
reddis_client = redis.Redis(host=address, port=os.getenv("REDIS_PORT"), db=0)

"""
All user activity related endpoints
"""

@router.get("/user/activities")
def get_user_activities():
    
    
    
    return None