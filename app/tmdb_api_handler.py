import requests
import os
import json

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
        for film in films:
            search_response = json.loads(requests.get(TMDB_URL+"/search/movie", params={"query": film}, headers=HEADERS).text)
            film_id = search_response["results"][0]['id']
            poster_response = json.loads(requests.get(TMDB_URL+"/movie/"+str(film_id)+"/images", headers=HEADERS).text)
            poster_urls.append("https://image.tmdb.org/t/p/original"+poster_response["posters"][0]["file_path"])
        return poster_urls