from datetime import datetime
from typing import List

from fastapi import Depends
from bson import ObjectId
from app.database import db
from app.models.tweet import Tweet, TweetCreate
from app.services.auth import get_current_user
from app.services.hashtag import create_or_get_hashtag, attach_hashtag_to_tweet


async def create_tweet(tweet: TweetCreate, current_user=Depends(get_current_user)):
    """Créer un tweet et y associer des hashtags"""

    tweet_data = {
        "user_id": current_user.id,
        "content": tweet.content,
        "media_url": tweet.media_url if tweet.media_url else None,
        "created_at": datetime.utcnow()
    }

    result = db.tweets.insert_one(tweet_data)
    tweet_id = str(result.inserted_id)

    hashtags = [tag.strip("#") for tag in tweet.content.split() if tag.startswith("#")]

    for tag in hashtags:
        hashtag = create_or_get_hashtag(tag)
        attach_hashtag_to_tweet(tweet_id, hashtag.id)

    return Tweet(id=tweet_id, **tweet_data)


from app.database import db
from app.models.tweet import Tweet
from bson import ObjectId
from typing import List

from app.database import db
from app.models.tweet import Tweet
from bson import ObjectId
from typing import List


async def get_tweets_by_hashtags(hashtags: List[str]):
    """Récupère les tweets contenant *tous* les hashtags demandés, peu importe s'il y en a d'autres"""

    regex_patterns = [{"content": {"$regex": f"#{tag}", "$options": "i"}} for tag in hashtags]

    tweets_cursor = db.tweets.find({
        "$and": regex_patterns
    }).sort("created_at", -1)

    tweets = []
    for tweet in tweets_cursor:
        tweet["id"] = str(tweet["_id"])
        del tweet["_id"]
        tweets.append(Tweet(**tweet))

    return tweets


async def get_all_tweets(limit: int = 50):
    """Récupérer tous les tweets les plus récents"""
    tweets = []
    for tweet in db.tweets.find().sort("created_at", -1).limit(limit):
        tweet["id"] = str(tweet["_id"])
        del tweet["_id"]
        if "user_id" not in tweet:
            print(f"⚠️ Tweet sans user_id détecté : {tweet}")  #pain
            continue

        tweets.append(Tweet(**tweet))

    return tweets



# elle existe juste au cas ou
async def delete_all_tweets():
    """Supprime tous les tweets de la base de données"""
    result = db.tweets.delete_many({})
    print(f"🗑️ {result.deleted_count} tweets supprimés.")
    return {"deleted_tweets": result.deleted_count}




