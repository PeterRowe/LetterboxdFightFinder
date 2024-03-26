import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from functools import cache
from multiprocessing import Pool

HEADERS={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'} #Hehe sneaky, I'll change this when I get the API


class LetterboxdScraper():
    """
    Class for collecting methods that scrape data from Letterboxd
    """
    @cache
    def _get_user_ratings(self, username: str) -> pd.DataFrame:
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
                # If statement filters out films that are logged and neither liked or rated and
                # films that are liked but not rated
                if (len(film_and_rating.contents[3].contents) > 1 and
                        film_and_rating.contents[3].contents[1]['class'][3].startswith('rated')):
                    ratings[film_and_rating.contents[1]['data-film-slug']] = (
                        float(film_and_rating.contents[3].contents[1]['class'][3].split('-')[1])/2
                    
                )
            
        ratings = pd.DataFrame.from_dict(data=ratings, orient='index', columns=[username])
        return ratings
    
    @cache
    def _get_user_mutuals(self, username: str) -> list[str]:
        """
        Scrapes the inputted username's mutuals from Letterboxd
        :param username: The username of the letterboxd user you want to collect mutuals from
        :return: The inputted users mutuals in a list"""
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

        following = []
        page_number = 0
        while True:
            page_number+=1
            response = urlopen(Request(headers=HEADERS, url=f'https://letterboxd.com/{username}/following/page/{page_number}')).read().decode("utf-8")
            soup = BeautifulSoup(response)
            new_following = [
                person_summary.contents[1]["href"][1:-1]
                for person_summary in soup.find_all("div", {"class": "person-summary"})
            ]
            if len(new_following) == 0:
                break
            following = following + new_following

        # The list of mutuals is sorted alphabetically for consistency. This ensures that if there are multiple ratings tied for fifth place
        # the same review is chosen every time.
        mutuals = sorted(list(set(followers) & set(following)))
        return mutuals
    
    def _get_community_ratings(self, user_ratings: pd.DataFrame) -> pd.DataFrame:
        """
        Finds the average community rating for all of the films rated by the user. This method
        is parallelised so must not be run as part of a parallel operation.
        :param user_ratings: A pandas dataframe where the index are the film names and the values are the user rating
        :returns: A pandas datafram with a single column named "Community". Indexes are the film names and the values
                  are the community rating for that film."""
        # Duplicate user ratings dataframe, ratings will be overwitten with community ratings
        community_ratings = user_ratings.copy()
        community_ratings = community_ratings.rename(columns={community_ratings.columns[0]: "Community"})
        with Pool() as p:
            community_ratings_dicts = p.map(self._get_community_rating_for_single_film, community_ratings.index)
            p.terminate()
        for film_and_community_rating in community_ratings_dicts:
            film = list(film_and_community_rating)[0]
            community_ratings.loc[film] = film_and_community_rating[film]
        return community_ratings
    
    def _get_community_rating_for_single_film(self, film: str) -> dict[str, float]:
        """
        Gets the average community rating for a single film
        :param film: The name of the film
        :returns: The community rating for the inputted film in a dict with format {<film name>: <rating>}
        """
        response = urlopen(Request(headers=HEADERS, url=f'https://letterboxd.com/csi/film/{film}/rating-histogram')).read().decode("utf-8")
        soup = BeautifulSoup(response)
        rating = float(soup.find("span").text)
        return {film: rating}
    
    def get_user_and_mutuals_ratings(self, username: str) -> pd.DataFrame:
        """
        Finds the username's ratings and places them in the left most column of the resulting dataframe. Mutuals
        ratings that have been rated by the user are then placed in subsequent columns under the column name 
        {username}'s ratings. Films that the user has rated but the mutual hasn't are given a score of 0
        :param username: the letterboxd username
        :returns: A dataframe containing the usernames ratings and mutuals ratings of those films
        """
        mutuals = self._get_user_mutuals(username=username)
        user_ratings = self._get_user_ratings(username=username)
        with Pool() as p:
            mutual_ratings = p.map(self._get_user_ratings, mutuals)
        user_ratings=user_ratings.join(mutual_ratings, how='left')
        return user_ratings
    
    def get_user_and_community_ratings(self, username: str) -> pd.DataFrame:
        user_ratings = self._get_user_ratings(username=username)
        community_ratings = self._get_community_ratings(user_ratings=user_ratings)
        user_and_community_ratings = pd.concat([user_ratings, community_ratings], axis=1)
        return user_and_community_ratings

