from zoneinfo import ZoneInfo
from datetime import datetime

import json
import re
from pathlib import Path

CONFIG_FILE = Path(__file__).with_name("config.json")

DEFAULT_CONFIG = {
    "timezone": "America/Chicago",
    "favorite_team": None,
    "favorite_team_id": None,
    "team_fixture_limit": 5,
}

LEAGUES = {
    "premierleague": {"name": "Premier League", "code": "PL"},
    "laliga": {"name": "La Liga", "code": "PD"},
    "bundesliga": {"name": "Bundesliga", "code": "BL1"},
    "seriea": {"name": "Serie A", "code": "SA"},
    "ligue1": {"name": "Ligue 1", "code": "FL1"},
    "championsleague": {"name": "Champions League", "code": "CL"},
}

LEAGUE_ALIASES = {
    "premier": "premierleague",
    "premierleague": "premierleague",
    "epl": "premierleague",
    "pl": "premierleague",
    "laliga": "laliga",
    "liga": "laliga",
    "pd": "laliga",
    "bundesliga": "bundesliga",
    "bl1": "bundesliga",
    "seriea": "seriea",
    "sa": "seriea",
    "ligue1": "ligue1",
    "fl1": "ligue1",
    "championsleague": "championsleague",
    "champions": "championsleague",
    "ucl": "championsleague",
    "cl": "championsleague",
}

