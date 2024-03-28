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

@app.get('/initial-mutual-and-community-differences/', response_class=HTMLResponse)
def get_initial_mutual_and_community_differences(request: Request, username: str):

    # Caches values for other endpoints to use
    global user_and_mutual_ratings
    global user_and_mutual_differences
    global user_and_community_ratings
    global user_and_community_differences

    user_and_mutual_ratings = letterboxd_scraper.get_user_and_mutuals_ratings(username=username)
    user_and_mutual_differences = ratings_analytics.get_differences_in_ratings(user_and_mutual_ratings)
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

    user_and_mutual_differences_poster_urls = tmdb_api_handler.get_film_posters(
        user_and_mutual_differences["Film"][0:5])

    # Putting posters in correct order
    current_user_and_mutual_differences_poster_urls = [user_and_mutual_differences_poster_urls[film]
                                 for film in user_and_mutual_differences["Film"].iloc[0:5]]

    user_and_community_ratings = letterboxd_scraper.get_user_and_community_ratings(username=username)
    user_and_community_differences = ratings_analytics.get_differences_in_ratings(user_and_community_ratings)

    user_and_community_differences_poster_urls = tmdb_api_handler.get_film_posters(
        user_and_community_differences["Film"][0:5])
    
    # Putting posters in correct order
    current_user_and_community_differences_poster_urls = [user_and_community_differences_poster_urls[film]
                                 for film in user_and_community_differences["Film"].iloc[0:5]]
    
    return templates.TemplateResponse(
        "initial_mutual_and_community_results.html",
        {
            "request": request, 
            "username": username,
            "user_and_mutual_differences": user_and_mutual_differences.iloc[0:5],
            "user_and_mutual_differences_poster_urls": current_user_and_mutual_differences_poster_urls,
            "user_and_community_differences": user_and_community_differences.iloc[0:5],
            "user_and_community_differences_poster_urls": current_user_and_community_differences_poster_urls
        }
        )

@app.get('/additional-mutuals-differences/', response_class=HTMLResponse)
def get_additional_mutuals_differences(request: Request, username: str, page: int = 0):
    
    user_and_mutual_differences_poster_urls = tmdb_api_handler.get_film_posters(
        user_and_mutual_differences["Film"][page*5:page*5+5])
    
    # Putting posters in correct order
    current_page_film_posters = [user_and_mutual_differences_poster_urls[film]
                                 for film in user_and_mutual_differences["Film"].iloc[page*5:page*5+5]]

    return templates.TemplateResponse(
        "mutuals_results_additional_rows.html",
        {
            "request": request, 
            "username": username,
            "page": page + 1,
            "user_and_mutual_differences": user_and_mutual_differences.iloc[page*5:page*5+5],
            "user_and_mutual_differences_poster_urls": current_page_film_posters
        }
        )

@app.get('/additional-community-differences/', response_class=HTMLResponse)
def get_additional_community_differences(request: Request, username: str, page: int = 0): 
    
    user_and_community_differences_poster_urls = tmdb_api_handler.get_film_posters(
        user_and_community_differences["Film"][page*5:page*5+5])
    
    current_page_film_posters = [user_and_community_differences_poster_urls[film]
                                for film in user_and_community_differences["Film"].iloc[page*5:page*5+5]]

    return templates.TemplateResponse(
            "community_results_additional_rows.html",
            {
                "request": request,
                "username": username,
                "page": page + 1,
                "user_and_community_differences": user_and_community_differences.iloc[page*5:page*5+5],
                "user_and_community_differences_poster_urls": current_page_film_posters
            }
        )
    

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # always good manners to return back the request
    return templates.TemplateResponse("index.html", {"request": request})
