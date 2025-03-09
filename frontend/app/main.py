import streamlit as st
import requests
import os
from dotenv import load_dotenv

loaded = load_dotenv()

# Application's backend URL
BACKEND_URL = st.secrets["BACKEND_URL"]
CLIENT_ID = st.secrets["STRAVA_CLIENT_ID"]
CLIENT_SECRET = st.secrets["STRAVA_CLIENT_SECRET"]
REDIRECT_URI = st.secrets["STRAVA_REDIRECT_URI"]

# Strava OAuth URLs
STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
APPROVAL_PROMPT = "auto"
AUTH_SCOPE = "read_all,profile:read_all,activity:read,activity:read_all"



# pages = {
#     "🏠 Hone": "main.py",
#     "👤 Profile": "profile.py",
#     "🏁 Segments": "segments.py"
# }

# st.sidebar.title("Navigation")

# for page_name, page_file in pages.items():
#     if st.sidebar.button(page_name):
#         st.switch_page(page=page_file)

def main():
    st.markdown(
    "<h1 style='text-align: center; font-style: italic;'>🚴 K/QOM Tracker! 👑</h1>",
    unsafe_allow_html=True)

    main_page = st.Page("main.py", title="Home", icon="🏠", default=True)
    profile_page = st.Page("pages/profile.py", title="Profile", icon="👤")
    segments_page = st.Page("pages/segments.py", title="Segments", icon="🏁")
    authcallback_page = st.Page("pages/authcallback.py")

    pg = st.navigation([main_page, profile_page, segments_page, authcallback_page])
    pg.run()
    # Handle callback from Strava auth
    # if st.query_params:
    #     handle_callback()
    
    # Check if user is logged in
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
        st.user_id = None

    if st.session_state.access_token:
        # st.success("You are logged in!!!")
        # st.page_link("main.py", label="Home", icon="🏠", use_container_width=True)
        # st.page_link("pages/profile.py", label="Profile", icon="👤", use_container_width=True)
        # st.page_link("pages/segments.py", label="Segments", icon="🏁", use_container_width=True)
        fetch_user_profile(st.session_state.user_id)
        fetch_starred_segments()
    else:
        st.warning("Please log in to view your stats")
        if st.button("Log in with Strava"):
            
            auth_url = build_strava_auth_url()
            st.markdown(f"[Strav Login]({auth_url})", unsafe_allow_html=True)

def handle_callback():
    query_params = st.query_params.to_dict()
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

def build_strava_auth_url() -> str:
    """Build and return the auth URL
    """
    return (
        f"{STRAVA_AUTH_URL}?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"approval_prompt={APPROVAL_PROMPT}&"
        f"scope={AUTH_SCOPE}"
    )

def exchange_code_for_token(code: str):
    """ Exchanges strava one time access code for an access token
    """
    try:
        # print("Exchanging token")
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code"
        }
        response = requests.post(STRAVA_TOKEN_URL, data)
        response.raise_for_status() # Raises an error if any
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch access token: {e}")
        return None


def auth_with_strava():
    try:
        response = requests.get(f"{BACKEND_URL}/login")
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to authenticate {e}")
        return None

def fetch_user_profile(user_id: int):
    """
    Fetch user's Strava profile
    """
    try:
        response = requests.get(f"{BACKEND_URL}/user/{user_id}")
        response.raise_for_status()
        st.session_state.profile = response.json()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to get user profile: {e}")
        return None

def fetch_starred_segments():
    """Fetch users's starred segments"""
    try:
        response = requests.get(f"{BACKEND_URL}/segments")
        response.raise_for_status()
        st.session_state.starred_segments = response.json()
        # return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch starred segments --> {e}")

def fetch_segment_data(segment_id: int):
    """Fetch segment data related to the given ID"""
    try:
        response = requests.get(f"{BACKEND_URL}/segment/{segment_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch segment with ID: {segment_id} --> {e}")
        return None

def fetch_activity_by_id(activity_id: int):
    """
    Fetch Strava activity data from the backend
    """
    try:
        response = requests.get(f"{BACKEND_URL}/activities/{activity_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch activity {activity_id} -->: {e}")
        return None

if __name__ == "__main__":
    main()
