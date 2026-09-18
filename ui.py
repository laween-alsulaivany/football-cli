from rich.table import Table
from config import format_datetime


def build_fixtures_table(title, matches, show_competition=False):
    table = Table(title=title)
    if show_competition:
        table.add_column("Competition", style="cyan")
    table.add_column("Date")
    table.add_column("Time")
    table.add_column("Home")
    table.add_column("Away")

    for match in matches:
        date, time = format_datetime(match["utcDate"])
        home = match.get("homeTeam", {}).get("shortName") or match.get("homeTeam", {}).get("name", "-")
        away = match.get("awayTeam", {}).get("shortName") or match.get("awayTeam", {}).get("name", "-")

        if show_competition:
            comp = match.get("competition", {}).get("name", "-")
            table.add_row(comp, date, time, home, away)
        else:
            table.add_row(date, time, home, away)

    return table


def build_live_matches_table(matches):
    table = Table(title="Live Matches")
    table.add_column("Competition", style="cyan")
    table.add_column("Home")
    table.add_column("Score", justify="center", style="bold")
    table.add_column("Away")
    table.add_column("Status")

    for match in matches:
        score = match.get("score", {}).get("fullTime", {})
        home_score = score.get("home")
        away_score = score.get("away")
        score_text = "-" if home_score is None or away_score is None else f"{home_score}-{away_score}"

        competition = match.get("competition", {}).get("name", "-")
        home = match.get("homeTeam", {}).get("shortName") or match.get("homeTeam", {}).get("name", "-")
        away = match.get("awayTeam", {}).get("shortName") or match.get("awayTeam", {}).get("name", "-")
        status = match.get("status", "-").replace("_", " ").title()

        table.add_row(competition, home, score_text, away, status)
    return table


def build_standings_table(league_name, standings_rows):
    title = f"{league_name} Standings"
    table = Table(title=title)
    table.add_column("Pos", justify="right", style="cyan")
    table.add_column("Team")
    table.add_column("P", justify="right")
    table.add_column("W", justify="right", style="green")
    table.add_column("D", justify="right")
    table.add_column("L", justify="right", style="red")
    table.add_column("GF", justify="right")
    table.add_column("GA", justify="right")
    table.add_column("GD", justify="right")
    table.add_column("Pts", justify="right", style="bold")

    for row in standings_rows:
        gd = row.get("goalDifference", 0)
        gd_text = f"{gd:+d}"
        if gd > 0:
            gd_text = f"[green]{gd_text}[/green]"
        elif gd < 0:
            gd_text = f"[red]{gd_text}[/red]"

        team_name = row.get("team", {}).get("shortName") or row.get("team", {}).get("name", "-")

        table.add_row(
            str(row.get("position", "-")),
            team_name,
            str(row.get("playedGames", "-")),
            str(row.get("won", "-")),
            str(row.get("draw", "-")),
            str(row.get("lost", "-")),
            str(row.get("goalsFor", "-")),
            str(row.get("goalsAgainst", "-")),
            gd_text,
            str(row.get("points", "-")),
        )
    return table