TEAMS = {
    # Premier League
    "arsenal": {"id": 57, "name": "Arsenal"},
    "astonvilla": {"id": 58, "name": "Aston Villa"},
    "chelsea": {"id": 61, "name": "Chelsea"},
    "everton": {"id": 62, "name": "Everton"},
    "fulham": {"id": 63, "name": "Fulham"},
    "liverpool": {"id": 64, "name": "Liverpool"},
    "mancity": {"id": 65, "name": "Man City"},
    "manunited": {"id": 66, "name": "Man United"},
    "newcastle": {"id": 67, "name": "Newcastle"},
    "sunderland": {"id": 71, "name": "Sunderland"},
    "tottenham": {"id": 73, "name": "Tottenham"},
    "hullcity": {"id": 322, "name": "Hull City"},
    "leedsunited": {"id": 341, "name": "Leeds United"},
    "ipswichtown": {"id": 349, "name": "Ipswich Town"},
    "nottingham": {"id": 351, "name": "Nottingham"},
    "crystalpalace": {"id": 354, "name": "Crystal Palace"},
    "brightonhove": {"id": 397, "name": "Brighton Hove"},
    "brentford": {"id": 402, "name": "Brentford"},
    "bournemouth": {"id": 1044, "name": "Bournemouth"},
    "coventrycity": {"id": 1076, "name": "Coventry City"},

    # La Liga
    "athletic": {"id": 77, "name": "Athletic"},
    "atleti": {"id": 78, "name": "Atleti"},
    "osasuna": {"id": 79, "name": "Osasuna"},
    "espanyol": {"id": 80, "name": "Espanyol"},
    "barca": {"id": 81, "name": "Barça"},
    "getafe": {"id": 82, "name": "Getafe"},
    "malaga": {"id": 84, "name": "Málaga"},
    "realmadrid": {"id": 86, "name": "Real Madrid"},
    "rayovallecano": {"id": 87, "name": "Rayo Vallecano"},
    "levante": {"id": 88, "name": "Levante"},
    "realbetis": {"id": 90, "name": "Real Betis"},
    "realsociedad": {"id": 92, "name": "Real Sociedad"},
    "villarreal": {"id": 94, "name": "Villarreal"},
    "valencia": {"id": 95, "name": "Valencia"},
    "alaves": {"id": 263, "name": "Alavés"},
    "elche": {"id": 285, "name": "Elche"},
    "celta": {"id": 558, "name": "Celta"},
    "sevillafc": {"id": 559, "name": "Sevilla FC"},
    "deportivo": {"id": 560, "name": "Deportivo"},
    "santander": {"id": 5335, "name": "Santander"},

    # Bundesliga
    "1fckoln": {"id": 1, "name": "1. FC Köln"},
    "hoffenheim": {"id": 2, "name": "Hoffenheim"},
    "leverkusen": {"id": 3, "name": "Leverkusen"},
    "dortmund": {"id": 4, "name": "Dortmund"},
    "bayern": {"id": 5, "name": "Bayern"},
    "schalke": {"id": 6, "name": "Schalke"},
    "hsv": {"id": 7, "name": "HSV"},
    "stuttgart": {"id": 10, "name": "Stuttgart"},
    "bremen": {"id": 12, "name": "Bremen"},
    "mainz": {"id": 15, "name": "Mainz"},
    "augsburg": {"id": 16, "name": "Augsburg"},
    "freiburg": {"id": 17, "name": "Freiburg"},
    "mgladbach": {"id": 18, "name": "M'gladbach"},
    "frankfurt": {"id": 19, "name": "Frankfurt"},
    "unionberlin": {"id": 28, "name": "Union Berlin"},
    "scpaderborn": {"id": 29, "name": "SC Paderborn"},
    "elversberg": {"id": 719, "name": "Elversberg"},
    "rbleipzig": {"id": 721, "name": "RB Leipzig"},

    # Serie A
    "milan": {"id": 98, "name": "Milan"},
    "fiorentina": {"id": 99, "name": "Fiorentina"},
    "roma": {"id": 100, "name": "Roma"},
    "atalanta": {"id": 102, "name": "Atalanta"},
    "bologna": {"id": 103, "name": "Bologna"},
    "cagliari": {"id": 104, "name": "Cagliari"},
    "genoa": {"id": 107, "name": "Genoa"},
    "inter": {"id": 108, "name": "Inter"},
    "juventus": {"id": 109, "name": "Juventus"},
    "lazio": {"id": 110, "name": "Lazio"},
    "parma": {"id": 112, "name": "Parma"},
    "napoli": {"id": 113, "name": "Napoli"},
    "udinese": {"id": 115, "name": "Udinese"},
    "veneziafc": {"id": 454, "name": "Venezia FC"},
    "frosinone": {"id": 470, "name": "Frosinone"},
    "sassuolo": {"id": 471, "name": "Sassuolo"},
    "torino": {"id": 586, "name": "Torino"},
    "lecce": {"id": 5890, "name": "Lecce"},
    "monza": {"id": 5911, "name": "Monza"},
    "como1907": {"id": 7397, "name": "Como 1907"},

    # Ligue 1
    "toulouse": {"id": 511, "name": "Toulouse"},
    "brest": {"id": 512, "name": "Brest"},
    "marseille": {"id": 516, "name": "Marseille"},
    "auxerre": {"id": 519, "name": "Auxerre"},
    "lille": {"id": 521, "name": "Lille"},
    "nice": {"id": 522, "name": "Nice"},
    "olympiquelyon": {"id": 523, "name": "Olympique Lyon"},
    "psg": {"id": 524, "name": "PSG"},
    "lorient": {"id": 525, "name": "Lorient"},
    "staderennais": {"id": 529, "name": "Stade Rennais"},
    "troyes": {"id": 531, "name": "Troyes"},
    "angerssco": {"id": 532, "name": "Angers SCO"},
    "lehavre": {"id": 533, "name": "Le Havre"},
    "lemans": {"id": 535, "name": "Le Mans"},
    "rclens": {"id": 546, "name": "RC Lens"},
    "monaco": {"id": 548, "name": "Monaco"},
    "strasbourg": {"id": 576, "name": "Strasbourg"},
    "parisfc": {"id": 1045, "name": "Paris FC"},

    # Other Champions League Clubs
    "sportingcp": {"id": 498, "name": "Sporting CP"},
    "porto": {"id": 503, "name": "Porto"},
    "galatasaray": {"id": 610, "name": "Galatasaray"},
    "fenerbahce": {"id": 613, "name": "Fenerbahçe"},
    "psv": {"id": 674, "name": "PSV"},
    "feyenoord": {"id": 675, "name": "Feyenoord"},
    "clubbrugge": {"id": 851, "name": "Club Brugge"},
    "slaviapraha": {"id": 930, "name": "Slavia Praha"},
    "shaktar": {"id": 1887, "name": "Shaktar"},
    "paeaek": {"id": 1899, "name": "PAE AEK"},
    "lask": {"id": 2016, "name": "LASK"},
    "viking": {"id": 5720, "name": "Viking"},
    "bodoglimt": {"id": 5721, "name": "Bodø/Glimt"},
    "slbratislava": {"id": 7509, "name": "Sl. Bratislava"},
    "sabahfk": {"id": 10233, "name": "Sabah FK"},
}

