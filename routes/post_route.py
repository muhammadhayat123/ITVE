from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from validations.post_validation import CreatePost
from config.db import users_collection, posts_collection
from bson import ObjectId

post_route = APIRouter()

@post_route.post("/create-post", status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost, user_email: str):
    """
    Client sends content & image + their email (from session/local storage)
    Backend fetches user info from DB and attaches username/profile_image.
    """

    user = users_collection.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_post = {
        "user_id": str(user["_id"]),
        "username": user.get("username"),
        "profile_image": user.get("profile_image", None),
        "content": post.content,
        "image": post.image,
        "likes": 0,
        "comments": 0,
        "shares": 0,
        "views": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = posts_collection.insert_one(new_post)

    return {
        "status": "success",
        "message": "Post created successfully",
        "data": {
            "post_id": str(result.inserted_id),
            "username": new_post["username"],
            "profile_image": new_post["profile_image"],
            "content": new_post["content"],
            "image": new_post["image"]
        }
    }



@post_route.post("/comment-post/{post_id}")
def comment_post(post_id: str, user_email: str, comment_text: str):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = {
        "user_email": user_email,
        "comment": comment_text,
        "created_at": datetime.utcnow()
    }

    posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$push": {"comments_list": new_comment}, "$inc": {"comments": 1}}
    )

    return {"status": "success", "total_comments": post.get("comments", 0) + 1}



@post_route.get("/get-posts")
def get_posts():
    posts = []

    for post in posts_collection.find().sort("created_at", -1):
        post["_id"] = str(post["_id"])
        posts.append(post)

    return {
        "status": "success",
        "data": posts
    }




@post_route.get("/get-post/{post_id}")
def get_single_post(post_id: str):

    post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post["_id"] = str(post["_id"])

    return {
        "status": "success",
        "data": post
    }


@post_route.put("/update-post/{post_id}")
def update_post(post_id: str, post: CreatePost):

    existing_post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_data = {
        "content": post.content,
        "image": post.image,
        "updated_at": datetime.utcnow()
    }

    posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": updated_data}
    )

    return {
        "status": "success",
        "message": "Post updated successfully"
    }




@post_route.delete("/delete-post/{post_id}")
def delete_post(post_id: str):

    post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    posts_collection.delete_one({"_id": ObjectId(post_id)})

    return {
        "status": "success",
        "message": "Post deleted successfully"
    }