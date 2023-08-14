from typing import Any, Dict, List


def count_pieces_2019(
    location: str, height: str, piece: str, breakdown: Dict[str, Any]
) -> int:
    if piece not in ["Panel", "Cargo"]:
        raise ValueError("Piece must be hatch or cargo")

    if location == "bay":
        if piece == "Panel":
            count = 0
            for i in range(1, 9):
                final = breakdown[f"bay{i}"]
                if "Panel" in final:
                    if i in [4, 5]:
                        count += 1
                    else:
                        start = breakdown[f"preMatchBay{i}"]
                        if "Panel" not in start and "Unknown" not in start:
                            count += 1
            return count
        elif piece == "Cargo":
            return sum(
                [1 if "Cargo" in breakdown[f"bay{i}"] else 0 for i in range(1, 9)]
            )
    elif location == "rocket":
        return sum(
            [
                1 if piece in breakdown[f"{height}{x}"] else 0
                for x in [
                    "LeftRocketFar",
                    "LeftRocketNear",
                    "RightRocketFar",
                    "RightRocketNear",
                ]
            ]
        )
    else:
        raise ValueError("Location must be bay or rocket")

    return 0


def count_pieces_2023(
    auto: List[str], teleop: List[str], piece: str, target: str
) -> int:
    if target == "auto":
        return len([x for x, y in zip(auto, teleop) if x == piece and y != "None"])
    elif target == "teleop":
        return len([x for x, y in zip(auto, teleop) if x == "None" and y == piece])
    else:
        raise ValueError("Target must be auto or teleop")


