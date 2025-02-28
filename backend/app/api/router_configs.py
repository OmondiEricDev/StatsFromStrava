from fastapi import FastAPI

from . import users, activities, segments

""" Add all application routers to the main FastAPI app instance
"""
def configure_routers(app: FastAPI) -> None:
    app.include_router(users.router)
    app.include_router(activities.router)
    app.include_router(segments.router)