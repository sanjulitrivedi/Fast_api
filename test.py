from peewee import *
from datetime import date
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
    user_info = ForeignKeyField(User, backref='Post')
    post_name = CharField()
    caption = CharField()

#Simply utility function to create tables
def create_tables():
    with database:
        database.create_tables([User,Post])

#allow running from the command line



if __name__ == '__main__':
    create_tables()

user1 = User.create(username = 'Sanjuli',password ='1234',email = 'sanjuli@gmail.com',join_Date = date(2020,1,2))
user2 = User.create(username = 'Vaibhav',password ='1234',email = 'Vaibhav@gmail.com',join_Date = '2023/01/30')
user3 = User.create(username = 'Richa',password ='1234',email = 'richa@gmail.com',join_Date = '2023/01/30')
user4 = User.create(username = 'Amartya',password ='1234',email = 'amartya@gmail.com',join_Date = '2023/01/30')
user5 = User.create(username = 'Ritik',password ='1234',email = 'ritik@gmail.com',join_Date = '2023/01/30')

Post.create(user_info = user1,post_name='firstPost',caption='hi')
Post.create(user_info = user1,post_name ='secondPost', caption= 'hi again')

for Post in Post.select().join(User).where(User.username == 'Sanjuli'):
    print(Post.caption)


