import asyncio
import httpx
import streamlit as st
import requests


# Application's backend URL
BACKEND_URL = st.secrets["BACKEND_URL"]
CLIENT_ID = st.secrets["STRAVA_CLIENT_ID"]
CLIENT_SECRET = st.secrets["STRAVA_CLIENT_SECRET"]
REDIRECT_URI = st.secrets["STRAVA_REDIRECT_URI"]

# Strava OAuth URLs
STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/api/v3/oauth/token"
APPROVAL_PROMPT = "auto"
AUTH_SCOPE = "read_all,profile:read_all,activity:read,activity:read_all"

async def main():
    if not st.query_params:
        st.warning("No parameters provided for authentication, try logging in again!")
        return
    
    query_params = st.query_params.to_dict()
    st.query_params.clear()

    if "code" not in query_params:
        st.warning("Authentication code needed for login!!")
        return
    
    code = query_params.get("code")
    print(f"Got the code --------> {code}")
    token_data = await exchange_code_for_token(code=f"{code}")  
    print(f"TOKEN DATA -------> {token_data}")

    if not token_data:
        st.warning("Failed to get token data!!!")
        return

    if "access_token" not in st.session_state:
        st.session_state.access_token = None
        st.session_state.user_id = None
    
    st.session_state.access_token = token_data.get("access_token")
    athlete = token_data.get("athlete")
    st.session_state.user_id = athlete.get("id")
    st.success("Login successful")

    save_auth_data(token_data)
    st.switch_page("main.py")

def handle_callback(query_params):
    # query_params = st.query_params.to_dict()
    if "code" in query_params:
        code = query_params.get("code")
        print(f"Got the code --> {code}")
        token_data = exchange_code_for_token(code=code)        
        print(token_data)
        if token_data:
            st.session_state.access_token = token_data.get("access_token")
            athlete = token_data.get("athlete")
            st.session_state.user_id = athlete.get("id")
            st.query_params.clear()
            st.success("Login successful")
            # Pass auth data to the backend
            save_auth_data(token_data)
            # st.rerun()
        else:
            st.error("Failed to login, please try again")
    print("callback processed")
    st.rerun()

def save_auth_data(auth_response_data):
    try:
        response = requests.get(f"{BACKEND_URL}/authdata", json=auth_response_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        st.error(f"Unable to save auth data {e}")

async def exchange_code_for_token(code: str):
    """ Exchanges strava one time access code for an access token
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                STRAVA_TOKEN_URL,
                json={
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code"
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        st.error(f"Failed to fetch access token: {e}")
        return None
    #     print("Exchanging token")
    #     data={
    #         "client_id": CLIENT_ID,
    #         "client_secret": CLIENT_SECRET,
    #         "code": code,
    #         "grant_type": "authorization_code"
    #     }
    #     response = requests.post(STRAVA_TOKEN_URL, json=data)
    #     response.raise_for_status() # Raises an error if any
    #     return response.json()
    # except requests.exceptions.RequestException as e:
    #     st.error(f"Failed to fetch access token: {e}")
    #     return None


asyncio.run(main())