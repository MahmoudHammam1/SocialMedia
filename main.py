from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pydantic import BaseModel
from social_media.core import FacebookPostManager


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ACCESS_TOKEN = "facebook_page_access_token"
AD_ACCOUNT_ID = "act_ + ad_account_id"
PAGE_ID = "page_id"
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload_photo")
async def upload_photo(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save the file locally
    # Later upload to Firebase and return the URL
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    photo_url = f"http://localhost:8000/{UPLOAD_DIR}/{file.filename}"
    return {"photo_url": photo_url}


class PostRequest(BaseModel):
    content: str
    photo_url: str | None = None


@app.post("/fb_post")
async def create_facebook_post(post: PostRequest):
    post_manager = FacebookPostManager(ACCESS_TOKEN, PAGE_ID)
    post_id = post_manager.create_post(
        message=post.content,
        # media_url=post.photo_url
    )

    print ({
        "content": post.content,
        "photo_url": post.photo_url,
        # "post_id": post_id
    })

    return {
        "content": post.content,
        "photo_url": post.photo_url,
        # "post_id": post_id
    }