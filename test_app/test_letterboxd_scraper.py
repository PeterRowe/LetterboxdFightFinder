from app.letterboxd_scraper import LetterboxdScraper

LetterboxdScraperTestInstance = LetterboxdScraper()

def test_get_user_reviews():
    ratings = LetterboxdScraperTestInstance._get_user_reviews(username='Prowe')
    # Below assertions work for this test because I know that these films are rated on different
    # webpages and the ratings are correct
    assert ratings.loc['poison-2023']['rating'] == 4.0
    assert ratings.loc['the-killing-of-a-sacred-deer']['rating'] == 4.5
    assert ratings.loc['the-holy-mountain']['rating'] == 4.0

def test_get_user_mutuals():
    # This will break every time I get a new mutual someone but what can you do
    mutuals = LetterboxdScraperTestInstance._get_user_mutuals(username='prowe')
    assert mutuals == [
        'bbcparliament',
        'bethanyrosetta',
        'bluebottles',
        'ferguscunning',
        'fuverdred',
        'geminyxia',
        'georgiebr97',
        'harritaylor',
        'jentron3000',
        'livelaughluan',
        'postboxqueen420'
    ]

def test_get_user_and_mutuals_reviews():
    test = LetterboxdScraperTestInstance.get_user_and_mutuals_reviews(username='PRowe')