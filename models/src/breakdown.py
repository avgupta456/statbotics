from typing import Any, Dict, List


def clean_breakdown(year: int, key: str, data: Dict[str, Any]) -> Dict[str, Any]:
    if year < 2016:
        return {}

    # Shared
    foul_points = data["foulPoints"]
    total_points = data["totalPoints"]
    no_foul_points = total_points - foul_points

    out = {
        "foul_points": foul_points,
        "total_points": total_points,
        "no_foul_points": no_foul_points,
    }

    if year == 2023:

        def count_pieces(
            auto: List[str], teleop: List[str], piece: str, target: str
        ) -> int:
            if target == "auto":
                return len(
                    [x for x, y in zip(auto, teleop) if x == piece and y != "None"]
                )
            elif target == "teleop":
                return len(
                    [x for x, y in zip(auto, teleop) if x != piece and y == piece]
                )
            else:
                raise ValueError("Target must be auto or teleop")

        auto_charge_station_points = data["autoChargeStationPoints"]
        auto_charge_station_robots = [0, 0, 0]
        if data["autoChargeStationRobot1"] == "Docked":
            auto_charge_station_robots[0] = auto_charge_station_points
        elif data["autoChargeStationRobot2"] == "Docked":
            auto_charge_station_robots[1] = auto_charge_station_points
        elif data["autoChargeStationRobot3"] == "Docked":
            auto_charge_station_robots[2] = auto_charge_station_points

        auto_com = data["autoCommunity"]
        teleop_com = data["teleopCommunity"]

        auto_low_cubes = count_pieces(auto_com["B"], teleop_com["B"], "Cube", "auto")
        auto_low_cones = count_pieces(auto_com["B"], teleop_com["B"], "Cone", "auto")
        auto_mid_cubes = count_pieces(auto_com["M"], teleop_com["M"], "Cube", "auto")
        auto_mid_cones = count_pieces(auto_com["M"], teleop_com["M"], "Cone", "auto")
        auto_high_cubes = count_pieces(auto_com["T"], teleop_com["T"], "Cube", "auto")
        auto_high_cones = count_pieces(auto_com["T"], teleop_com["T"], "Cone", "auto")

        auto_cubes = auto_low_cubes + auto_mid_cubes + auto_high_cubes
        auto_cones = auto_low_cones + auto_mid_cones + auto_high_cones
        auto_low = auto_low_cubes + auto_low_cones
        auto_mid = auto_mid_cubes + auto_mid_cones
        auto_high = auto_high_cubes + auto_high_cones
        auto_pieces = auto_cubes + auto_cones
        auto_points = 3 * auto_low + 4 * auto_mid + 6 * auto_high
        auto_mobility_points = data["autoMobilityPoints"]
        auto_mobility_robots = [
            {"No": 0, "Yes": 3}[data[f"mobilityRobot{i}"]] for i in range(1, 4)
        ]

        assert sum(auto_charge_station_robots) == auto_charge_station_points
        assert auto_points == data["autoGamePiecePoints"]
        assert sum(auto_mobility_robots) == auto_mobility_points

        out["auto_charge_station_points"] = auto_charge_station_points
        out["auto_charge_station_robots"] = auto_charge_station_robots
        out["auto_low_cubes"] = auto_low_cubes
        out["auto_low_cones"] = auto_low_cones
        out["auto_mid_cubes"] = auto_mid_cubes
        out["auto_mid_cones"] = auto_mid_cones
        out["auto_high_cubes"] = auto_high_cubes
        out["auto_high_cones"] = auto_high_cones
        out["auto_cubes"] = auto_cubes
        out["auto_cones"] = auto_cones
        out["auto_low"] = auto_low
        out["auto_mid"] = auto_mid
        out["auto_high"] = auto_high
        out["auto_pieces"] = auto_pieces
        out["auto_points"] = auto_points
        out["auto_mobility_points"] = auto_mobility_points
        out["auto_mobility_robots"] = auto_mobility_robots

    return out
