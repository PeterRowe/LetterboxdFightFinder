from app.app import App

def test_get_user_reviews():
    ratings = App.get_user_reviews(username='Prowe')
    # Below assertions work for this test because I know that these films are rated on different
    # webpages and the ratings are correct
    assert ratings['poison-2023'] == 4.0
    assert ratings['the-killing-of-a-sacred-deer'] == 4.5
    assert ratings['the-holy-mountain'] == 4.0

def test_get_user_followers():
    # This will break every time I follow someone but what can you do
    followers = App.get_user_followers(username='PRowe')
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
