import json
from pathlib import Path
from api import get_data
from config import LEAGUES

all_teams = {}

for league in LEAGUES.values():
    code = league["code"]
    name = league["name"]
    print(f"Fetching {name}...")

    data = get_data(f"competitions/{code}/teams")
    all_teams[name] = {
        team.get("shortName") or team.get("name"): team.get("id")
        for team in data.get("teams", [])
    }

Path("teams.json").write_text(json.dumps(all_teams, indent=2), encoding="utf-8")
print("Done! Check teams.json.")
