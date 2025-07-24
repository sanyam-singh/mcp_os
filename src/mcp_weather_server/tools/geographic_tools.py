"""
This module contains tools for geographic operations.
"""

async def list_villages(state: str, district: str = None):
    """
    Returns a list of villages for a given state and optional district.
    """
    # Mock data
    if state.lower() == 'bihar':
        if district and district.lower() == 'patna':
            return {"villages": ["Patna", "Danapur", "Masaurhi"]}
        return {"districts": ["Patna", "Gaya", "Muzaffarpur"]}
    return {"error": "State not found"}

async def reverse_geocode(location_name: str):
    """
    Returns the coordinates for a given location name.
    """
    # Mock data
    locations = {
        "patna": {"latitude": 25.5941, "longitude": 85.1376},
        "gaya": {"latitude": 24.7971, "longitude": 84.9969},
        "muzaffarpur": {"latitude": 26.1214, "longitude": 85.3932},
    }
    return locations.get(location_name.lower(), {"error": "Location not found"})

async def get_administrative_bounds(village_id: str):
    """
    Returns the geographic boundaries for a given village ID.
    """
    # Mock data
    boundaries = {
        "patna": {"type": "Polygon", "coordinates": [[[85.0, 25.5], [85.2, 25.5], [85.2, 25.7], [85.0, 25.7], [85.0, 25.5]]]},
    }
    return boundaries.get(village_id.lower(), {"error": "Village ID not found"})
