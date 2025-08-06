import streamlit as st
import requests
import os
from datetime import datetime
from components.layout import show_sidebar
from components.theme import apply_theme

st.set_page_config(
    page_title="K/QOM Tracker",
    page_icon="🚴",
    layout="wide"
)

apply_theme()

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


def format_time(time_seconds: int):
    minutes = int(time_seconds) // 60
    seconds = minutes % 60
    return f"{minutes:02}:{seconds:02}"

def format_date(iso_date):
    formatted_date = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ")
    return formatted_date

def display_starred_segments(starred_segments):
    for segment in starred_segments:
        pr_date = format_date(segment.get("pr_date"))
        with st.container(border=True):
            st.subheader(segment.get("name"))
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Distance", f"{segment.get('distance')} m", border=True)
                st.metric("Climb Category",segment.get("climb_category"), border=True)
            with col2:
                st.metric("KOM Status", "✅" if segment.get("kom_status") else "❌", border=True)
                st.metric("PR Time", format_time(int(segment.get("pr_time"))), border=True)
            with col3:
                st.metric("PR Date", f"{pr_date.year}/{pr_date.month}/{pr_date.day}", border=True)
                st.metric("PR Activity", segment.get("pr_activity_id"), border=True)

def main():
    show_sidebar()
    
    # Check if user is logged in
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
        st.user_id = None
        # Redirect to login page if not authenticated
        st.switch_page("pages/login.py")
        return

    st.markdown(
    "<h1 style='text-align: center; font-style: italic;'>🏁 Starred Segments 🏁</h1>",
    unsafe_allow_html=True)

    col1, col2 = st.columns([0.9, 0.1])
    with col2:
        if st.button("🔄", help="Refresh segments data"):
            st.rerun()

    fetch_user_profile(st.session_state.user_id)
    fetch_starred_segments()
    
    if "starred_segments" in st.session_state:
        starred_segments = st.session_state.starred_segments
        if starred_segments:
            display_starred_segments(starred_segments)
        else:
            st.info("No starred segments found. Star some segments on Strava to see them here!")

def handle_callback():
    query_params = st.query_params.to_dict()
    if "code" in query_params:
        code = query_params.get("code")
        token_data = exchange_code_for_token(code=code)        
        if token_data:
            st.session_state.access_token = token_data.get("access_token")
            athlete = token_data.get("athlete")
            st.session_state.user_id = athlete.get("id")
            st.query_params.clear()
            st.success("Login successful")
            save_auth_data(token_data)
        else:
            st.error("Failed to login, please try again")
    st.rerun()

def save_auth_data(auth_response_data):
    try:
        response = requests.get(f"{BACKEND_URL}/authdata", json=auth_response_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error("Unable to save authentication data. Please try again later.")

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
        print(f"Token exchange error: {e}")
        st.error("Authentication failed. Please try again.")
        return None


def auth_with_strava():
    try:
        response = requests.get(f"{BACKEND_URL}/login")
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Authentication error: {e}")
        st.error("Authentication failed. Please try again.")
        return None

def fetch_user_profile(user_id: int):
    """
    Fetch user's Strava profile
    """
    with st.spinner('Loading profile...'):
        try:
            response = requests.get(f"{BACKEND_URL}/user/{user_id}")
            response.raise_for_status()
            profile_data = response.json()
            st.session_state.profile = profile_data
            return profile_data
        except requests.ConnectionError:
            st.error("Unable to connect to the server. Please check your internet connection.")
            return None
        except requests.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to get user profile: {e}")
            return None

def fetch_starred_segments():
    """Fetch users's starred segments"""
    with st.spinner('Loading segments...'):
        try:
            response = requests.get(f"{BACKEND_URL}/segments")
            response.raise_for_status()
            segments_data = response.json()
            st.session_state.starred_segments = segments_data
        except requests.ConnectionError:
            st.error("Unable to connect to the server. Please check your internet connection.")
        except requests.Timeout:
            st.error("Request timed out. Please try again.")
        except requests.RequestException as e:
            st.error(f"Failed to fetch starred segments: {e}")

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
