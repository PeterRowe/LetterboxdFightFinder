import requests
import os
import json
from multiprocessing import Pool
from functools import cache

API_KEY = os.environ["API_KEY"]
TMDB_URL = "https://api.themoviedb.org/3"
HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer " + API_KEY
}

class TMDBAPIHandler:
    """
    Class for handling API request to TMDB.
    """
    def get_film_posters(self, films=list[str]) -> list[str]:
        """Scrapes the passed in poster urls from The Movie Data Base.
        
        :param films: The list of films you want to get poster urls for
        :returns: A list of urls of posters on TMDB in the same order as the passed in list"""
        poster_urls = []
        with Pool() as p:
            poster_urls_dicts = p.map(self._get_single_film_poster, films)
            p.terminate()
        poster_urls_dict = {k:v for poster_url_dict in poster_urls_dicts for (k,v) in poster_url_dict.items()}
        return poster_urls_dict
    
    @cache
    def _get_single_film_poster(self, film: str) -> dict[str|str]:
        """
        Gets the poster url rating for a single film
        :param film: The name of the film
        :returns: The poster url for the inputted film in a dict with format {<film name>: <poster url>}
        """
        # Letterboxd and TMDB sometimes disagree on year, so they're curring cut off. This means sometimes the wrong
        # film might be selected if there are multiples of the same name, but this is a rarer occurance than disagreements.
        film_title_only = film[:-5] if film[-4:].isdigit() else film
        try:
            search_response = json.loads(requests.get(TMDB_URL+"/search/movie", params={"query": film_title_only}, headers=HEADERS).text)
            film_id = search_response["results"][0]['id']
            poster_response = json.loads(requests.get(TMDB_URL+"/movie/"+str(film_id)+"/images", headers=HEADERS).text)
            poster_url = "https://image.tmdb.org/t/p/original"+poster_response["posters"][0]["file_path"]
        except:
            # Just can't find the poster, oh well. I'll default to 'Junior' because I think it's funny
            poster_url = "https://image.tmdb.org/t/p/w1280/eQmgPrXf7c7daRdl3Zwgm65lw3o.jpg"
        return {film: poster_url}