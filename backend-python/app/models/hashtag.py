from pydantic import BaseModel
from datetime import datetime
from typing import List

class HashtagCreate(BaseModel):
    tag: str

class Hashtag(BaseModel):
    id: str
    tag: str

class TweetHashtag(BaseModel):
    id: str
    tweet_id: str
    hashtag_id: str
