from typing import Any, Dict, List, Optional, Tuple


def get_event_rankings(
    event: str, mock_index: int
) -> Tuple[Dict[int, int], Optional[str]]:
    raise NotImplementedError


def get_matches(
    year: int, event: str, event_time: int, mock_index: int
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    raise NotImplementedError
