from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from app.database import db
from app.models import Tweet
from app.models.bookmark import Bookmark

def add_bookmark(user_id: str, tweet_id: str) -> Bookmark:
    """Ajoute un tweet aux favoris de l'utilisateur"""

    tweet = db.tweets.find_one({"_id": ObjectId(tweet_id)})
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    existing_bookmark = db.bookmarks.find_one({"user_id": user_id, "tweet_id": tweet_id})
    if existing_bookmark:
        raise HTTPException(status_code=400, detail="Tweet already bookmarked")

    bookmark_data = {
        "user_id": user_id,
        "tweet_id": tweet_id,
        "created_at": datetime.utcnow()
    }

    result = db.bookmarks.insert_one(bookmark_data)
    bookmark_data["id"] = str(result.inserted_id)

    return Bookmark(**bookmark_data)

def get_bookmarked_tweets(user_id: str):
    """
    Récupère tous les tweets enregistrés par un utilisateur.
    """
    bookmarks = db.bookmarks.find({"user_id": user_id})
    bookmarked_tweets = []

    for bookmark in bookmarks:
        tweet = db.tweets.find_one({"_id": ObjectId(bookmark["tweet_id"])})
        if tweet:
            tweet["id"] = str(tweet["_id"])
            del tweet["_id"]
            bookmarked_tweets.append(Tweet(**tweet))

    return bookmarked_tweets


def remove_bookmark(user_id: str, tweet_id: str):
    """Supprime un tweet des favoris de l'utilisateur"""

    result = db.bookmarks.delete_one({"user_id": user_id, "tweet_id": tweet_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    return {"message": "Bookmark removed successfully"}
