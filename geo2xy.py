# --- START OF FILE geo2xy.py ---

import numpy as np

def geo2xy(geo: np.ndarray) -> np.ndarray:
    """
    Convert (LAT,LON) pairs into XY pairs using the Web Mercator projection.

    Args:
        geo (np.ndarray): A 2xN numpy array where geo[0,:] is latitude
                          and geo[1,:] is longitude in degrees.

    Returns:
        np.ndarray: The projected 2xN XY coordinates, mapped to the
                    square [0, 256]x[0, 256]. The Y coordinate grows
                    from north to south to match pixel coordinates.
    """
    # Convert degrees to radians
    geo_rad = (np.pi / 180) * geo
    
    # Apply Web Mercator projection formula
    pi = np.pi
    lat_rad = geo_rad[0, :]
    lon_rad = geo_rad[1, :]
    
    x = pi + lon_rad
    y = pi - np.log(np.tan(pi / 4 + lat_rad / 2))
    
    xy = (128 / pi) * np.array([x, y])
    return xy