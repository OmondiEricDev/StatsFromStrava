import os
import redis
from dotenv import load_dotenv

loaded = load_dotenv()
redis_address = os.getenv("REDIS_ADDRESS")
redis_client = redis.Redis(host=redis_address,
                           port=os.getenv("REDIS_PORT"),
                           db=0,
                           decode_responses=True)
USER_ID = os.getenv("USER_ID") #NOTE: find a better way for this
# TODO: Implement a thread safe version of this service using aioredis + error handling
# TODO: Implement this as a class

async def access_token_exists(user_id: int) -> bool:
    access_token = redis_client.hget(f"userAuth:{user_id}", "access_token")
    if access_token:
        return True
    return False

async def get_refresh_token(user_id: int) -> str:
    return redis_client.hget(f"userAuth:{user_id}", "refresh_token")

async def get_access_token(user_id: int) -> str:
    if await access_token_exists(user_id):
        token: str = redis_client.hget(f"userAuth:{user_id}", "access_token")
        print(f"ACCESS TOKEN ---> {token}")
        print(token)
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

def create_hash_set(name_key: str, data: dict, ttl = 600000000):
    redis_client.hset(name_key, mapping=data)
    redis_client.expire(name_key, ttl)

async def get_all_hash_fields(hash_set: str):
    return redis_client.hgetall(hash_set)

async def get_hash_field(hash: str, field: str):
    redis_client.hget(hash, field)

def add_to_list(list_name: str, item, ttl = 600000000):
    redis_client.rpush(list_name, item)
    redis_client.expire(list_name, ttl)