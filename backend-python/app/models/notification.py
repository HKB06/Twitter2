from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Notification(BaseModel):
    id: str
    user_id: str
    from_user_id: str
    type: str  # 'like', 'retweet', 'comment', 'follow'
    tweet_id: Optional[str] = None
    is_read: bool
    created_at: datetime
