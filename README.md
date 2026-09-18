# football-cli

Small terminal football app built on top of [football-data.org](https://www.football-data.org/).

Mostly made because I wanted to type things like this instead of opening a browser:

```bash
fb standings laliga
fb fixtures pl
fb live
fb team barcelona
```

Uses `click` for the CLI and `rich` for the tables/output.

## Setup

Requires Python 3.14.

Clone the repo and create a virtual environment:

```bash
git clone https://github.com/laween-alsulaivany/football-cli.git
cd football-cli
python -m venv .venv
```

Activate the venv, then install:

```bash
pip install -e .
```

`pyproject.toml` installs the `fb` command, so after that you can use it directly instead of running `python main.py`.

### API key

Create a free account at [football-data.org](https://www.football-data.org/) and put your token in a `.env` file in the project directory:

```env
FOOTBALL_API_KEY=your_api_key_here
```

The free API tier has limits and live scores may not be completely instant.

## Usage

### Standings

```bash
fb standings laliga
fb standings pl
fb standings bundesliga
```

Shows the full league table with goal difference and points.

### Fixtures

```bash
fb fixtures pl
fb fixtures laliga
fb fixtures cl
```

Shows the next scheduled matchday, or the next tournament round for competitions like the Champions League.

### Live

```bash
fb live
```

Shows matches currently marked as live by the API.

### Team fixtures

```bash
fb team arsenal
fb team real madrid
fb team barcelona
```

Team names are matched against a local team/alias list, so common names like `barca`, `madrid`, `spurs`, `bayern`, etc. work too.

### Favorite team

Save a team:

```bash
fb set-team barcelona
```

or:

```bash
fb favorite barcelona
```

Then just run:

```bash
fb team
```

## Competitions

Currently configured:

| Competition      | Examples                                    |
| ---------------- | ------------------------------------------- |
| Premier League   | `pl`, `epl`, `premier`, `premierleague`     |
| La Liga          | `laliga`, `liga`, `pd`                      |
| Bundesliga       | `bundesliga`, `bl1`                         |
| Serie A          | `seriea`, `sa`                              |
| Ligue 1          | `ligue1`, `fl1`                             |
| Champions League | `cl`, `ucl`, `champions`, `championsleague` |

## Commands

```text
fb standings <league>
fb fixtures <league>
fb live
fb team [team]
fb set-team <team>
```

Some commands also have aliases:

```text
standings -> standing
team      -> myteam
set-team  -> favorite
```

### Reference project

I used [soccer-cli](https://github.com/architv/soccer-cli) as an inspiration for the general idea.

football-cli is my own implementation and does not copy code from the reference project.
