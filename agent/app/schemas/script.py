from pydantic import BaseModel , Field 

class ScriptUpdate(BaseModel):
    """
        Schema for updating a podcast Script .
    """
    script: str = Field(..., description="The Full , updated Conversation Script ")