from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.services import segment as segments_service
from app.services import activity as activity_service

router = APIRouter()

# Background task to populate user activity data
async def populate_user_activity_data():
    print("populating user activity data...")
    _ = await activity_service.fetch_all_activities_strava()

@router.get("/segments")
async def get_starred_segments(background_tasks: BackgroundTasks):
    """Fetch all of the user's starred segments"""
    background_tasks.add_task(populate_user_activity_data)
    try:
        starred_segements = await segments_service.fetch_starred_segments()
        return starred_segements
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Segments API :: Unable to fetch starred segments -> {e}")


@router.get("/segment/{segment_id}")
async def get_segment_by_id(segment_id: int):
    """Fetch segment with the specified segment ID"""
    try:
        selected_segment = await segments_service.fetch_segment_by_id(segment_id)
        return selected_segment
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to fetch segment with ID {segment_id} -> {e}")