import streamlit as st
from components.layout import show_sidebar
from components.theme import apply_theme

st.set_page_config(
    page_title="Profile - K/QOM Tracker",
    page_icon="👤",
    layout="wide"
)

apply_theme()
show_sidebar()

st.markdown(
    "<h1 style='text-align: center; font-style: italic;'>👤 Profile </h1>",
    unsafe_allow_html=True
)

def main():
    profile = st.session_state.profile
    display_profile(profile)


def display_profile(profile):
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(profile["profileMedium"], caption="Profile Picture", width=150)
        with col2:
            # Profile details
            st.markdown(
                """
                <div style='background-color: #2d4263; padding: 20px; border-radius: 8px;'>
                """,
                unsafe_allow_html=True
            )
            st.write(f"#### {profile['firstName']} {profile['lastName']}")
            st.write(f"**@{profile['username']}**")
            st.markdown("---")
            
            # Location
            st.write(f"📍 **Location:** {profile['city']}, {profile['state']}, {profile['country']}")
            
            # Other details with icons
            st.write(f"👤 **Gender:** {profile['sex']}")
            st.write(f"📅 **Member Since:** {profile['createdAt']}")
            st.write(f"🔄 **Last Updated:** {profile['updatedAt']}")
            
            # Bio
            st.markdown("---")
            st.write("📝 **Bio:**")
            st.write(f"_{profile['bio'] if profile['bio'] else 'No bio available.'}_")
        
main()