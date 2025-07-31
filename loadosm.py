# --- START OF FILE loadosm.py ---

import xml.etree.ElementTree as ET
import numpy as np
from typing import Dict, List, Any

def loadosm(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Load an OSM file into a Python dictionary mimicking the MATLAB structure.

    Args:
        file_path (str): The path to the .osm file.

    Returns:
        Dict: A dictionary 'map_data' containing:
            - 'nodes': A list of node dictionaries {'id', 'lat', 'lon'}.
            - 'ways': A list of way dictionaries {'id', 'nds', 'tags', 
                      'points', 'isHighway', 'isBuilding', 'building_height'}.
    """
    print("Parsing XML file...")
    tree = ET.parse(file_path)
    root = tree.getroot()

    map_data = {'nodes': [], 'ways': []}
    
    # 1. First pass: Parse all nodes and ways into basic structures
    nodes_temp = {}
    for node_elem in root.findall('node'):
        node_id = int(node_elem.get('id'))
        nodes_temp[node_id] = {
            'id': node_id,
            'lat': float(node_elem.get('lat')),
            'lon': float(node_elem.get('lon'))
        }
    map_data['nodes'] = list(nodes_temp.values())

    for way_elem in root.findall('way'):
        way_dict = {
            'id': int(way_elem.get('id')),
            'nds': [int(nd.get('ref')) for nd in way_elem.findall('nd')],
            'tags': [[tag.get('k'), tag.get('v')] for tag in way_elem.findall('tag')]
        }
        map_data['ways'].append(way_dict)
    
    print(f"Found {len(map_data['nodes'])} nodes and {len(map_data['ways'])} ways.")
    
    # 2. Second pass: Add convenience fields to ways
    print("Adding convenience fields...")
    for way in map_data['ways']:
        # Add 'points'
        points = []
        for node_id in way['nds']:
            if node_id in nodes_temp:
                node = nodes_temp[node_id]
                points.append([node['lat'], node['lon']])
        
        if points:
            way['points'] = np.array(points).T  # Transpose to get 2xN shape
        else:
            way['points'] = np.empty((2, 0))

        # Add boolean flags
        tags_dict = {tag[0]: tag[1] for tag in way['tags']}
        way['isHighway'] = 'highway' in tags_dict
        way['isBuilding'] = 'building' in tags_dict

        # Add 'building_height'
        AVERAGE_LEVEL_HEIGHT = 3
        DEFAULT_BUILDING_HEIGHT = 5
        way['building_height'] = 0
        
        if way['isBuilding']:
            way['building_height'] = DEFAULT_BUILDING_HEIGHT
            
            # Try to find 'height' tag
            if 'height' in tags_dict:
                try:
                    way['building_height'] = float(tags_dict['height'])
                except (ValueError, TypeError):
                    pass # Keep default if conversion fails
            # Else, try to find 'building:levels'
            elif 'building:levels' in tags_dict:
                try:
                    way['building_height'] = float(tags_dict['building:levels']) * AVERAGE_LEVEL_HEIGHT
                except (ValueError, TypeError):
                    pass

    return map_data