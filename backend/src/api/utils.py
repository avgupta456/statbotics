from typing import Any, Dict

from src.db.models.match import Match


def unpack_match(m: Match) -> Dict[str, Any]:
    return {
        "time": m.time,
        "key": m.key,
        "comp_level": m.comp_level,
        "set_number": m.set_number,
        "match_number": m.match_number,
        "playoff": m.playoff,
        "red": m.get_red(),
        "blue": m.get_blue(),
        "red_score": m.red_score,
        "blue_score": m.blue_score,
        "winner": m.winner,
        "red_rp_1": m.red_rp_1,
        "red_rp_2": m.red_rp_2,
        "blue_rp_1": m.blue_rp_1,
        "blue_rp_2": m.blue_rp_2,
        "red_epa_pred": m.red_epa_sum,
        "blue_epa_pred": m.blue_epa_sum,
        "red_rp_1_pred": m.red_rp_1_epa_sum,
        "red_rp_2_pred": m.red_rp_2_epa_sum,
        "epa_win_prob": m.epa_win_prob,
        "pred_winner": m.epa_winner,
        "blue_rp_1_pred": m.blue_rp_1_epa_sum,
        "blue_rp_2_pred": m.blue_rp_2_epa_sum,
        # for simulation
        "red_auto": m.red_auto,
        "red_teleop": m.red_teleop,
        "red_endgame": m.red_endgame,
        "red_1": (m.red_auto_1 or 0) + (m.red_teleop_1 or 0),
        "red_2": (m.red_auto_2 or 0) + (m.red_teleop_2 or 0),
        "blue_auto": m.blue_auto,
        "blue_teleop": m.blue_teleop,
        "blue_endgame": m.blue_endgame,
        "blue_1": (m.blue_auto_1 or 0) + (m.blue_teleop_1 or 0),
        "blue_2": (m.blue_auto_2 or 0) + (m.blue_teleop_2 or 0),
    }
