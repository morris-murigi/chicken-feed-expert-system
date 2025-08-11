# app/main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .inference_engine import recommend_feed
from .data_models import RecommendRequest

app = FastAPI(title="Chicken Feed Expert System (MVP)")

# serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/ui/templates")

@app.get("/", response_class=HTMLResponse)
def read_dashboard(request: Request):
    # show form
    chicken_types = ["Chick", "Pullet", "Layer", "Broiler", "Kienyeji"]
    return templates.TemplateResponse("dashboard.html", {"request": request, "chicken_types": chicken_types})

@app.post("/recommend", response_class=HTMLResponse)
def post_recommend(request: Request, type: str = Form(...), age_weeks: int = Form(...)):
    result = recommend_feed(type, age_weeks, include_recipes=True)
    return templates.TemplateResponse("result.html", {"request": request, "result": result})
