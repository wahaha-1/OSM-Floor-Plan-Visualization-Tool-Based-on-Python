# --- START OF FILE demo.py ---

import matplotlib.pyplot as plt
from loadosm import loadosm
from osmgetlines import osmgetlines
from geo2xy import geo2xy

def main():
    """
    Main script to load OSM data and plot it, mimicking the MATLAB demo.
    """
    # Load an OSM file as a Python dictionary
    print("Loading OSM file...")
    map_data = loadosm('map.osm')
    print("OSM file loaded.")

    # Find indices for highways, buildings, and other ways
    all_indices = range(len(map_data['ways']))
    hw_indices = [i for i in all_indices if map_data['ways'][i]['isHighway']]
    bl_indices = [i for i in all_indices if map_data['ways'][i]['isBuilding']]
    
    # Use sets for efficient difference calculation
    hw_set = set(hw_indices)
    bl_set = set(bl_indices)
    ot_indices = [i for i in all_indices if i not in hw_set and i not in bl_set]

    # --- Plotting ---
    print("Plotting data...")
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')

    # Plot highways
    if hw_indices:
        lines_hw = osmgetlines(map_data, hw_indices)
        xy_hw = geo2xy(lines_hw)
        ax.plot(xy_hw[0, :], xy_hw[1, :], 'b-', linewidth=1.5, label='highways')

    # Plot buildings
    if bl_indices:
        lines_bl = osmgetlines(map_data, bl_indices)
        xy_bl = geo2xy(lines_bl)
        ax.plot(xy_bl[0, :], xy_bl[1, :], 'g-', linewidth=0.75, label='building')

    # Plot other ways
    if ot_indices:
        lines_ot = osmgetlines(map_data, ot_indices)
        xy_ot = geo2xy(lines_ot)
        ax.plot(xy_ot[0, :], xy_ot[1, :], 'k-', linewidth=0.5, label='other')

    # Set axes properties to match MATLAB output
    ax.invert_yaxis()  # Equivalent to set(gca, 'ydir', 'reverse')
    ax.set_xlabel('Web Mercator X')
    ax.set_ylabel('Web Mercator Y')
    ax.set_title('OSM in Python (matplotlib)')
    ax.legend()

    plt.show()
    print("Plotting complete.")

if __name__ == '__main__':
    main()