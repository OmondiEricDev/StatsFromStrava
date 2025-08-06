import streamlit as st

def show_sidebar():
    """Display the consistent sidebar elements across all pages"""
    with st.sidebar:
        if st.session_state.get("access_token"):
            if st.button("Logout"):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
