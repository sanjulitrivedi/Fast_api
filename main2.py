from routes import database
from .user_controller import User
from .posts_controller import Post,Like_Table
from .routes import app


def create_tables():
    with database:
        database.create_tables([User,Post,Like_Table])


create_tables()

User.create(username = 'Sanjuli',password ='1234',email = 'sanjuli@gmail.com',join_Date = date(2020,1,2))
User.create(username = 'Vaibhav',password ='1234',email = 'Vaibhav@gmail.com',join_Date = '2023/01/30')
User.create(username = 'Richa',password ='1234',email = 'richa@gmail.com',join_Date = '2023/01/30')
User.create(username = 'Amartya',password ='1234',email = 'amartya@gmail.com',join_Date = '2023/01/30')
User.create(username = 'Ritik',password ='1234',email = 'ritik@gmail.com',join_Date = '2023/01/30')

Post.create(user_info = 'Sanjuli',post_name='firstPost',caption='hi')
Post.create(user_info = 'Vaibhav',post_name ='secondPost', caption= 'hi again')

Like_Table.create(user_info_like = 'Sanjuli', post_id = '2',like_by_whom = 'Vaibhav',like_count=0)
