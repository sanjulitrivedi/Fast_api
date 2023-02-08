from fastapi import FastAPI, Request, Response, HTTPException, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
from hashlib import sha256
from jinja2 import Template
from fastapi.responses import RedirectResponse
import peewee
import uuid
import os



app = FastAPI()
templates = Jinja2Templates(directory="templates")

db = peewee.SqliteDatabase("authentication_data.db")


class User(peewee.Model):
    username = peewee.CharField(unique=True)
    password = peewee.CharField()

    class Meta:
        database = db


class Authentication(peewee.Model):
    user = peewee.ForeignKeyField(User, backref="authentications")
    token = peewee.CharField()

    class Meta:
        database = db


class Post(peewee.Model):
    user_info = peewee.ForeignKeyField(User, to_field='username')
    post_name = peewee.CharField()
    caption = peewee.CharField()

    class Meta:
        database = db


class Like_Table(peewee.Model):
    user_info_like = peewee.ForeignKeyField(User, to_field='username')
    post_id = peewee.ForeignKeyField(Post, to_field='id')
    like_by_whom = peewee.CharField()
    like_count = peewee.IntegerField()

    class Meta:
        database = db


class UserIn(BaseModel):
    username: str
    password: str
    confirm_password: str

    @validator('password')
    def password_validation(cls, v):
        if len(v) < 8:
            raise ValueError('Password should be at least 8 characters long')
        return v

    @validator('confirm_password')
    def confirm_password_validation(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


def create_tables():
    with db:
        db.create_tables([User, Authentication, Post, Like_Table])

# allow running from the command line


create_tables()


@app.get("/")
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/login")
async def login(request : Request):
    user_data = await request.form()
    user_data = {key: value for key, value in user_data.items()}
    user = User(**user_data)
    print(user)
    try:
        user = User.get(User.username == user.username)
        if user.password == user.password:
            token = str(uuid.uuid4())
            Authentication.create(user=user, token=token)
            # return {"message": "Login successful", "token": token}
        else:
            raise HTTPException(status_code=400, detail="Incorrect password")
    except User.DoesNotExist:
        raise HTTPException(status_code=400, detail="Username not found")
    
    response = RedirectResponse(url=f"/posts/{user.username}")
    response.status_code = 302
    return response

@app.get("/login")
async def render():
    with open("login.html", "r") as f:
        content = f.read()
    return HTMLResponse(content)


@app.post("/register_user")
async def register(request: Request):
    user_data = await request.form()
    user_data = {key: value for key, value in user_data.items()}
    user_in = UserIn(**user_data)
    try:
        new_user = User.create(username=user_in.username,
                               password=user_in.password)
    except peewee.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Username already registered")

    token = str(uuid.uuid4())
    Authentication.create(user=new_user, token=token)
    return {"message": "User registered", "token": token}


@app.post("/create_post")
async def create_post(request: Request):
    request_data = await request.json()
    token = request.headers.get("Authorization")
    post_name = request_data.get("post_name")
    caption = request_data.get("caption")

    try:
        authentication = Authentication.get(Authentication.token == token)
        user = authentication.user
    except Authentication.DoesNotExist:
        raise HTTPException(status_code=400, detail="Invalid Token")

    try:
        new_post = Post.create(
            user_info=user,
            post_name=post_name,
            caption=caption
        )
    except peewee.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Error creating post")

    return {"message": "Post created successfully"}

@app.get("/create_post")
async def render():
    with open("create_posts.html", "r") as f:
        content = f.read()
    return HTMLResponse(content)


@app.put("/like_post/{id}")
def like_post(id):
    try:
        qry = Like_Table.get(Like_Table.post_id == int(id))
    except Like_Table.DoesNotExist:
        return {"error": "Post not found"}

    qry.like_count = qry.like_count + 1
    print(qry.like_count)
    qry.save()
    return {"message": "Post liked"}

@app.get("/post/{post_id}/likes")
async def get_likes(post_id: int):
    try:
        post = Post.get(Post.id == post_id)
    except Post.DoesNotExist:
        raise HTTPException(status_code=400, detail="Post not found")
    
    likes = Like_Table.select().where(Like_Table.post_id == post.id)
    like_users = [{"username": like.like_by_whom} for like in likes]
    return {"likes": like_users}


@app.get("/posts/{username}")
async def get_user_posts(username: str):
    try:
        user = User.get(User.username == username)
    except User.DoesNotExist:
        raise HTTPException(status_code=400, detail="User not found")
    
    posts = Post.select().where(Post.user_info == user)
    posts_data = [{"post_name": post.post_name, "caption": post.caption} for post in posts]
    with open("posts.html") as file:
        template = Template(file.read())
    html_content = template.render(posts=posts_data)
    
    return HTMLResponse(content=html_content)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "contents":contents.decode()}

@app.get("/root")
async def render():
    with open("sign_up.html", "r") as f:
        content = f.read()
    return HTMLResponse(content)





@app.get("/data")
async def render():
    content = '''
    <!DOCTYPE html>
    <form action="/create_data" method="post">
        <input type="text" name="data" placeholder="Enter Data">
        <input type="hidden" name="Authorization" value="Token goes here">
        <button type="submit">Submit</button>
    </form>
    '''
    return HTMLResponse(content)



@app.get('/upload_file')
def render():
    content = '''
    <html>
    <head>
        <title> File Upload</title>
    </head>
    <body>
        <h1> Upload a file</h1>
        <form action="/uploadfile/" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    </body>
</html>
    '''

    return HTMLResponse(content)
