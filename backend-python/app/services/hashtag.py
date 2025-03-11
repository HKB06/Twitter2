from bson import ObjectId
from app.database import db
from app.models.hashtag import Hashtag, HashtagCreate


def create_or_get_hashtag(tag: str):
    """Créer un hashtag"""
    existing_hashtag = db.hashtags.find_one({"tag": tag})

    if existing_hashtag:
        return Hashtag(id=str(existing_hashtag["_id"]), tag=existing_hashtag["tag"])

    result = db.hashtags.insert_one({"tag": tag})

    return Hashtag(id=str(result.inserted_id), tag=tag)


def attach_hashtag_to_tweet(tweet_id: str, hashtag_id: str):
    """Associer un hashtag à un tweet"""
    db.tweet_hashtags.insert_one({
        "tweet_id": tweet_id,
        "hashtag_id": hashtag_id
    })
