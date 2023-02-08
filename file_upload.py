from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "contents":contents.decode()}

@app.get('/root')
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
