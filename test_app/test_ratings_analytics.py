from app.ratings_analytics import RatingsAnalytics
from app.letterboxd_scraper import LetterboxdScraper


def test_get_biggest_differences_in_ratings():
    letterboxd_scraper = LetterboxdScraper()
    ratings = letterboxd_scraper.get_user_and_followers_reviews(username='bbcparliament')
    ratings_analytics = RatingsAnalytics()
    test = ratings_analytics.get_differences_in_ratings(ratings_dataframe=ratings)