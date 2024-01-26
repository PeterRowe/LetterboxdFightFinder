import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

HEADERS={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'} #Hehe sneaky, I'll change this when I get the API


class LetterboxdScraper():
    """
    Class for collecting methods that scrape data from Letterboxd
    """
    def _get_user_reviews(self, username: str) -> dict[str, float]:
        """
        Scrapes the film ratings from the inputted usernames pages on letterboxd
        :param username: The username of the letterboxd user you want to collect ratings from
        :returns: A dictionary containing the ratings of the users watched films. The keys
                  are the film titles and the values are the ratings. Films logged but not
                  rated will have a value of None"""
        page_number = 0
        ratings = {}
        while True:
            page_number += 1
            response = urlopen(Request(headers=HEADERS, url=f'https://letterboxd.com/{username}/films/page/{page_number}')).read().decode("utf-8")
            soup = BeautifulSoup(response)
            page_ratings = soup.find_all("ul", {"class": "poster-list"})[0].contents[1::2]
            if len(page_ratings) == 0:
                break
            for film_and_rating in page_ratings:
                ratings[film_and_rating.contents[1]['data-film-slug']] = (
                    float(film_and_rating.contents[3].contents[1]['class'][3].split('-')[1])/2
                    if len(film_and_rating.contents[3].contents) > 1
                    else None
                )
            
        ratings = pd.DataFrame.from_dict(data=ratings, orient='index', columns=[f"{username}'s ratings"])
        return ratings
    
    
    def _get_user_followers(self, username: str) -> list[str]:
        """
        Scrapes the inputted username's followers from Letterboxd
        :param username: The username of the letterboxd user you want to collect followers from
        :return: The inputted users followers in a list"""
        followers = []
        page_number = 0
        while True:
            page_number+=1
            response = urlopen(Request(headers=HEADERS, url=f'https://letterboxd.com/{username}/followers/page/{page_number}')).read().decode("utf-8")
            soup = BeautifulSoup(response)
            new_followers = [
                person_summary.contents[1]["href"][1:-1]
                for person_summary in soup.find_all("div", {"class": "person-summary"})
            ]
            if len(new_followers) == 0:
                break
            followers = followers + new_followers

        return followers
    
    def get_user_and_followers_reviews(self, username: str) -> pd.DataFrame:
        followers = self._get_user_followers(username=username)
        user_ratings = self._get_user_reviews(username=username)
        for follower in followers:
            follower_ratings = self._get_user_reviews(username=follower)
            user_ratings=user_ratings.join(follower_ratings, how='left')

