from peewee import *
from routes import database
class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_Date  = DateTimeField()

def get_users():
    return User.select()