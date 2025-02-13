from fastapi import FastAPI

from . import users, activities

""" Add all application routers to the main FastAPI app instance
"""
def configure_routers(app: FastAPI) -> None:
    app.include_router(users.router)
    app.include_router(activities.router)