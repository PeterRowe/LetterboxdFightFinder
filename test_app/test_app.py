from app.app import App

def test_get_user_reviews():
    ratings = App.get_user_reviews(username='Prowe')
    # Below assertions work for this test because I know that these films are rated on different
    # webpages and the ratings are correct
    assert ratings['poison-2023'] == 4.0
    assert ratings['the-killing-of-a-sacred-deer'] == 4.5
    assert ratings['the-holy-mountain'] == 4.0
