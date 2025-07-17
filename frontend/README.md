# StatsFromStrava - Frontend

## Overview

The frontend of StatsFromStrava is a **Streamlit-based web application** that provides an intuitive interface for cyclists to track their King/Queen of the Mountain (K/QOM) achievements on Strava segments. The application integrates seamlessly with the Strava API through OAuth2 authentication and displays comprehensive statistics about starred segments and personal records.

## Architecture & Design

### Framework Choice
The frontend is built using **Streamlit**, a Python-based framework that enables rapid development of data-driven web applications. This choice provides several advantages:
- **Rapid prototyping** and development
- **Built-in state management** through `st.session_state`
- **Native support for data visualization** components
- **Seamless integration** with Python data science libraries

### Application Structure

```
frontend/app/
├── main.py              # Main application entry point and authentication logic
├── components/          # Reusable UI components (planned)
│   ├── auth.py         # Authentication components (placeholder)
│   └── charts.py       # Chart components (placeholder)
├── pages/              # Multi-page application structure
│   ├── authcallback.py # OAuth callback handler
│   ├── home.py         # Home page
│   ├── profile.py      # User profile display
│   └── segments.py     # Starred segments dashboard
└── utils/              # Utility functions
    └── api.py          # API utilities (placeholder)
```

## Core Functionality

### 1. Authentication System

The application implements a **complete OAuth2 flow** with Strava:

- **Authorization URL Generation**: Constructs proper Strava OAuth URLs with required scopes
- **Token Exchange**: Handles the authorization code exchange for access tokens
- **Session Management**: Maintains user authentication state across page navigation
- **Backend Integration**: Securely passes authentication data to the backend API

**Key Features:**
- Scope-based permissions: `read_all,profile:read_all,activity:read,activity:read_all`
- Secure token handling with session state management
- Automatic redirection after successful authentication

### 2. Multi-Page Architecture

The application uses Streamlit's native multi-page functionality:

#### **Main Page (`main.py`)**
- Application entry point with centralized authentication logic
- Conditional rendering based on authentication status
- Integration with backend API for data fetching

#### **Profile Page (`profile.py`)**
- Displays comprehensive user profile information
- **Two-column layout** with profile image and user details
- Shows: Name, username, location, gender, membership date, and bio

#### **Segments Dashboard (`segments.py`)**
- **Primary feature** displaying starred Strava segments
- **Metric cards** showing segment statistics in a grid layout
- **Real-time KOM/QOM status** with visual indicators (✅/❌)
- **Time formatting** utilities for readable performance data

#### **Authentication Callback (`authcallback.py`)**
- Dedicated page for handling OAuth redirects
- **Asynchronous token exchange** using `httpx` for better performance
- Error handling and user feedback
- Automatic navigation to main application after successful auth

### 3. Data Integration

The frontend communicates with the backend through **RESTful API calls**:

```python
# Key API endpoints:
- GET /user/{user_id}        # User profile data
- GET /segments              # Starred segments
- GET /segment/{segment_id}  # Individual segment data
- GET /activities/{id}       # Activity details
- GET /authdata              # Authentication data storage
```

### 4. State Management

**Streamlit session state** is used for:
- `access_token`: User's Strava access token
- `user_id`: Authenticated user's ID
- `profile`: Cached user profile data
- `starred_segments`: Cached segment data



## Technical Implementation

### Dependencies
- **Streamlit**: Web framework and UI components
- **Requests/HTTPX**: HTTP client libraries for API communication
- **Python-dotenv**: Environment configuration management

### Configuration Management
The application uses **Streamlit secrets** for secure configuration:
- `BACKEND_URL`: Backend API endpoint
- `STRAVA_CLIENT_ID`: Strava application ID
- `STRAVA_CLIENT_SECRET`: Strava application secret
- `STRAVA_REDIRECT_URI`: OAuth callback URL

### Error Handling
Comprehensive error handling throughout:
- **HTTP exception handling** with user-friendly error messages
- **Authentication failure recovery** with retry mechanisms
- **Graceful degradation** when backend services are unavailable

## Data Flow

1. **User Authentication**: OAuth2 flow with Strava
2. **Token Management**: Secure storage and session handling
3. **Data Fetching**: Backend API calls for user data and segments
4. **State Caching**: Session-based caching for performance
5. **UI Rendering**: Dynamic component rendering based on data availability

## Future Enhancements

The architecture supports planned expansions:
- **Chart Components**: Plotly-based visualizations for performance trends
- **Authentication Components**: Modular auth UI components
- **API Utilities**: Enhanced API client with retry logic and caching
- **Enhanced Segment Analysis**: Detailed performance comparisons and trends

## Development Approach

The frontend demonstrates several software engineering best practices:
- **Separation of Concerns**: Clear division between authentication, data, and presentation logic
- **Modular Architecture**: Page-based organization for maintainability
- **Configuration Externalization**: Environment-based configuration management
- **Error Resilience**: Comprehensive error handling and user feedback
- **Performance Optimization**: Strategic caching and async operations

This architecture provides a solid foundation for a scalable, maintainable cycling performance tracking application that can grow with additional features and user requirements.