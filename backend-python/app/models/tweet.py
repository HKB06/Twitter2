from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TweetCreate(BaseModel):
    content: str
    media_url: Optional[str] = None

class Tweet(BaseModel):
    id: str
    user_id: str
    content: str
    media_url: Optional[str] = None
    created_at: datetime
