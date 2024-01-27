from fastapi import FastAPI

from app.letterboxd_scraper import LetterboxdScraper
from app.ratings_analytics import RatingsAnalytics

app = FastAPI()
letterboxd_scraper = LetterboxdScraper()
ratings_analytics = RatingsAnalytics()

@app.get('/top-five-differences/{username}')
def get_top_five_differences(username: str):
    ratings = letterboxd_scraper.get_user_and_followers_reviews(username=username)
    differences = ratings_analytics.get_differences_in_ratings(ratings)
    return differences[0:5]
