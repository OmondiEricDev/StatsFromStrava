import streamlit as st

st.markdown(
    "<h1 style='text-align: center; font-style: italic;'>👤 Profile </h1>",
    unsafe_allow_html=True
)

def main():
    profile = st.session_state.profile
    display_profile(profile)


def display_profile(profile):
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
        
main()