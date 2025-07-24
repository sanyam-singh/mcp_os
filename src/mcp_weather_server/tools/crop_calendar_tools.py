"""
This module contains tools for crop calendar operations.
"""
from datetime import date

async def get_crop_calendar(region: str, crop_type: str = None):
    """
    Returns the crop calendar for a given region and optional crop type.
    """
    # Mock data
    if region.lower() == 'bihar':
        if crop_type and crop_type.lower() == 'rice':
            return {"crop": "rice", "planting": "June-July", "harvesting": "October-November"}
        return {"crops": ["rice", "wheat", "maize"]}
    return {"error": "Region not found"}

async def get_prominent_crops(region: str, season: str):
    """
    Returns the prominent crops for a given region and season.
    """
    # Mock data
    if region.lower() == 'bihar':
        if season.lower() == 'kharif':
            return {"crops": ["rice", "maize"]}
        elif season.lower() == 'rabi':
            return {"crops": ["wheat", "barley"]}
    return {"error": "Region or season not found"}

async def estimate_crop_stage(crop: str, plant_date: str, current_date: str):
    """
    Estimates the growth stage of a crop.
    """
    # Mock data
    plant_date = date.fromisoformat(plant_date)
    current_date = date.fromisoformat(current_date)
    days_since_planting = (current_date - plant_date).days

    if crop.lower() == 'rice':
        if days_since_planting <= 30:
            return {"stage": "vegetative"}
        elif days_since_planting < 60:
            return {"stage": "flowering"}
        else:
            return {"stage": "maturity"}
    return {"error": "Crop not found"}
