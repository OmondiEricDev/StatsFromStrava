# K/QOM Hunter Backend

## Overview

The K/QOM Hunter backend is a **FastAPI-based REST API** that serves as the data layer for a Strava analytics application. It provides a comprehensive interface for users to authenticate with Strava, fetch their athletic data, and perform statistical analysis on their activities and segments. The backend acts as a middleware between the frontend application and the Strava API, offering caching, data persistence, and enhanced functionality.

## Core Objectives

1. **Strava Integration**: Seamless OAuth 2.0 authentication and data synchronization with the Strava API
2. **Performance Optimization**: Intelligent caching using Redis to reduce API calls and improve response times
3. **Data Aggregation**: Centralized access to user activities, segments, and athlete information
4. **Scalable Architecture**: Modular design supporting future feature expansion and microservices migration
5. **Developer Experience**: Clean API design with comprehensive error handling and structured responses

## Architecture & Design

### Technology Stack

- **Framework**: FastAPI (Python 3.9+)
- **Caching Layer**: Redis for session management and data caching
- **HTTP Client**: Requests library for Strava API communication
- **Configuration**: Python-dotenv for environment variable management
- **Package Management**: Poetry/UV for dependency management

### Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── api/                    # API route definitions
│   │   ├── router_configs.py   # Router configuration and registration
│   │   ├── users.py           # User-related endpoints
│   │   ├── activities.py      # Activity data endpoints
│   │   └── segments.py        # Segment data endpoints
│   ├── services/              # Business logic layer
│   │   ├── strava.py          # Strava API integration
│   │   ├── redis.py           # Redis operations and caching
│   │   ├── activity.py        # Activity data processing
│   │   └── segment.py         # Segment data processing
│   ├── utils/                 # Utility functions
│   │   ├── auth.py            # Authentication and token management
│   │   └── cache.py           # Caching utilities
│   └── models/                # Data models and schemas
│       ├── activitiy.py       # Activity data models (Pydantic)
│       └── user.py            # User data models
```

### Architectural Patterns

#### 1. **Layered Architecture**

- **API Layer**: FastAPI routers handling HTTP requests/responses
- **Service Layer**: Business logic and external API integration
- **Data Layer**: Redis caching and data persistence
- **Utility Layer**: Cross-cutting concerns (auth, caching, validation)

#### 2. **Repository Pattern**

- Redis service acts as a repository for user data, activities, and segments
- Abstraction layer between business logic and data storage
- Consistent interface for data operations across the application

#### 3. **OAuth 2.0 Implementation**

- Complete Strava OAuth flow with authorization code exchange
- Automatic token refresh mechanism
- Secure token storage with TTL management

## Core Features & Implementation

### 1. Authentication System

#### OAuth 2.0 Flow

```python
# Authorization URL generation
GET /auth/login -> Redirects to Strava authorization
GET /auth/callback -> Handles authorization code exchange
```

**Key Components:**

- **Token Management**: Automatic access token refresh using refresh tokens
- **Session Persistence**: Redis-based user session storage with expiration
- **Security**: Secure token storage with TTL-based expiration (expires_in - 60 seconds)

**Implementation Highlights:**

```python
# Token storage with automatic expiration
reddis_client.hset(f"userAuth:{athlete_id}", mapping={
    "access_token": access_token,
    "refresh_token": refresh_token,
    "expires_at": expires_at,
    "expires_in": expires_in,
})
ttl = expires_in - 60
reddis_client.hexpire(f"userAuth:{athlete_id}", ttl, "access_token")
```

### 2. Activity Management

#### Data Flow

1. **API Request**: Client requests activity data
2. **Cache Check**: Redis lookup for existing data
3. **API Fallback**: Strava API call if cache miss
4. **Data Processing**: Normalize and structure response data
5. **Cache Storage**: Store processed data with TTL
6. **Response**: Return formatted data to client

**Endpoints:**

- `GET /activities` - Fetch all user activities
- `GET /activities/{activity_id}` - Get specific activity details

**Caching Strategy:**

- Activity data cached in Redis hash sets
- Activity IDs maintained in Redis sets for efficient querying
- Configurable TTL for cache invalidation

### 3. Segment Analytics

#### Features

- **Starred Segments**: Fetch user's starred Strava segments
- **Performance Tracking**: PR times, KOM/QOM status, effort analysis
- **Detailed Metrics**: Distance, climb category, and performance comparisons

**Data Structure:**

```python
segment_data = {
    "id": segment_id,
    "name": segment_name,
    "distance": distance_meters,
    "climb_category": category,
    "pr_time": personal_record_time,
    "pr_effort_id": effort_id,
    "pr_activity_id": activity_id,
    "pr_date": effort_date,
    "K/QOM": is_king_queen_of_mountain
}
```

### 4. User Profile Management

#### Profile Data

- **Athlete Information**: Name, bio, location, profile images
- **Account Details**: Creation date, update history
- **Preferences**: User-specific settings and configurations

**Redis Schema:**

```
userProfile:{athlete_id} -> Hash containing profile data
userAuth:{athlete_id} -> Hash containing authentication tokens
```

## Data Management & Caching

### Redis Implementation

#### Key Patterns

- **Hash Sets**: Structured data storage for users, activities, segments
- **Sets**: Collection management for activity and segment IDs
- **TTL Management**: Automatic expiration for cache invalidation
- **Atomic Operations**: Consistent data updates across related keys

#### Cache Strategy

1. **Cache-First**: Always check Redis before external API calls
2. **Write-Through**: Update cache immediately after Strava API responses
3. **TTL-Based Expiration**: Automatic cache invalidation (configurable per data type)
4. **Lazy Loading**: Fetch from Strava API only when cache misses occur

### Data Persistence Patterns

```python
# Example: Activity caching with automatic expiration
async def save_activity(activity_item):
    activity_hash_key = f"activity:{activity_item.get('id')}"
    activity_data = {
        "id": activity_item.get("id"),
        "name": activity_item.get("name"),
        "distance": activity_item.get("distance"),
        "avg_speed": activity_item.get("average_speed"),
        "avg_power": activity_item.get("average_watts"),
        "kudos_count": activity_item.get("kudos_count")
    }
    
    redis_service.create_hash_set(
        name_key=activity_hash_key,
        data=activity_data,
        ttl=3600  # 1 hour cache
    )
