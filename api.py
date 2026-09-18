import os

import requests
from dotenv import load_dotenv

BASE_URL = "https://api.football-data.org/v4"
TIMEOUT = 10


# loads the api key
def get_api_key():
    load_dotenv()
    return os.getenv("FOOTBALL_API_KEY")


# gets data from the football api
def get_data(endpoint, params=None):
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("Error: FOOTBALL_API_KEY is missing from .env")

    url = f"{BASE_URL}/{endpoint}"
    headers = {"X-Auth-Token": api_key}  # football-data.org API requires the X-Auth-Token header

    try:
        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
    except requests.RequestException:
        raise RuntimeError("Could not connect to football-data.org.")

    if response.status_code == 429:
        raise RuntimeError("API rate limit reached. Try again in 1 minute.")
    if response.status_code == 403:
        raise RuntimeError("This data is not available on your football-data.org plan.")
    if response.status_code == 404:
        raise RuntimeError("Football data was not found.")
    if response.status_code >= 400:
        raise RuntimeError("Could not get football data.")

    try:
        return response.json()
    except ValueError:
        raise RuntimeError("Could not get football data.")


# gets league standings
def get_standings(code):
    return get_data(f"competitions/{code}/standings")


# gets matches that are currently live
def get_live_matches():
    return get_data("matches", {"status": "LIVE"})


# gets scheduled matches for a league
def get_league_fixtures(code):
    return get_data(f"competitions/{code}/matches", {"status": "SCHEDULED"})


# gets upcoming matches for one team
def get_team_fixtures(team_id, limit=5):
    return get_data(f"teams/{team_id}/matches", {"status": "SCHEDULED", "limit": limit},)