TEAM_ALIASES = {
    # Premier League
    "afc": "arsenal",
    "gunners": "arsenal",
    "villa": "astonvilla",
    "avfc": "astonvilla",
    "cfc": "chelsea",
    "blues": "chelsea",
    "toffees": "everton",
    "lfc": "liverpool",
    "reds": "liverpool",
    "city": "mancity",
    "mcfc": "mancity",
    "manchestercity": "mancity",
    "citizens": "mancity",
    "united": "manunited",
    "mufc": "manunited",
    "manchesterunited": "manunited",
    "manutd": "manunited",
    "reddevils": "manunited",
    "toon": "newcastle",
    "newcastleunited": "newcastle",
    "spurs": "tottenham",
    "hotspur": "tottenham",
    "tottenhamhotspur": "tottenham",
    "thfc": "tottenham",
    "hull": "hullcity",
    "leeds": "leedsunited",
    "ipswich": "ipswichtown",
    "forest": "nottingham",
    "nottinghamforest": "nottingham",
    "nffc": "nottingham",
    "palace": "crystalpalace",
    "cpfc": "crystalpalace",
    "brighton": "brightonhove",
    "bhafc": "brightonhove",
    "bees": "brentford",
    "cherries": "bournemouth",
    "afcbournemouth": "bournemouth",
    "coventry": "coventrycity",

    # La Liga
    "athleticbilbao": "athletic",
    "bilbao": "athletic",
    "atletico": "atleti",
    "atleticodemadrid": "atleti",
    "atleticomadrid": "atleti",
    "rcdespanyol": "espanyol",
    "barcelona": "barca",
    "fcb": "barca",
    "fcbarcelona": "barca",
    "real": "realmadrid",
    "rm": "realmadrid",
    "rmcf": "realmadrid",
    "madrid": "realmadrid",
    "rayo": "rayovallecano",
    "betis": "realbetis",
    "sociedad": "realsociedad",
    "lafe": "realsociedad",
    "submarinoamarillo": "villarreal",
    "villareal": "villarreal",
    "vcf": "valencia",
    "deportivocelta": "celta",
    "celtavigo": "celta",
    "sevilla": "sevillafc",
    "depor": "deportivo",
    "racing": "santander",
    "racingsantander": "santander",

    # Bundesliga
    "koln": "1fckoln",
    "cologne": "1fckoln",
    "bayer": "leverkusen",
    "bayerleverkusen": "leverkusen",
    "bvb": "dortmund",
    "borussiadortmund": "dortmund",
    "fcbayern": "bayern",
    "bayernmunchen": "bayern",
    "bayernmunich": "bayern",
    "schalke04": "schalke",
    "s04": "schalke",
    "hamburg": "hsv",
    "hamburgersv": "hsv",
    "vfb": "stuttgart",
    "vfbstuttgart": "stuttgart",
    "werder": "bremen",
    "werderbremen": "bremen",
    "fsvmainz": "mainz",
    "mainz05": "mainz",
    "fca": "augsburg",
    "scfreiburg": "freiburg",
    "gladbach": "mgladbach",
    "borussia": "mgladbach",
    "eintracht": "frankfurt",
    "eintrachtfrankfurt": "frankfurt",
    "union": "unionberlin",
    "paderborn": "scpaderborn",
    "leipzig": "rbleipzig",
    "rasenballsportleipzig": "rbleipzig",

    # Serie A
    "acmilan": "milan",
    "acm": "milan",
    "viola": "fiorentina",
    "asroma": "roma",
    "giallorossi": "roma",
    "intermilan": "inter",
    "internazionale": "inter",
    "juve": "juventus",
    "ssclazio": "lazio",
    "sscnapoli": "napoli",
    "venezia": "veneziafc",
    "toro": "torino",
    "como": "como1907",

    # Ligue 1
    "om": "marseille",
    "olympiquedemarseille": "marseille",
    "losc": "lille",
    "losclille": "lille",
    "ogcnice": "nice",
    "lyon": "olympiquelyon",
    "ol": "olympiquelyon",
    "parissaintgermain": "psg",
    "rennes": "staderennais",
    "angers": "angerssco",
    "lens": "rclens",
    "asmonaco": "monaco",
    "racingstrasbourg": "strasbourg",

    # Champions League
    "sporting": "sportingcp",
    "sportinglisbon": "sportingcp",
    "fcporto": "porto",
    "gala": "galatasaray",
    "fener": "fenerbahce",
    "psveindhoven": "psv",
    "brugge": "clubbrugge",
    "slavia": "slaviapraha",
    "shakhtar": "shaktar",
    "shakhtardonetsk": "shaktar",
    "aek": "paeaek",
    "aekathens": "paeaek",
    "bodo": "bodoglimt",
    "glimt": "bodoglimt",
    "slovan": "slbratislava",
    "slovanbratislava": "slbratislava",
}


