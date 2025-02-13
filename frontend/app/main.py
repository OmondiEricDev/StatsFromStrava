import streamlit as st
import requests
import os
from dotenv import load_dotenv

loaded = load_dotenv()

# Application's backend URL
BACKEND_URL = "http://localhost:8000"

APP_AUTH_URL = f"{BACKEND_URL}/auth/login"

def main():
    st.title("Fitness Analytics Dashboard")
    
    # Check if user is logged in
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    
    if st.session_state.access_token:
        st.success("You are logged in to!!!")
        
        user_profile = fetch_user_profile(13974060) # TODO: find a better way for this
        if user_profile:
            display_profile(user_profile)
        else:
            st.error("Failed to fetch user profile!!")
        
        # show_dashboard()
    else:
        st.warning("Please log in to view your stats")
        if st.button("Log in with Strava"):
            st.write(f"Redirecting to Strava login page:{APP_AUTH_URL}...")
            user_profile = fetch_user_profile(13974060) # TODO: find a better way for this
            if user_profile:
                display_profile(user_profile)
            else:
                st.error("Failed to fetch user profile!!")
            # main()
            # st.rerun()


def show_profile():
    """
    Display users's Strava profile
    """
    st.header("Your Strava profile:")
    
    # Fetch user profile from the backend
    


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





