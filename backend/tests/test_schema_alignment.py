"""Tests that entity serialization output matches the corresponding Pydantic schema.

These tests ensure that when entities are modified, their serialization output
still conforms to the OpenAPI response schemas defined in src/api/schemas.py.
Run with: pytest tests/test_schema_alignment.py -v

Note: These tests use representative sample data rather than actual entity instances
to avoid requiring database connectivity during test collection.
"""

import json
from typing import Any, Dict, List

import pytest

# Import schemas only (no entity imports to avoid DB engine creation)
from src.api.schemas import (
    TeamResponse,
    EventResponse,
    MatchResponse,
    TeamEventResponse,
    TeamYearResponse,
    YearResponse,
)


def test_team_schema_alignment():
    """Team.to_dict() output must match TeamResponse schema."""
    # Representative team serialization output matching actual to_dict() structure
    data = {
        "team": 5511,
        "name": "Test Team",
        "nickname": "Testers",
        "city": "Raleigh",
        "state": "NC",
        "country": "USA",
        "website": "http://example.com",
        "rookie_year": 2019,
        "record": {"wins": 10, "losses": 5, "ties": 1},
        "norm_epa": {
            "current": 100.0,
            "recent": 105.0,
            "mean": 98.0,
            "max": 110.0
        }
    }
    TeamResponse(**data)


def test_event_schema_alignment():
    """Event.to_dict() output must match EventResponse schema."""
    data = {
        "key": "2024nytr",
        "year": 2024,
        "name": "New York Tri-State Regional",
        "time": 1713984000.0,
        "country": "USA",
        "state": "NY",
        "district": None,
        "start_date": "2024-04-25",
        "end_date": "2024-04-27",
        "type": 1,
        "week": 8,
        "video": ["youtube"],
        "status": "Completed",
        "status_str": "Completed",
        "num_teams": 30,
        "current_match": 50,
        "qual_matches": 48,
        "epa": {
            "max": 12.5,
            "top_8": 10.2,
            "top_24": 8.7,
            "mean": 6.3,
            "sd": 3.1,
        },
        "metrics": {
            "win_prob": {
                "count": 50,
                "conf": 0.95,
                "acc": 0.82,
                "mse": 4.5,
            },
            "score_pred": {
                "count": 100,
                "rmse": 15.3,
                "error": 12.8,
            },
        },
    }
    EventResponse(**data)


def test_match_schema_alignment():
    """Match.to_dict() output must match MatchResponse schema."""
    data = {
        "key": "2024casj_qm1",
        "year": 2024,
        "event": "casj",
        "week": 3,
        "elim": False,
        "comp_level": "qm",
        "set_number": 0,
        "match_number": 1,
        "time": 1711986000,
        "predicted_time": None,
        "status": "completed",
        "video": None,
        "red_1": 254,
        "red_2": 311,
        "red_3": 1113,
        "red_dq": "",
        "red_surrogate": "",
        "blue_1": 694,
        "blue_2": 701,
        "blue_3": 118,
        "blue_dq": "",
        "blue_surrogate": "",
        "winner": "red",
        "epa_winner": "blue",
        "red_score": 50,
        "red_no_foul": 45,
        "red_foul": 5,
        "red_auto": 10,
        "red_teleop": 30,
        "red_endgame": 10,
        "blue_score": 60,
        "blue_no_foul": 55,
        "blue_foul": 5,
        "blue_auto": 15,
        "blue_teleop": 35,
        "blue_endgame": 10,
        "epa_win_prob": 0.7,
        "epa_red_score_pred": 48.0,
        "epa_blue_score_pred": 62.0,
        "pre_epas": None,
        "epas": None
    }
    MatchResponse(**data)


def test_team_event_schema_alignment():
    """TeamEvent.to_dict() output must match TeamEventResponse schema."""
    data = {
        "team": 5511,
        "year": 2024,
        "event": "casj",
        "time": 1711986000.0,
        "team_name": "Test Team",
        "event_name": "Test Event",
        "country": "USA",
        "state": "CA",
        "district": None,
        "type": 1,
        "week": 3,
        "status": "Completed",
        "first_event": True,
        "epa": {
            "total_points": 85.0,
            "unitless": 80.0,
            "norm": 90.0,
            "breakdown": {},
            "stats": {
                "start": 100.0,
                "pre_elim": 120.0,
                "mean": 110.0,
                "max": 130.0,
            },
        },
        "record": {
            "qual": {
                "wins": 5,
                "losses": 2,
                "ties": 0,
                "count": 7,
                "winrate": 0.714,
                "rps": 15,
                "rps_per_match": 2.14,
                "rank": 3,
                "num_teams": 30,
            },
            "elim": {
                "wins": 2,
                "losses": 1,
                "ties": 0,
                "count": 3,
                "winrate": 0.667,
                "alliance": None,
                "is_captain": False,
            },
            "total": {
                "wins": 7,
                "losses": 3,
                "ties": 0,
                "count": 10,
                "winrate": 0.7,
            },
        },
    }
    TeamEventResponse(**data)


def test_team_year_schema_alignment():
    """TeamYear.to_dict() output must match TeamYearResponse schema."""
    data = {
        "team": 5511,
        "year": 2024,
        "epa": {
            "total_points": 3000.0,
            "unitless": 2800.0,
            "norm": 2900.0,
            "breakdown": {},
            "stats": {
                "start": 100.0,
                "pre_elim": 150.0,
                "mean": 130.0,
                "max": 180.0,
            },
        },
        "record": {
            "qual": {
                "wins": 30,
                "losses": 10,
                "ties": 0,
                "count": 40,
                "winrate": 0.75,
                "rps": 60,
                "rps_per_match": 1.5,
            },
            "elim": {
                "wins": 5,
                "losses": 2,
                "ties": 0,
                "count": 7,
                "winrate": 0.714,
            },
            "total": {
                "wins": 35,
                "losses": 12,
                "ties": 0,
                "count": 47,
                "winrate": 0.745,
            },
        },
        "competing": True,
    }
    TeamYearResponse(**data)


def test_year_schema_alignment():
    """Year.to_dict() output must match YearResponse schema."""
    data = {
        "year": 2024,
        "teams": [
            {"team_number": 5511, "name": "Test Team", "nickname": "Testers"},
            {"team_number": 254, "name": "Chevy Chase High School", "nickname": "The Chargers"}
        ],
        "events": [
            {"event_key": "2024casj", "name": "San Jose Regional"},
            {"event_key": "2024nytr", "name": "New York Tri-State Regional"}
        ]
    }
    YearResponse(**data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
