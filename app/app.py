from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.letterboxd_scraper import LetterboxdScraper
from app.ratings_analytics import RatingsAnalytics

app = FastAPI()
letterboxd_scraper = LetterboxdScraper()
ratings_analytics = RatingsAnalytics()

templates = Jinja2Templates(directory="templates")

@app.get('/top-five-differences/{username}')
def get_top_five_differences(username: str):
    ratings = letterboxd_scraper.get_user_and_followers_reviews(username=username)
    differences = ratings_analytics.get_differences_in_ratings(ratings)
    return differences[0:5]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # always good manners to return back the request
    return templates.TemplateResponse("index.html", {"request": request})
