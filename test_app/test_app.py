from app import app


def test_get_top_five_differences_endpoint():
    app.get_top_five_differences(username='prowe')