from fastapi import FastAPI
from peewee import *
from .user_controller import *
from .posts_controller import *

app = FastAPI()

DATABASE = 'teweepee2.db'

#create a peewee database instance our models will use thios database to persisit information
database = SqliteDatabase(DATABASE)



@app.get("/users")
def read_users():
    k=User.select()
    return [{"username": user.username, "Password": user.password, "Email": user.email, "Joining_Date": user.join_Date} for user in k]

@app.get("/single_user/{username}")
def get_current_user(username):
    query = User.get(User.username == str(username))
    return query

@app.get("/posts/")
def get_posts():
    posts = Post.select()
    return [{"user_id": post.user_info,"name_of_post": post.post_name ,"description": post.caption} for post in posts]

@app.get("/single_post/{username}")
def get_single_post(username):
    single_post = Post.get(Post.user_info == str(username))
    print(single_post)
    return single_post

@app.put("/like_post/{id}")
def like_post(id):
    qry = Like_Table.get(Like_Table.post_id == int(id))
    print(qry.like_count)
    qry.like_count = qry.like_count + 1
    qry.save()

    return {'msg': 'post liked'}


@app.put("/like_post/{id}")
def like_post(id):
    qry = Like_Table.get(Like_Table.post_id == int(id))
    print(qry.like_count)
    qry.like_count = qry.like_count - 1
    qry.save()

    return {'msg': 'post liked'}

@app.delete("/post/{post_id}")
def delete_post(post_id):
    post = Post.get(Post.id == post_id)
    post.delete_instance()
    return {"message": "Post deleted successfully"}

@app.get("/user_filter/")
async def search_user(username: str):
    users = User.select().where(User.username.contains(username))
    return [{"username": user.username, "email": user.email, "joining_date": user.join_Date} for user in users]
    
@app.get("/limited_posts/")
def search_posts(limit: int = None):
    query = Post.select()
    if limit:
        query = query.limit(limit)
    return [{"user_id": post.user_info,"name_of_post": post.post_name ,"description": post.caption} for post in query]
