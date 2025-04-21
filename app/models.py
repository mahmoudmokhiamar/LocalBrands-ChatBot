from pydantic import BaseModel

class RecommendRequest(BaseModel):
    query: str

class RecommendResponse(BaseModel):
    result: str