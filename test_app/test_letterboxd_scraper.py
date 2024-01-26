from app.letterboxd_scraper import LetterboxdScraper

def test_get_user_reviews():
    ratings = LetterboxdScraper.get_user_reviews(username='Prowe')
    # Below assertions work for this test because I know that these films are rated on different
    # webpages and the ratings are correct
    assert ratings.loc['poison-2023']['rating'] == 4.0
    assert ratings.loc['the-killing-of-a-sacred-deer']['rating'] == 4.5
    assert ratings.loc['the-holy-mountain']['rating'] == 4.0

def test_get_user_followers():
    # This will break every time I follow someone but what can you do
    followers = LetterboxdScraper.get_user_followers(username='PRowe')
    assert followers == [
        'jentron3000',
        'postboxqueen420',
        'ferguscunning',
        'harritaylor',
        'georgiebr97',
        'livelaughluan',
        'bluebottles',
        'fuverdred',
        'geminyxia',
        'bethanyrosetta',
        'bbcparliament'
    ]