import streamlit as st
from datetime import datetime
st.markdown(
    "<h1 style='text-align: center;font-style: italic;'>🏁 Starred Segments 🏁</h1>",
    unsafe_allow_html=True
)

def main():
    starred_segments = st.session_state.starred_segments
    display_starred_segments(starred_segments)

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

main()
