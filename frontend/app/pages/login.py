import asyncio
import httpx
import streamlit as st
import requests
from components.layout import show_sidebar
from components.theme import apply_theme

# Configure the page
st.set_page_config(
    page_title="Login - K/QOM Tracker",
    page_icon="🚴",
    layout="wide"
)

# Apply consistent theme
apply_theme()

# Show sidebar (without logout since we're on login page)
show_sidebar()

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
    # If user is already logged in, redirect to main page
    if st.session_state.get("access_token"):
        st.switch_page("main.py")
        
    # Show login interface
    st.markdown(
        "<h1 style='text-align: center; font-style: italic;'>🚴 K/QOM Hunter! 👑</h1>",
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div style='text-align: center;'>
            <p>Connect with Strava to track your segments and achievements!</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Center the login button using columns
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Login with Strava", type="primary", use_container_width=True):
            auth_url = (
                f"{STRAVA_AUTH_URL}?"
                f"client_id={CLIENT_ID}&"
                f"redirect_uri={REDIRECT_URI}&"
                f"response_type=code&"
                f"approval_prompt={APPROVAL_PROMPT}&"
                f"scope={AUTH_SCOPE}"
            )
            st.markdown(f"[Connecting to Strava...]({auth_url})")
    
    # Handle callback if we have code parameter
    if "code" in st.query_params:
        code = st.query_params.get("code")
        
        async with httpx.AsyncClient() as client:
            try:
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
                token_data = response.json()
                
                # Save token data to session state
                st.session_state.access_token = token_data.get("access_token")
                athlete = token_data.get("athlete")
                st.session_state.user_id = athlete.get("id")
                
                # Save auth data to backend
                save_auth_data(token_data)
                
                # Clear query parameters and redirect to main page
                st.query_params.clear()
                st.switch_page("main.py")
                
            except httpx.HTTPStatusError as e:
                st.error(f"Failed to authenticate with Strava: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

def save_auth_data(auth_response_data):
    try:
        response = requests.get(f"{BACKEND_URL}/authdata", json=auth_response_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to save authentication data: {str(e)}")

asyncio.run(main())
