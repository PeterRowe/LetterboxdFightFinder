from math import floor

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.letterboxd_scraper import LetterboxdScraper
from app.ratings_analytics import RatingsAnalytics
from app.tmdb_api_handler import TMDBAPIHandler

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
letterboxd_scraper = LetterboxdScraper()
ratings_analytics = RatingsAnalytics()
tmdb_api_handler = TMDBAPIHandler()

templates = Jinja2Templates(directory="templates")

@app.get('/top-five-differences/', response_class=HTMLResponse)
def get_top_five_differences(request: Request, username: str):
    ratings = letterboxd_scraper.get_user_and_mutuals_reviews(username=username)
    differences = ratings_analytics.get_differences_in_ratings(ratings).iloc[0:5]
    poster_urls = tmdb_api_handler.get_film_posters(differences["Film"])
    for row_number in range(5):
        star_rating = ""
        for star in range(floor(differences.iloc[row_number]["Mutual Rating"])):
            star_rating = star_rating + "★"
        star_rating = star_rating if (floor(differences.iloc[row_number]["Mutual Rating"]) ==
                                      differences.iloc[row_number]["Mutual Rating"]) else star_rating + "½"
        differences.iat[row_number, 3] = star_rating
        star_rating = ""
        for star in range(floor(differences.iloc[row_number]["User Rating"])):
            star_rating = star_rating + "★"
        star_rating = star_rating if (floor(differences.iloc[row_number]["User Rating"]) ==
                                      differences.iloc[row_number]["User Rating"]) else star_rating + "½"
        differences.iat[row_number, 4] = star_rating
    return templates.TemplateResponse(
        "results.html",
        {"request": request, "differences": differences, "poster_urls": poster_urls}
        )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # always good manners to return back the request
    return templates.TemplateResponse("index.html", {"request": request})
