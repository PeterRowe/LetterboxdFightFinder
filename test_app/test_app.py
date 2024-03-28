from fastapi import Request, FastAPI
from fastapi.testclient import TestClient

from app.app import app
from expected_responses.expected_top_five_differences_endpoint_response import EXPECTED_TOP_FIVE_DIFFERENCES_ENDPOINT_RESPONSE

client = TestClient(app)

def test_get_top_five_differences_endpoint():
    response = client.get("/initial-mutual-and-community-differences", params={"username": "prowe"})
    # This will break if someone posts a top five terrible take. 
    # Hopefully that's a rare occurrence.
    assert response.text == EXPECTED_TOP_FIVE_DIFFERENCES_ENDPOINT_RESPONSE

def test_additional_community_differences():
    response = client.get("/initial-mutual-and-community-differences", params={"username": "prowe"})
    response = client.get("/additional-community-differences", params={"username": "prowe", "page": "1"})