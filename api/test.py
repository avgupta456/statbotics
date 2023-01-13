from src.main import Statbotics

sb = Statbotics()

print(sb.get_team(5511))
print()

print(
    sb.get_teams(
        state="NC",
        metric="norm_epa_recent",
        ascending=False,
        limit=20,
        fields=["team", "norm_epa_recent"],
    )
)
print()

print(sb.get_year(2022))
print()

print(sb.get_years(metric="epa_acc", limit=10, fields=["year", "epa_acc", "epa_mse"]))
print()

print(sb.get_team_year(team=5511, year=2019))
print()

print(
    sb.get_team_years(
        state="CA",
        metric="norm_epa_end",
        limit=20,
        fields=["team", "year", "norm_epa_end"],
    )
)
print()

print(sb.get_event("2022carv"))
print()

print(
    sb.get_events(
        year=2022, type=3, metric="epa_acc", fields=["key", "epa_acc", "epa_mse"]
    )
)
print()

print(sb.get_team_event(team=5511, event="2019ncwak"))
print()

print(
    sb.get_team_events(
        team=5511, metric="winrate", limit=10, fields=["event", "winrate"]
    )
)
print()

print(sb.get_match("2019ncwak_f1m1"))
print()

print(
    sb.get_matches(
        year=2022,
        metric="red_epa_sum",  # or blue_epa_sum
        ascending=False,
        limit=10,
        fields=[
            "key",
            "red_1",
            "red_2",
            "red_3",
            "blue_1",
            "blue_2",
            "blue_3",
            "red_epa_sum",
            "blue_epa_sum",
        ],
    )
)
print()
