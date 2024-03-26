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

    #User and mutual differences
    user_and_mutual_ratings = letterboxd_scraper.get_user_and_mutuals_ratings(username=username)
    user_and_mutual_differences = ratings_analytics.get_differences_in_ratings(user_and_mutual_ratings).iloc[0:5]
    user_and_mutual_differences_poster_urls = tmdb_api_handler.get_film_posters(user_and_mutual_differences["Film"])
    for row_number in range(5):
        star_rating = ""
        for star in range(floor(user_and_mutual_differences.iloc[row_number]["Mutual Rating"])):
            star_rating = star_rating + "★"
        star_rating = star_rating if (floor(user_and_mutual_differences.iloc[row_number]["Mutual Rating"]) ==
                                      user_and_mutual_differences.iloc[row_number]["Mutual Rating"]) else star_rating + "½"
        user_and_mutual_differences.iat[row_number, 3] = star_rating
        star_rating = ""
        for star in range(floor(user_and_mutual_differences.iloc[row_number]["User Rating"])):
            star_rating = star_rating + "★"
        star_rating = star_rating if (floor(user_and_mutual_differences.iloc[row_number]["User Rating"]) ==
                                      user_and_mutual_differences.iloc[row_number]["User Rating"]) else star_rating + "½"
        user_and_mutual_differences.iat[row_number, 4] = star_rating

    #User and community differences
        
    #TODO: convert user ratings to star
    user_and_community_ratings = letterboxd_scraper.get_user_and_community_ratings(username=username)
    user_and_community_differences = ratings_analytics.get_differences_in_ratings(user_and_community_ratings)[0:5]
    user_and_community_differences_poster_urls = tmdb_api_handler.get_film_posters(user_and_community_differences["Film"])
        
    return templates.TemplateResponse(
        "results.html",
        {
            "request": request, 
            "user_and_mutual_differences": user_and_mutual_differences,
            "user_and_mutual_differences_poster_urls": user_and_mutual_differences_poster_urls,
            "user_and_community_differences": user_and_community_differences,
            "user_and_community_differences_poster_urls": user_and_community_differences_poster_urls
        }
    )

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # always good manners to return back the request
    return templates.TemplateResponse("index.html", {"request": request})
