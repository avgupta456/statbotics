from src.main import Statbotics

sb = Statbotics()

print(
    sb.get_teams(
        state="NC",
        metric="norm_epa_recent",
        ascending=False,
        limit=20,
        fields=["team", "norm_epa_recent"],
    )
)
