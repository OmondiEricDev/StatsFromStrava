import os
import sys
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# from app.utils.auth import get_access_token
from app.services import strava as strava_service

loaded = load_dotenv()
if not loaded:
    raise Exception("Failed to load environment variables from .env file")

# Initialize the FastMCP server
mcp = FastMCP("stats")

@mcp.tool()
async def get_starred_segments() -> str:
    """
    Fetch starred segments from Strava.
    example starred segment response from Strava:
    [
    {
        "id": "1613911",
        "name": "１９４ Climb",
        "distance": "1737.86",
        "climb_category": "1",
        "pr_time": "338",
        "pr_effort_id": "2956820098468437970",
        "pr_activity_id": "7085112943",
        "pr_date": "2022-05-04T00:27:03Z",
        "K/QOM": "False"
    },
    {
        "id": "1616012",
        "name": "Lenox Mt Road from Swamp",
        "distance": "2653.72",
        "climb_category": "0",
        "pr_time": "477",
        "pr_effort_id": "2860678613924330010",
        "pr_activity_id": "5777945599",
        "pr_date": "2021-08-11T22:04:44Z",
        "K/QOM": "False"
    }]
    """
    access_token = os.getenv("STRAVA_ACCESS_TOKEN")
    if not access_token:
        return "Unauthorized"

    try:
        starred_segments = await strava_service.get_starred_segments(access_token)

        if not starred_segments:
            return "No starred segments found."

        # Format the segments for display
        formatted_segments = []
        for segment in starred_segments:
            kqom_value = segment.get("K/QOM", "False")
            kqom_bool = str(kqom_value).lower() == "true"
            pr_date_full = segment.get('pr_date', 'N/A')
            pr_date = pr_date_full[:10] if pr_date_full != 'N/A' else 'N/A'
            segment_info = (
                f"Name: {segment.get('name')}\n"
                f"Distance: {segment.get('distance')} meters\n"
                f"Climb Category: {segment.get('climb_category')}\n"
                f"PR Time: {segment.get('pr_time', 'N/A')} seconds\n"
                f"PR Date: {pr_date}\n"
                f"KOM/QOM: {'Yes' if kqom_bool else 'No'}"
            )
            formatted_segments.append(segment_info)

        return "\n---\n".join(formatted_segments)
    except Exception as e:
        return f"Error fetching starred segments: {e}"
    
if __name__ == "__main__":
    # Run the FastMCP server
    print('...', file=sys.stderr)
    mcp.run(transport='stdio')