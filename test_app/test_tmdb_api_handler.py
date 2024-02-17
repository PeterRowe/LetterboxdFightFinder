from app.tmdb_api_handler import TMDBAPIHandler

tmdb_api_handler = TMDBAPIHandler()

def test_get_film_posters():
    films = ["star-wars", "little-women", "cars-2"]
    poster_urls = tmdb_api_handler.get_film_posters(films=films)
    assert poster_urls == [
        'https://image.tmdb.org/t/p/original/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg',
        'https://image.tmdb.org/t/p/original/yn5ihODtZ7ofn8pDYfxCmxh8AXI.jpg',
        'https://image.tmdb.org/t/p/original/okIz1HyxeVOMzYwwHUjH2pHi74I.jpg'
    ]
