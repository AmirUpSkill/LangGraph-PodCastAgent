from pydantic import BaseModel , Field 

class AudioGenerationResponse(BaseModel):
    """
        Schema for the response after triggering audio generation .
    """
    podcast_id: str
    status: str = Field(..., description="The current status of the audio generation job.")
    message: str