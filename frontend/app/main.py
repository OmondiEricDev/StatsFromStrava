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

def main():
    st.title("K/QOM Tracker")
    print("starting")
    # Handle callback from Strava auth
    handle_callback()
    print("after callback")
    # Check if user is logged in
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
        st.user_id = None

    if st.session_state.access_token:
        st.success("You are logged in!!!")
        print("Logged in")
        show_profile()
    else:
        st.warning("Please log in to view your stats")
        print("not logged in!!!")
        if st.button("Log in with Strava"):
            auth_url = build_strava_auth_url()
            st.markdown(f"[Strav Login]({auth_url})", unsafe_allow_html=True)
            # st.write(f"Redirecting to [Strava Login]({auth_url})...")
            # st.rerun()

def handle_callback():
    query_params = st.experimental_get_query_params()
    print(f"Query params === {query_params}")
    if "code" in query_params:
        code = query_params["code"][0]
        token_data = exchange_code_for_token(code=code)        
        print("Got the code")
        print(token_data)
        if token_data:
            st.session_state.access_token = token_data.get("access_token")
            athlete = token_data.get("athlete")
            st.session_state.user_id = athlete.get("id")
            st.experimental_set_query_params() # Clears current data in query parameters
            st.success("Login successful")
            # Pass auth data to the backend
            save_auth_data(token_data)
            st.rerun()
        else:
            st.error("Failed to login, please try again")

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
        print("Exchanging token")
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

def show_profile():
    """
    Display users's Strava profile
    """
    user_profile = fetch_user_profile(st.session_state.user_id)
    display_profile(user_profile)

def show_starred_segments():
    "Display user's starred segments"
    starred_segments = fetch_starred_segments()
    display_starred_segments(starred_segments)

def auth_with_strava():
    try:
        response = requests.get(f"{BACKEND_URL}/login")
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to authenticate {e}")
        return None

def show_dashboard():
    """
    Display user activity data
    """
    st.header("Your Strava activities:")
    
    # Fetch activity data from the backend
    activities = fetch_activities()
    if activities:
        st.write(f"Found {len(activities)} activities")
        display_activities(activities)
    else:
        st.error("Failed to fetch activities")

def fetch_user_profile(user_id: int):
    """
    Fetch user's Strava profile
    """
    try:
        response = requests.get(f"{BACKEND_URL}/user/{user_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to get user profile: {e}")
        return None

def fetch_starred_segments():
    """Fetch users's starred segments"""
    try:
        response = requests.get(f"{BACKEND_URL}/segments")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch starred segments --> {e}")
        return None

def fetch_segment_data(segment_id: int):
    """Fetch segment data related to the given ID"""
    try:
        response = requests.get(f"{BACKEND_URL}/segment/{segment_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch segment with ID: {segment_id} --> {e}")
        return None

def fetch_activities():
    """
    Fetch Strava activiy data from the backend
    """
    try:
        response = requests.get(f"{BACKEND_URL}/user/activities")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch user activity data: {e}")
        return None

def display_starred_segments(starred_segments):
    st.header("Starred segments:")

def display_profile(profile):
    """
    Display user profile
    """
    st.header("Account details:")
    
    # Display profile picture
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(profile["profileMedium"], caption="Profile Picture", width=150)
    with col2:
        st.write(f"**Name:** {profile['firstName']} {profile['lastName']}")
        st.write(f"**Username:** {profile['username']}")
        st.write(f"**Location:** {profile['city']}, {profile['state']}, {profile['country']}")
        st.write(f"**Gender:** {profile['sex']}")
        st.write(f"**Member Since:** {profile['createdAt']}")
        st.write(f"**Last Updated:** {profile['updatedAt']}")
        st.write(f"**Bio:** {profile['bio'] if profile['bio'] else 'No bio available.'}")

def display_activities(activities):
    """
    Display activities in a table
    """
    st.subheader("Activity table")
    st.table(activities)
    
    # Activity distance bar chart
    st.subheader("Activity distances")
    activity_names = [act["name"] for act in activities]
    activity_distances = [act["distance"] for act in activities]
    st.bar_chart({"Distance (km)": activity_distances})
    
    # Activity duration line chart
    st.subheader("Activity durations")
    activity_durations = [act["elapsed_time"] for act in activities]
    st.line_chart({"Duration": activity_durations})


if __name__ == "__main__":
    main()
