import click
from rich.console import Console

from api import get_league_fixtures, get_live_matches, get_standings, get_team_fixtures
from config import get_league, get_team, load_config, save_config
from ui import build_live_matches_table, build_fixtures_table, build_standings_table


class AliasedGroup(click.Group):
    aliases = {
        "standing": "standings",
        "myteam": "team",
        "favorite": "set-team",
    }

    def get_command(self, ctx, cmd_name):
        cmd_name = self.aliases.get(cmd_name, cmd_name)
        return super().get_command(ctx, cmd_name)


@click.group(cls=AliasedGroup)
def cli():
    """football scores and fixtures in your terminal."""


@cli.command("standings")
@click.argument("league", nargs=-1, required=True)
# shows the full standings for a league
def standings(league):
    """Show the current table for a league."""
    # concatenate the league argument into a single string again
    league_text = " ".join(league)
    league = get_league(league_text)
    if not league:
        raise click.ClickException(f"Unknown league: '{league_text}'")

    try:
        data = get_standings(league["code"])
    except RuntimeError as error:
        raise click.ClickException(str(error))

    # Get the total standings from the data
    total = None
    for item in data.get("standings", []):
        if item.get("type") == "TOTAL":
            total = item
            break

    if not total:
        raise click.ClickException("Standings are not available right now.")

    table = build_standings_table(league["name"], total.get("table", []))

    Console().print(table)


@cli.command("live")
# shows matches currently marked as in play
def live():
    """Show matches currently in play."""
    try:
        data = get_live_matches()
    except RuntimeError as error:
        raise click.ClickException(str(error))

    matches = data.get("matches", [])
    if not matches:
        Console().print("No live matches right now.")
        return

    table = build_live_matches_table(matches)
    Console().print(table)


@cli.command("fixtures")
@click.argument("league", nargs=-1, required=True)
# shows the next matchday for a league
def fixtures(league):
    """Show the next fixtures for a league or competition."""
    # concatenate the league argument into a single string again
    league_text = " ".join(league)
    league = get_league(league_text)
    if not league:
        raise click.ClickException(f"Unknown league: '{league_text}'")

    try:
        data = get_league_fixtures(league["code"])
    except RuntimeError as error:
        raise click.ClickException(str(error))

    matches = data.get("matches", [])
    if not matches:
        raise click.ClickException(f"No upcoming fixtures found for {league['name']}.")

    # Sort matches chronologically
    matches.sort(key=lambda m: m.get("utcDate", ""))

    # Check if this competition operates by numbered matchdays
    current_matchday = data.get("season", {}).get("currentMatchday")
    upcoming_matchdays = [m["matchday"] for m in matches if m.get("matchday")]

    if upcoming_matchdays:
        target_matchday = current_matchday if current_matchday in upcoming_matchdays else min(upcoming_matchdays)
        filtered = [m for m in matches if m.get("matchday") == target_matchday]
        title = f"{league['name']} — Matchday {target_matchday}"

    # Otherwise, handle cup rounds via 'stage'
    else:
        target_stage = matches[0].get("stage", "NEXT_ROUND")
        filtered = [m for m in matches if m.get("stage") == target_stage]
        stage_label = target_stage.replace("_", " ").title()
        title = f"{league['name']} — {stage_label}"

    table = build_fixtures_table(title, filtered)

    Console().print(table)


@cli.command("team")
@click.argument("team_name", nargs=-1)
# shows the next upcoming matches for a team
def team(team_name):
    """Show upcoming matches for a team."""
    config = load_config()
    limit = config.get("team_fixture_limit", 5)

    # if a team name is provided, use it
    if team_name:
        raw_name = " ".join(team_name)
        team = get_team(raw_name)

        if not team:
            raise click.ClickException(f"Team not found: {raw_name}")

        team_id, display_name = team["id"], team["shortName"]

    # otherwise, use the favorite team from the config
    else:
        team_id = config.get("favorite_team_id")
        display_name = config.get("favorite_team")
        if not team_id:
            raise click.ClickException("No favorite team set. Use: fb set-team <team>")

    try:
        data = get_team_fixtures(team_id, limit)
    except RuntimeError as error:
        raise click.ClickException(str(error))

    matches = data.get("matches", [])
    if not matches:
        raise click.ClickException(f"No upcoming matches found for {display_name}.")

    matches.sort(key=lambda match: match.get("utcDate", ""))
    table = build_fixtures_table(
        f"{display_name} — Upcoming Matches",
        matches[:limit],
        show_competition=True,
    )
    Console().print(table)


@cli.command("set-team")
@click.argument("team_name", nargs=-1, required=True)
# saves a favorite team
def set_team(team_name):
    """Set your favorite team."""
    name = " ".join(team_name)
    team = get_team(name)
    if not team:
        raise click.ClickException(f"Team not found: {name}")

    config = load_config()
    config["favorite_team"] = team["shortName"]
    config["favorite_team_id"] = team["id"]
    save_config(config)

    Console().print(f"Favorite team set to [bold]{team['shortName']}[/bold].")


if __name__ == "__main__":
    cli()