# makes names easier to compare
def normalize_name(value):
    return re.sub(r"[^a-z0-9]", "", value.lower())


# finds a league from a normal name or alias
def get_league(value):
    key = normalize_name(value)
    key = LEAGUE_ALIASES.get(key, key)
    league = LEAGUES.get(key)
    if not league:
        raise RuntimeError(f"Unknown league: '{value}'")
    return league


# Finds a team by name using local aliases and substring matching
def get_team(team_name):
    clean_team_name = normalize_name(team_name)
    if not clean_team_name:
        return None

    # Resolve the direct alias if any aliases found
    key = TEAM_ALIASES.get(clean_team_name, clean_team_name)
    if key in TEAMS:
        return {"id": TEAMS[key]["id"], "shortName": TEAMS[key]["name"]}

    # FALLBACK: if direct alias lookup fails, check substring matching against local teams
    matched_teams = []

    for key, data in TEAMS.items():
        team_id = data["id"]
        team_name = data["name"]
        normalized_team_name = normalize_name(team_name)

        # Check if the search term appears inside the key or the team name
        if clean_team_name in key or clean_team_name in normalized_team_name:
            matched_teams.append({
                "id": team_id,
                "shortName": team_name
            })

    # Return the team only if exactly one unambiguous match was found
    if len(matched_teams) == 1:
        return matched_teams[0]
    else:
        # If multiple matches were found or no matches were found
        return None

# converts api time to the configured timezone


def format_datetime(utc_value):
    config = load_config()
    timezone = ZoneInfo(config["timezone"])
    value = utc_value.replace("Z", "+00:00")

    # convert UTC to local time
    local = datetime.fromisoformat(value).astimezone(timezone)

    # format date
    date = local.strftime("%m/%d/%Y")

    # format time
    time = local.strftime("%I:%M%p").lstrip("0").lower()

    return date, time


def load_config():
    config = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        try:
            with CONFIG_FILE.open("r", encoding="utf-8") as file:
                saved = json.load(file)
            if isinstance(saved, dict):
                config.update(saved)
        except Exception:
            print("Failed to load config file.")
    return config


def save_config(config):
    # saves local app settings
    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)
        file.write("\n")
