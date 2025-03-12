from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from app.database import db
from app.models.comment import CommentCreate, Comment
from app.services.auth import get_current_user
from datetime import datetime
from pymongo.errors import PyMongoError

async def create_comment(comment: CommentCreate, current_user=Depends(get_current_user)):
    try:
        # Check if the tweet exists
        tweet = db.tweets.find_one({"_id": ObjectId(comment.tweet_id)})
        print(f"Tweet: {tweet}")
        if not tweet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found")

        # Prepare the comment data to insert into the database
        comment_data = {
            "content": comment.content,
            "tweet_id": comment.tweet_id,
            "user_id": current_user.id,
            "created_at": datetime.utcnow()
        }
        # Insert the comment data into the 'comments' collection
        result = db.comments.insert_one(comment_data)
        comment_id = str(result.inserted_id)
        # Return the created comment as a response
        return Comment(id=comment_id, **comment_data)
    except PyMongoError as e:
        print(f"Database Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
         print(f"Unexpected Error: {str(e)}")
         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def read_comments():
    # Query to find all the comments
    comments = [{"id": str(comment["_id"]), **comment} for comment in db.comments.find().sort("created_at", -1).limit(50)]
    if not comments:
         raise HTTPException(status_code=404, detail="No comments found for this tweet ID")
    return comments

async def read_comments_by_tweet_id(tweet_id: str):
    # Query to find comments associated with the given tweet_id
    comments = [{"id": str(comment["_id"]), **comment} for comment in db.comments.find({"tweet_id": tweet_id}).sort("created_at", -1).limit(50)]
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for this tweet ID")
    return comments

# Modify an existing comment
async def modify_comment(comment_id: str, updated_content: str, current_user=Depends(get_current_user)):
    try:
        # Find the comment in the database
        comment = db.comments.find_one({"_id": ObjectId(comment_id)})

        # If comment does not exist
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

        # Ensure only the comment owner can modify it
        if str(comment["user_id"]) != str(current_user.id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to modify this comment")

        # Update only the content and add an updated_at timestamp
        db.comments.update_one(
            {"_id": ObjectId(comment_id)},
            {"$set": {"content": updated_content, "updated_at": datetime.utcnow()}}
        )

        return Comment(id=comment_id, **comment)

    except PyMongoError as e:
        print(f"Database Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Delete a comment
async def delete_comment(comment_id: str, current_user=Depends(get_current_user)):
    try:
        # Find the comment
        comment = db.comments.find_one({"_id": ObjectId(comment_id), "user_id": current_user.id})
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found or unauthorized")

        # Delete the comment
        db.comments.delete_one({"_id": ObjectId(comment_id)})

        return {"message": "Comment deleted successfully"}

    except PyMongoError as e:
        print(f"Database Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")