```

## API Design & Error Handling

### RESTful Endpoints

#### User Management

- `GET /user/{user_id}` - User profile information
- `GET /athlete/{user_id}` - Live athlete data from Strava

#### Activity Operations

- `GET /activities` - All user activities (paginated)
- `GET /activities/{activity_id}` - Specific activity details

#### Segment Operations

- `GET /segments` - User's starred segments
- `GET /segment/{segment_id}` - Specific segment data

### Error Handling Strategy

1. **HTTP Status Codes**: Proper use of 4xx and 5xx status codes
2. **Detailed Error Messages**: Structured error responses with context
3. **Graceful Degradation**: Fallback mechanisms for service failures
4. **Logging**: Comprehensive error logging for debugging

```python
# Example error handling pattern
try:
    activity_data = await activity_service.fetch_activity_by_id(activity_id)
    return activity_data
except Exception as e:
    raise HTTPException(
        status_code=500, 
        detail=f"Failed to get activity with id: {activity_id} -> {e}"
    )
```

## Security Considerations

### Token Security

- **Secure Storage**: Redis with proper access controls
- **Token Rotation**: Automatic refresh token mechanism
- **Expiration Management**: Proactive token refresh before expiration
- **Environment Variables**: Sensitive data stored in environment configuration

### API Security

- **Input Validation**: Parameter validation on all endpoints
- **Rate Limiting**: (Recommended for production) Request throttling
- **CORS Configuration**: (Future implementation) Cross-origin request handling

## Performance Optimizations

### Caching Benefits

1. **Reduced API Calls**: Minimize Strava API rate limit impact
2. **Faster Response Times**: Local Redis queries vs external HTTP calls
3. **Offline Capabilities**: Serve cached data during API downtime
4. **Bandwidth Efficiency**: Reduce external data transfer

### Future Optimizations

- **Connection Pooling**: Redis and HTTP connection reuse
- **Background Tasks**: Async data synchronization
- **Data Compression**: Optimize Redis memory usage
- **Batch Operations**: Bulk data processing capabilities

## Development & Deployment

### Environment Configuration

```bash
# Required environment variables
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
STRAVA_REDIRECT_URI=http://localhost:8000/auth/callback
REDIS_ADDRESS=localhost
REDIS_PORT=6379
USER_ID=your_user_id  # TODO: Dynamic user management
```

### Running the Application

```bash
# Install dependencies
poetry install

# Start Redis server
redis-server

# Run FastAPI application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run test suite
pytest tests/

# Coverage report
pytest --cov=app tests/
```

## Future Enhancements

### Planned Features

1. **Multi-User Support**: Dynamic user management and session handling
2. **Database Integration**: PostgreSQL for persistent data storage
3. **Real-time Analytics**: WebSocket support for live data updates
4. **Advanced Caching**: Redis clustering and advanced cache strategies
5. **Microservices Architecture**: Service decomposition for scalability
6. **API Documentation**: Automated OpenAPI/Swagger documentation
7. **Monitoring & Metrics**: Application performance monitoring
8. **Background Jobs**: Celery integration for async task processing

### Technical Debt

1. **Hard-coded User ID**: Implement dynamic user identification
2. **Error Handling**: Enhanced exception handling and logging
3. **Data Models**: Complete Pydantic model definitions
4. **Testing Coverage**: Comprehensive unit and integration tests
5. **Configuration Management**: Centralized settings management
6. **Security Hardening**: Enhanced authentication and authorization

## API Documentation

The backend provides a RESTful API with the following key endpoints:

### Authentication Endpoints

- `GET /` - Health check endpoint
- `GET /login` - Get Strava authorization URL
- `GET /auth/login` - Redirect to Strava authorization
- `GET /auth/callback` - Handle OAuth callback from Strava

### Data Endpoints

- `GET /user/{user_id}` - Get user profile from cache
- `GET /athlete/{user_id}` - Get live athlete data from Strava
- `GET /activities` - Get all user activities
- `GET /activities/{activity_id}` - Get specific activity
- `GET /segments` - Get starred segments
- `GET /segment/{segment_id}` - Get specific segment

This backend serves as a robust foundation for a Strava analytics application, providing efficient data management, secure authentication, and scalable architecture for future enhancements.
