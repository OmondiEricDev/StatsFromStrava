import os
import redis
from dotenv import load_dotenv

loaded = load_dotenv()
redis_address = os.getenv("REDIS_ADDRESS")
redis_client = redis.Redis(host=redis_address, port=os.getenv("REDIS_PORT"), db=0)
USER_ID = os.getenv("USER_ID") #NOTE: find a better way for this
# TODO: Implement a thread safe version of this service using aioredis + error handling

async def access_token_exists(user_id: int) -> bool:
    access_token = redis_client.hget(f"userAuth:{user_id}", "access_token")
    if access_token:
        return True
    return False

async def get_refresh_token(user_id: int) -> str:
    return redis_client.hget(f"userAuth:{user_id}", "refresh_token")

async def get_access_token(user_id: int) -> str:
    if await access_token_exists(user_id):
        token = redis_client.hget(f"userAuth:{user_id}", "access_token")
        return token

async def update_user_auth(refresh_response_data):
    redis_client.hset("userAuth:13974060",
                      mapping={
                          "access_token": refresh_response_data.get("access_token"),
                          "refresh_token": refresh_response_data.get("refresh_token"),
                          "expires_at": refresh_response_data.get("expires_at"),
                          "expires_in": refresh_response_data.get("expires_in"),
                      },
                      )
    ttl = refresh_response_data.get("expires_in") - 60
    redis_client.httl("userAuth:13974060", ttl, "access_token")

async def create_hash_set(name: str, data: dict):
    redis_client.hset(f"{name}:{USER_ID}", mapping=data)

async def get_all_hash_fields(hash_set: str):
    return redis_client.hgetall(hash_set)

async def get_hash_field(hash: str, field: str):
    redis_client.hget(hash, field)