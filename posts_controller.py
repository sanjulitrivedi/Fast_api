from fastapi import FastAPI
from peewee import *
from routes import database
from .user_controller import User


class BaseModel(Model):
    class Meta:
        database = database

class Post(BaseModel):
    user_info = ForeignKeyField(User, to_field='username')
    post_name = CharField()
    caption = CharField()

class Like_Table(BaseModel):
    user_info_like = ForeignKeyField(User, to_field='username')
    post_id = ForeignKeyField(Post, to_field='id')
    like_by_whom = CharField()
    like_count = IntegerField()
