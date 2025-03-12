from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    tweet_id: str
    content: str

class Comment(BaseModel):
    id: str
    tweet_id: str
    user_id: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None
