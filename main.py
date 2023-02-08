from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from peewee import *
from datetime import date
from pydantic import BaseModel



# from . import crud, models, schemas
# from typing import List
# from sqlalchemy.orm import Session
# from .database import SessionLocal, engine




DATABASE = 'teweepee1.db'

#create a peewee database instance our models will use thios database to persisit information
database = SqliteDatabase(DATABASE)

#model definitions -- the standard pattern is to define a base model class
# that specifies which database to use then any subclass will automatically use the correct stoeage for more information, see:

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_Date  = DateTimeField()

#Post table

class Post(BaseModel):
    user_info = ForeignKeyField(User, to_field='username')
    post_name = CharField()
    caption = CharField()

class Like_Table(BaseModel):
    user_info_like = ForeignKeyField(User, to_field='username')
    post_id = ForeignKeyField(Post, to_field='id')
    like_by_whom = CharField()
    like_count = IntegerField()


#Simply utility function to create tables
def create_tables():
    with database:
        database.create_tables([User,Post,Like_Table])

#allow running from the command line




# create_tables()

# user1 = User.create(username = 'Sanjuli',password ='1234',email = 'sanjuli@gmail.com',join_Date = date(2020,1,2))
# User.create(username = 'Vaibhav',password ='1234',email = 'Vaibhav@gmail.com',join_Date = '2023/01/30')
# User.create(username = 'Richa',password ='1234',email = 'richa@gmail.com',join_Date = '2023/01/30')
# User.create(username = 'Amartya',password ='1234',email = 'amartya@gmail.com',join_Date = '2023/01/30')
# User.create(username = 'Ritik',password ='1234',email = 'ritik@gmail.com',join_Date = '2023/01/30')

# Post.create(user_info = 'Sanjuli',post_name='firstPost',caption='hi')
# Post.create(user_info = 'Vaibhav',post_name ='secondPost', caption= 'hi again')

# Like_Table.create(user_info_like = 'Sanjuli', post_id = '2',like_by_whom = 'Vaibhav',like_count=0)


app = FastAPI()



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


@app.put("/dislike_post/{id}")
def like_post(id):
    qry = Like_Table.get(Like_Table.post_id == int(id))
    print(qry.like_count)
    qry.like_count = qry.like_count - 1
    qry.save()

    return {'msg': 'post disliked'}

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