def clean_breakdown(
    year: int, key: str, data: Dict[str, Any], total_points: int
) -> Dict[str, Any]:
    # Shared
    foul_points = data.get("foulPoints", 0)
    total_points = total_points
    no_foul_points = total_points - foul_points
    rp_1 = 0
    rp_2 = 0

    adjust_points = data.get("adjustPoints", 0)
    if adjust_points != 0:
        foul_points += adjust_points  # count adjust points as foul points
        no_foul_points -= adjust_points

    out = {
        "foul_points": foul_points,
        "total_points": total_points,
        "no_foul_points": no_foul_points,
        "rp_1": rp_1,
        "rp_2": rp_2,
    }

    if year == 2016:
        auto_reach_points = data["autoReachPoints"]
        auto_crossing_points = data["autoCrossingPoints"]
        auto_low_boulders = data["autoBouldersLow"]
        auto_high_boulders = data["autoBouldersHigh"]

        teleop_crossing_points = data["teleopCrossingPoints"]
        teleop_low_boulders = data["teleopBouldersLow"]
        teleop_high_boulders = data["teleopBouldersHigh"]

        challenge_points = data["teleopChallengePoints"]
        scale_points = data["teleopScalePoints"]

        all_endgame_robots = (
            data["teleopChallengePoints"] // 5 + data["teleopScalePoints"] // 15
        ) == 3

        auto_points = (
            auto_reach_points
            + auto_crossing_points
            + 5 * auto_low_boulders
            + 10 * auto_high_boulders
        )
        teleop_points = (
            teleop_crossing_points + 2 * teleop_low_boulders + 5 * teleop_high_boulders
        )
        endgame_points = challenge_points + scale_points

        rp_1 = int(data.get("teleopDefensesBreached", 0))
        rp_2 = int(data.get("teleopTowerCaptured", 0))

        rp_1_points = data["breachPoints"]
        rp_2_points = data["capturePoints"]
        no_foul_points -= rp_1_points + rp_2_points

        if key not in ["2016capl_f1m1", "2016milsu_qf4m1", "2016mndu2_f1m2"]:
            assert auto_points + teleop_points + endgame_points == no_foul_points

        out["auto_reach_points"] = auto_reach_points
        out["auto_crossing_points"] = auto_crossing_points
        out["auto_low_boulders"] = auto_low_boulders
        out["auto_high_boulders"] = auto_high_boulders
        out["teleop_crossing_points"] = teleop_crossing_points
        out["teleop_low_boulders"] = teleop_low_boulders
        out["teleop_high_boulders"] = teleop_high_boulders
        out["challenge_points"] = challenge_points
        out["scale_points"] = scale_points
        out["all_endgame_robots"] = all_endgame_robots
        out["no_foul_points"] = no_foul_points

        out["rp_1"] = rp_1
        out["rp_2"] = rp_2

    elif year == 2017:
        auto_mobility_points = data["autoMobilityPoints"]

        auto_fuel_low = data["autoFuelLow"]
        auto_fuel_high = data["autoFuelHigh"]
        auto_rotor_points = data["autoRotorPoints"]

        teleop_fuel_low = data["teleopFuelLow"]
        teleop_fuel_high = data["teleopFuelHigh"]
        teleop_rotor_points = data["teleopRotorPoints"]

        num_auto_rotors = auto_rotor_points // 60
        auto_rotor_points -= num_auto_rotors * 40
        teleop_rotor_points += num_auto_rotors * 40

        takeoff_points = data["teleopTakeoffPoints"]

        auto_kpa = 3 * auto_fuel_low + 9 * auto_fuel_high
        auto_points = auto_mobility_points + auto_kpa // 9 + auto_rotor_points

        teleop_kpa = auto_kpa % 9 + teleop_fuel_low + 3 * teleop_fuel_high
        teleop_points = teleop_kpa // 9 + teleop_rotor_points

        rp_1 = int(data.get("kPaRankingPointAchieved", 0))
        rp_2 = int(data.get("rotorRankingPointAchieved", 0))

        rp_1_points = data["kPaBonusPoints"]
        rp_2_points = data["rotorBonusPoints"]
        no_foul_points -= rp_1_points + rp_2_points

        assert auto_points + teleop_points + takeoff_points == no_foul_points

        out["auto_mobility_points"] = auto_mobility_points
        out["auto_fuel_low"] = auto_fuel_low
        out["auto_fuel_high"] = auto_fuel_high
        out["auto_rotor_points"] = auto_rotor_points
        out["teleop_fuel_low"] = teleop_fuel_low
        out["teleop_fuel_high"] = teleop_fuel_high
        out["teleop_rotor_points"] = teleop_rotor_points
        out["takeoff_points"] = takeoff_points
        out["no_foul_points"] = no_foul_points

        out["rp_1"] = rp_1
        out["rp_2"] = rp_2

    elif year == 2018:
        auto_run_points = data["autoRunPoints"]

        auto_switch_secs = data["autoSwitchOwnershipSec"]
        auto_scale_secs = data["autoScaleOwnershipSec"]

        teleop_switch_secs = (
            data["teleopSwitchOwnershipSec"] + data["teleopSwitchBoostSec"]
        )

        teleop_scale_secs = (
            data["teleopScaleOwnershipSec"] + data["teleopScaleBoostSec"]
        )

        vault_points = data["vaultPoints"]

        endgame_points = data["endgamePoints"]

        rp_1 = int(data.get("faceTheBossRankingPoint", 0))
        rp_2 = int(data.get("autoQuestRankingPoint", 0))

        error = no_foul_points - (
            auto_run_points
            + 2 * auto_switch_secs
            + 2 * auto_scale_secs
            + teleop_switch_secs
            + teleop_scale_secs
            + vault_points
            + endgame_points
        )

        if error != 0:
            if error * teleop_switch_secs > error * teleop_scale_secs:
                teleop_scale_secs += error
            else:
                teleop_switch_secs += error

        assert (
            auto_run_points
            + 2 * auto_switch_secs
            + 2 * auto_scale_secs
            + 1 * teleop_switch_secs
            + 1 * teleop_scale_secs
            + vault_points
            + endgame_points
            == no_foul_points
        )

        out["auto_run_points"] = auto_run_points
        out["auto_switch_secs"] = auto_switch_secs
        out["auto_scale_secs"] = auto_scale_secs
        out["teleop_switch_secs"] = teleop_switch_secs
        out["teleop_scale_secs"] = teleop_scale_secs
        out["vault_points"] = vault_points
        out["endgame_points"] = endgame_points

        out["rp_1"] = rp_1
        out["rp_2"] = rp_2

    elif year == 2019:
        sandstorm_points = data["sandStormBonusPoints"]

        bay_hatch = count_pieces_2019("bay", "any", "Panel", data)
        bay_cargo = count_pieces_2019("bay", "any", "Cargo", data)
        rocket_hatch_low = count_pieces_2019("rocket", "low", "Panel", data)
        rocket_hatch_mid = count_pieces_2019("rocket", "mid", "Panel", data)
        rocket_hatch_top = count_pieces_2019("rocket", "top", "Panel", data)
        rocket_cargo_low = count_pieces_2019("rocket", "low", "Cargo", data)
        rocket_cargo_mid = count_pieces_2019("rocket", "mid", "Cargo", data)
        rocket_cargo_top = count_pieces_2019("rocket", "top", "Cargo", data)

        hatch_points = 2 * (
            bay_hatch + rocket_hatch_low + rocket_hatch_mid + rocket_hatch_top
        )
        cargo_points = 3 * (
            bay_cargo + rocket_cargo_low + rocket_cargo_mid + rocket_cargo_top
        )

        hab_climb_points = data["habClimbPoints"]

        rp_1 = int(data.get("habDockingRankingPoint", 0))
        rp_2 = int(data.get("completeRocketRankingPoint", 0))

        assert (
            sandstorm_points + hatch_points + cargo_points + hab_climb_points
            == no_foul_points
        )

        out["sandstorm_points"] = sandstorm_points
        out["bay_hatch"] = bay_hatch
        out["bay_cargo"] = bay_cargo
        out["rocket_hatch_low"] = rocket_hatch_low
        out["rocket_hatch_mid"] = rocket_hatch_mid
        out["rocket_hatch_top"] = rocket_hatch_top
        out["rocket_cargo_low"] = rocket_cargo_low
        out["rocket_cargo_mid"] = rocket_cargo_mid
        out["rocket_cargo_top"] = rocket_cargo_top
        out["hab_climb_points"] = hab_climb_points

        out["rp_1"] = rp_1
        out["rp_2"] = rp_2

    elif year == 2020:
        auto_init_line_points = data["autoInitLinePoints"]
        auto_cells_bottom = data["autoCellsBottom"]
        auto_cells_outer = data["autoCellsOuter"]
        auto_cells_inner = data["autoCellsInner"]
        auto_cell_points = (
            2 * auto_cells_bottom + 4 * auto_cells_outer + 6 * auto_cells_inner
        )

        teleop_cells_bottom = data["teleopCellsBottom"]
        teleop_cells_outer = data["teleopCellsOuter"]
        teleop_cells_inner = data["teleopCellsInner"]
        teleop_cell_points = (
            1 * teleop_cells_bottom + 2 * teleop_cells_outer + 3 * teleop_cells_inner
        )

        control_panel_points = data["controlPanelPoints"]

        endgame_points = data["endgamePoints"]

        rp_1 = int(data.get("shieldOperationalRankingPoint", 0))
        rp_2 = int(data.get("shieldEnergizedRankingPoint", 0))

        assert (
            auto_init_line_points
            + auto_cell_points
            + teleop_cell_points
            + control_panel_points
            + endgame_points
            == no_foul_points
        )

        out["auto_init_line_points"] = auto_init_line_points
        out["auto_cells_bottom"] = auto_cells_bottom
        out["auto_cells_outer"] = auto_cells_outer
        out["auto_cells_inner"] = auto_cells_inner
        out["teleop_cells_bottom"] = teleop_cells_bottom
        out["teleop_cells_outer"] = teleop_cells_outer
        out["teleop_cells_inner"] = teleop_cells_inner
        out["control_panel_points"] = control_panel_points
        out["endgame_points"] = endgame_points

        out["rp_1"] = rp_1
        out["rp_2"] = rp_2

    if year == 2021:
        pass

    if year == 2022:
        auto_taxi_points = data["autoTaxiPoints"]
        auto_cargo_lower = (
            data["autoCargoLowerBlue"]
            + data["autoCargoLowerFar"]
            + data["autoCargoLowerNear"]
            + data["autoCargoLowerRed"]
        )
        auto_cargo_upper = (
            data["autoCargoUpperBlue"]
            + data["autoCargoUpperFar"]
            + data["autoCargoUpperNear"]
            + data["autoCargoUpperRed"]
        )

        # correct sensor issues
        initial_auto_cargo = 2 * auto_cargo_lower + 4 * auto_cargo_upper
        actual_auto_cargo_points = data["autoCargoPoints"]
        auto_cargo_error = actual_auto_cargo_points - initial_auto_cargo
        if initial_auto_cargo != actual_auto_cargo_points:
            if auto_cargo_lower > auto_cargo_upper:
                auto_cargo_lower += auto_cargo_error / 2
            else:
                auto_cargo_upper += auto_cargo_error / 4

        auto_cargo_points = 2 * auto_cargo_lower + 4 * auto_cargo_upper

        teleop_cargo_lower = (
            data["teleopCargoLowerBlue"]
            + data["teleopCargoLowerFar"]
            + data["teleopCargoLowerNear"]
            + data["teleopCargoLowerRed"]
        )
        teleop_cargo_upper = (
            data["teleopCargoUpperBlue"]
            + data["teleopCargoUpperFar"]
            + data["teleopCargoUpperNear"]
            + data["teleopCargoUpperRed"]
        )

        # correct sensor issues
        initial_teleop_cargo = 1 * teleop_cargo_lower + 2 * teleop_cargo_upper
        actual_teleop_cargo_points = data["teleopCargoPoints"]
        teleop_cargo_error = actual_teleop_cargo_points - initial_teleop_cargo
        if teleop_cargo_error != 0:
            if teleop_cargo_lower > teleop_cargo_upper:
                teleop_cargo_lower += teleop_cargo_error / 1
            else:
                teleop_cargo_upper += teleop_cargo_error / 2

        teleop_cargo_points = 1 * teleop_cargo_lower + 2 * teleop_cargo_upper

        endgame_points = data["endgamePoints"]

        rp_1 = int(data.get("cargoBonusRankingPoint", 0))
        rp_2 = int(data.get("hangarBonusRankingPoint", 0))

        assert (
            auto_taxi_points + auto_cargo_points + teleop_cargo_points + endgame_points
            == no_foul_points
        )

        out["auto_taxi_points"] = auto_taxi_points
        out["auto_cargo_lower"] = auto_cargo_lower
        out["auto_cargo_upper"] = auto_cargo_upper
        out["teleop_cargo_lower"] = teleop_cargo_lower
        out["teleop_cargo_upper"] = teleop_cargo_upper
        out["endgame_points"] = endgame_points

        out["rp_1"] = rp_1
        out["rp_2"] = rp_2

    elif year == 2023:
        auto_charge_station_points = data["autoChargeStationPoints"]

        auto_com = data["autoCommunity"]
        teleop_com = data["teleopCommunity"]

        alcu = count_pieces_2023(auto_com["B"], teleop_com["B"], "Cube", "auto")
        alco = count_pieces_2023(auto_com["B"], teleop_com["B"], "Cone", "auto")
        amcu = count_pieces_2023(auto_com["M"], teleop_com["M"], "Cube", "auto")
        amco = count_pieces_2023(auto_com["M"], teleop_com["M"], "Cone", "auto")
        ahcu = count_pieces_2023(auto_com["T"], teleop_com["T"], "Cube", "auto")
        ahco = count_pieces_2023(auto_com["T"], teleop_com["T"], "Cone", "auto")
        auto_points = 3 * (alcu + alco) + 4 * (amcu + amco) + 6 * (ahcu + ahco)

        auto_mobility_points = data["autoMobilityPoints"]

        tlcu = count_pieces_2023(auto_com["B"], teleop_com["B"], "Cube", "teleop")
        tlco = count_pieces_2023(auto_com["B"], teleop_com["B"], "Cone", "teleop")
        tmcu = count_pieces_2023(auto_com["M"], teleop_com["M"], "Cube", "teleop")
        tmco = count_pieces_2023(auto_com["M"], teleop_com["M"], "Cone", "teleop")
        thcu = count_pieces_2023(auto_com["T"], teleop_com["T"], "Cube", "teleop")
        thco = count_pieces_2023(auto_com["T"], teleop_com["T"], "Cone", "teleop")

        sc = 0
        if data["teleopGamePieceCount"] == 27:
            sc = data.get("extraGamePieceCount", 0)

        teleop_points = 2 * (tlcu + tlco) + 3 * (tmcu + tmco + sc) + 5 * (thcu + thco)

        links = len(data["links"])
        link_points = 5 * links

        endgame_charge_station_points = data["endGameChargeStationPoints"]
        endgame_park_points = data["endGameParkPoints"]

        rp_1 = int(data.get("sustainabilityBonusAchieved", 0))
        rp_2 = int(data.get("activationBonusAchieved", 0))

        assert (
            auto_mobility_points
            + auto_charge_station_points
            + auto_points
            + teleop_points
            + link_points
            + endgame_charge_station_points
            + endgame_park_points
            == no_foul_points
        )

        out["auto_low_cubes"] = alcu
        out["auto_low_cones"] = alco
        out["auto_mid_cubes"] = amcu
        out["auto_mid_cones"] = amco
        out["auto_high_cubes"] = ahcu
        out["auto_high_cones"] = ahco
        out["auto_charge_station_points"] = auto_charge_station_points
        out["auto_mobility_points"] = auto_mobility_points

        out["teleop_low_cubes"] = tlcu
        out["teleop_low_cones"] = tlco
        out["teleop_mid_cubes"] = tmcu + sc
        out["teleop_mid_cones"] = tmco
        out["teleop_high_cubes"] = thcu
        out["teleop_high_cones"] = thco
        out["links"] = links

        out["endgame_charge_station_points"] = endgame_charge_station_points
        out["endgame_park_points"] = endgame_park_points

        out["rp_1"] = rp_1
        out["rp_2"] = rp_2

    return out
