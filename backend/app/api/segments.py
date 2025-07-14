from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.services import segment as segments_service

router = APIRouter()

@router.get("/segments")
async def get_starred_segments():
    """Fetch all of the user's starred segments"""
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