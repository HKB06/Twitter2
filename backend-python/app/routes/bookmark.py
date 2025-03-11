from typing import List

from fastapi import APIRouter, Depends

from app.models import Tweet
from app.services.bookmark import add_bookmark, get_bookmarked_tweets, remove_bookmark
from app.models.bookmark import Bookmark, BookmarkCreate
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/bookmarks", response_model=Bookmark)
async def add_bookmark_route(bookmark: BookmarkCreate, current_user: User = Depends(get_current_user)):
    return add_bookmark(current_user.id, bookmark.tweet_id)

@router.get("/bookmarks", response_model=List[Tweet])
async def get_bookmarks_route(current_user: User = Depends(get_current_user)):
    return get_bookmarked_tweets(current_user.id)

@router.delete("/bookmarks/{tweet_id}")
async def remove_bookmark_route(tweet_id: str, current_user: User = Depends(get_current_user)):
    return remove_bookmark(current_user.id, tweet_id)
