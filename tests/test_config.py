import pytest

from config import get_team


# tests team names and their common aliases
@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Arsenal", {"id": 57, "shortName": "Arsenal"}),
        ("barca", {"id": 81, "shortName": "Barça"}),
        ("FC Barcelona", {"id": 81, "shortName": "Barça"}),
        ("Bayern Munich", {"id": 5, "shortName": "Bayern"}),
        ("real madrid", {"id": 86, "shortName": "Real Madrid"}),
        ("BVB", {"id": 4, "shortName": "Dortmund"}),
    ],
)
def test_get_team_names_and_aliases(name, expected):
    assert get_team(name) == expected


# tests partial team names when no direct alias exists
@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("leverk", {"id": 3, "shortName": "Leverkusen"}),
        ("totten", {"id": 73, "shortName": "Tottenham"}),
    ],
)
def test_get_team_partial_names(name, expected):
    assert get_team(name) == expected


# avoids returning the wrong team for an unclear search
@pytest.mark.parametrize("name", ["man", "uni"])
def test_get_team_ambiguous_names(name):
    assert get_team(name) is None


# rejects empty or unknown team names
@pytest.mark.parametrize("name", ["", "   ", "!?", "Atlantis FC"])
def test_get_team_invalid_names(name):
    assert get_team(name) is None
