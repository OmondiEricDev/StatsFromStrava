import streamlit as st

def apply_theme():
    """Apply consistent styling across all pages"""
    # Add custom CSS
    st.markdown(
        """
        <style>
        /* Main content styling */
        .stApp {
            background-color: #1c2b51;
        }
        
        /* Headers */
        h1 {
            color: #ffffff;
            font-family: 'Arial', sans-serif;
            margin-bottom: 2rem;
        }
        
        /* Metrics styling */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            color: #4CAF50;
        }
        
        /* Container styling */
        [data-testid="stExpander"] {
            background-color: #2d4263;
            border: none;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        /* Button styling */
        .stButton button {
            border-radius: 20px;
            padding: 2px 15px;
            border: none;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #152238;
        }
        
        [data-testid="stSidebar"] .stButton button {
            width: 100%;
            margin-top: 20px;
        }
        
        /* Metric containers */
        [data-testid="stMetric"] {
            background-color: #2d4263;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Container borders */
        [data-stale="false"] > div:has(> [data-testid="stVerticalBlock"]) > [data-testid="stVerticalBlock"] {
            background-color: #2d4263;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        /* Links */
        a {
            color: #4CAF50 !important;
            text-decoration: none;
        }
        
        a:hover {
            color: #45a049 !important;
            text-decoration: underline;
        }
        
        /* Warning/Info messages */
        .stAlert {
            background-color: #2d4263;
            border: 1px solid #4CAF50;
            color: white;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #2d4263;
            border-radius: 4px 4px 0px 0px;
            gap: 2px;
            padding: 10px 20px;
        }

        .stTabs [aria-selected="true"] {
            background-color: #4CAF50;
        }
        
        /* Tables */
        [data-testid="stTable"] {
            background-color: #2d4263;
        }
        
        /* Charts */
        .js-plotly-plot {
            background-color: #2d4263;
            border-radius: 8px;
            padding: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
