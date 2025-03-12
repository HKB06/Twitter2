from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from app.database import db
from app.models.comment import CommentCreate, Comment
from app.services.auth import get_current_user
from app.services.comment import create_comment, read_comments, read_comments_by_tweet_id, modify_comment, delete_comment
from datetime import datetime
from pymongo.errors import PyMongoError

router = APIRouter()

# create comment
@router.post("/comments", response_model=Comment)
async def post_comment(comment: CommentCreate, current_user=Depends(get_current_user)):
    return await create_comment(comment, current_user)


# read comments
@router.get("/comments", response_model=List[Comment])
async def get_comments():
    return await read_comments()


# read comments by tweet id
@router.get("/comments/{tweet_id}", response_model=List[Comment])
async def get_comments_by_tweet_id(tweet_id: str):
    return await read_comments_by_tweet_id(tweet_id)

# Modify a comment
@router.put("/comments/{comment_id}", response_model=Comment)
async def update_comment(comment_id: str, comment: CommentCreate, current_user=Depends(get_current_user)):
    updated_content = comment.content
    return await modify_comment(comment_id, updated_content, current_user)

# Delete a comment
@router.delete("/comments/{comment_id}")
async def remove_comment(comment_id: str, current_user=Depends(get_current_user)):
    return await delete_comment(comment_id, current_user)