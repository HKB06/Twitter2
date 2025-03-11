from fastapi import APIRouter, Depends
from typing import List
from app.models.tweet import Tweet, TweetCreate
from app.services.tweet import create_tweet, get_tweets_by_hashtags, get_all_tweets, delete_all_tweets, \
    get_tweets_by_hashtags
from app.services.auth import get_current_user

router = APIRouter()


@router.post("/tweets", response_model=Tweet)
async def post_tweet(tweet: TweetCreate, current_user=Depends(get_current_user)):
    return await create_tweet(tweet, current_user)


@router.get("/tweets/hashtags/{tags}", response_model=List[Tweet])
async def get_tweets(tags: str):
    """Recherche de tweets contenant un ou plusieurs hashtags"""
    hashtags = tags.split(",")
    return await get_tweets_by_hashtags(hashtags)


@router.get("/tweets", response_model=List[Tweet])
async def get_tweets():
    return await get_all_tweets()

'''
@router.delete("/tweets/delete-all")
async def delete_all():
    return await delete_all_tweets()
'''