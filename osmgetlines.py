# --- START OF FILE osmgetlines.py ---

import numpy as np
from typing import Dict, List, Any

def osmgetlines(map_data: Dict, way_indices: List[int]) -> np.ndarray:
    """
    Extract lines from selected map ways for plotting.

    Args:
        map_data (Dict): The map data structure from loadosm.
        way_indices (List[int]): A list of indices of the ways to extract.

    Returns:
        np.ndarray: A 2xM array of points, with NaN values separating
                    different lines.
    """
    if not way_indices:
        return np.empty((2, 0))

    lines_to_join = []
    nan_separator = np.full((2, 1), np.nan)

    for i in way_indices:
        way = map_data['ways'][i]
        if 'points' in way and way['points'].shape[1] > 0:
            lines_to_join.append(way['points'])
            lines_to_join.append(nan_separator)

    if not lines_to_join:
        return np.empty((2, 0))
        
    # Remove the last unnecessary NaN separator
    lines_to_join.pop()
    
    return np.hstack(lines_to_join)