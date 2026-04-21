from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

posts : list[dict] = [{
    "name": "King Monish",
    "work" : "Rule the World."
},
{
    "name": "Inventor Monish",
    "work": "Invent New Tech"

}]


@app.get("/", include_in_schema=False)
@app.get('/posts', include_in_schema=False)
def home(requests : Request):
    return templates.TemplateResponse(requests, 'home.html')

@app.get("/kings")
def kings(requests : Request):
    return templates.TemplateResponse(requests, "home.html", {"posts": posts, "title" : "kings"})


@app.get('/api/kings')
def kings_api():
    return posts
