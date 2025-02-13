from pydantic import BaseModel


"""Defines the Activity model structure
"""

class Activity(BaseModel):
    pass


class Config:
    json_schema_extra = {
        "example": {
            
        }
    }