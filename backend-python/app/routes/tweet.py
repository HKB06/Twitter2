from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from app.database import db
from app.models.tweet import TweetCreate, Tweet
from app.services.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/tweets", response_model=Tweet)
async def create_tweet(tweet: TweetCreate, current_user=Depends(get_current_user)):

    tweet_data = {
        "user_id": current_user.id,
        "content": tweet.content,
        "media_url": tweet.media_url if tweet.media_url else None,
        "created_at": datetime.utcnow()
    }
    result = db.tweets.insert_one(tweet_data)
    return Tweet(id=str(result.inserted_id), **tweet_data)

@router.get("/tweets", response_model=List[Tweet])
async def read_tweets():
    tweets = [{"id": str(tweet["_id"]), **tweet} for tweet in db.tweets.find().sort("created_at", -1).limit(50)]
    return tweets
