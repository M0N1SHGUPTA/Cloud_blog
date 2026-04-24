from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

#validators
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

#Pydantic-Schemas
from schemas import PostCreate, PostResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name = "static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]




#===================================Template EndPoints===========================================
@app.get('/posts', include_in_schema=False, name = "posts")
@app.get("/", include_in_schema=False, name = "home")
def home(requests : Request):
    return templates.TemplateResponse(requests, 'home.html', {"posts": posts, "title": "Cloud_Blog"})


@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(requests: Request, post_id : int):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse(
                requests,
                'post.html',
                {"post": post, "title" : title},
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found.")

#============================================End- Template Endpoints=============================================================

#======================================API endpoints============================================
@app.get('/api/posts', response_model=list[PostResponse])
def get_posts():
    return posts


@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id : int):

    for post in posts:
        if post.get("id") == post_id:
            return post
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not found.")


@app.post('/api/posts', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "content": post.content,
        "title": post.title,
        "date_posted": "Arpil 23 2025" 

    }
    posts.append(new_post)
    return new_post

#================================END API ENDPOINTS==============================================


# ===================================Validators================================================

'''
  validation handler is a gatekeeper and the
  Starlette handler covers everything that goes wrong
   after the request is accepted

'''
## StarletteHTTPException Handler
'''
  - StarletteHTTPException — fires during your route
  function's execution. This is for errors you raise
  yourself (nothing found, DB failures, auth errors,
  etc.) or any other HTTP error that occurs while
  processing the request.
'''
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
'''
  - RequestValidationError — fires before your route
  function even runs. FastAPI validates path/query
  params against type hints (e.g., post_id: int), and
   if it fails (/posts/abc), this handler catches it
  immediately.
'''
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )