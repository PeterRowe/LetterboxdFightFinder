from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.letterboxd_scraper import LetterboxdScraper
from app.ratings_analytics import RatingsAnalytics

app = FastAPI()
letterboxd_scraper = LetterboxdScraper()
ratings_analytics = RatingsAnalytics()

templates = Jinja2Templates(directory="templates")

@app.get('/top-five-differences/', response_class=HTMLResponse)
def get_top_five_differences(request: Request, username: str):
    ratings = letterboxd_scraper.get_user_and_followers_reviews(username=username)
    differences = ratings_analytics.get_differences_in_ratings(ratings).iloc[0:5]
    return templates.TemplateResponse(
        "results.html",
        {"request": request, "results": differences}
        )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # always good manners to return back the request
    return templates.TemplateResponse("index.html", {"request": request}) # Why does not passing request break?
