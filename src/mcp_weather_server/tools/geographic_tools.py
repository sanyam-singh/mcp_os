"""
This module contains tools for geographic operations.
"""

# Expanded mock data for Bihar: All districts, several villages/towns each
BIHAR_DATA = {
    "Araria": ["Araria", "Forbesganj", "Jokihat", "Raniganj"],
    "Arwal": ["Arwal", "Kaler", "Karpi", "Kurtha"],
    "Aurangabad": ["Aurangabad", "Daudnagar", "Obra", "Nabinagar"],
    "Banka": ["Banka", "Amarpur", "Barahat", "Belhar"],
    "Begusarai": ["Begusarai", "Bakhri", "Barauni", "Teghra"],
    "Bhagalpur": ["Bhagalpur", "Sabour", "Nathnagar", "Kahalgaon"],
    "Bhojpur": ["Arrah", "Jagdishpur", "Piro", "Shahpur"],
    "Buxar": ["Buxar", "Dumraon", "Chausa", "Simri"],
    "Darbhanga": ["Darbhanga", "Baheri", "Jale", "Benipur"],
    "East Champaran": ["Motihari", "Raxaul", "Chakia", "Dhaka"],
    "Gaya": ["Gaya", "Bodh Gaya", "Tekari", "Sherghati"],
    "Gopalganj": ["Gopalganj", "Barauli", "Baikunthpur", "Kateya"],
    "Jamui": ["Jamui", "Jhajha", "Sikandra", "Sono"],
    "Jehanabad": ["Jehanabad", "Ghoshi", "Makhdumpur", "Modanganj"],
    "Kaimur": ["Bhabua", "Mohania", "Ramgarh", "Chainpur"],
    "Katihar": ["Katihar", "Barsoi", "Manihari", "Pranpur"],
    "Khagaria": ["Khagaria", "Gogri", "Mansi", "Alauli"],
    "Kishanganj": ["Kishanganj", "Bahadurganj", "Thakurganj", "Kochadhaman"],
    "Lakhisarai": ["Lakhisarai", "Barahiya", "Halsi", "Surajgarha"],
    "Madhepura": ["Madhepura", "Bihariganj", "Murliganj", "Udakishunganj"],
    "Madhubani": ["Madhubani", "Jhanjharpur", "Benipatti", "Phulparas"],
    "Munger": ["Munger", "Jamalpur", "Kharagpur", "Tarapur"],
    "Muzaffarpur": ["Muzaffarpur", "Motipur", "Kanti", "Saraiya"],
    "Nalanda": ["Bihar Sharif", "Rajgir", "Hilsa", "Islampur"],
    "Nawada": ["Nawada", "Rajauli", "Hisua", "Warsaliganj"],
    "Patna": ["Patna", "Danapur", "Masaurhi", "Phulwari", "Barh"],
    "Purnia": ["Purnia", "Banmankhi", "Dhamdaha", "Baisi"],
    "Rohtas": ["Sasaram", "Dehri", "Bikramganj", "Nokha"],
    "Saharsa": ["Saharsa", "Simri Bakhtiyarpur", "Salkhua", "Sonbarsa"],
    "Samastipur": ["Samastipur", "Rosera", "Dalsinghsarai", "Patori"],
    "Saran": ["Chhapra", "Marhaura", "Dariapur", "Amnour"],
    "Sheikhpura": ["Sheikhpura", "Barbigha", "Chewara", "Ghatkusumbha"],
    "Sheohar": ["Sheohar", "Piprahi", "Tariyani", "Dumri Katsari"],
    "Sitamarhi": ["Sitamarhi", "Bairgania", "Belsand", "Parihar"],
    "Siwan": ["Siwan", "Maharajganj", "Goriakothi", "Barharia"],
    "Supaul": ["Supaul", "Birpur", "Triveniganj", "Nirmali"],
    "Vaishali": ["Hajipur", "Mahnar", "Lalganj", "Raghopur"],
    "West Champaran": ["Bettiah", "Bagaha", "Narkatiaganj", "Ramnagar"],
}

# Expanded mock coordinates (one per main town/village)
locations = {
    "patna": {"latitude": 25.5941, "longitude": 85.1376},
    "danapur": {"latitude": 25.6394, "longitude": 85.0456},
    "masaurhi": {"latitude": 25.3532, "longitude": 85.0312},
    "phulwari": {"latitude": 25.5587, "longitude": 85.0487},
    "barh": {"latitude": 25.4846, "longitude": 85.7096},
    "gaya": {"latitude": 24.7971, "longitude": 84.9969},
    "bodh gaya": {"latitude": 24.6951, "longitude": 84.9914},
    "muzaffarpur": {"latitude": 26.1214, "longitude": 85.3932},
    "motihari": {"latitude": 26.6486, "longitude": 84.9166},
    "bhagalpur": {"latitude": 25.3476, "longitude": 86.9824},
    "darbhanga": {"latitude": 26.1527, "longitude": 85.8970},
    "purnia": {"latitude": 25.7771, "longitude": 87.4753},
    "sasaram": {"latitude": 24.9500, "longitude": 84.0300},
    "hajipur": {"latitude": 25.6850, "longitude": 85.2098},
    "chhapra": {"latitude": 25.7800, "longitude": 84.7300},
    "bettiah": {"latitude": 26.8022, "longitude": 84.5036},
    "araria": {"latitude": 26.1500, "longitude": 87.5167},
    "buxar": {"latitude": 25.5647, "longitude": 83.9777},
    "katihar": {"latitude": 25.5385, "longitude": 87.5750},
    "madhepura": {"latitude": 25.9210, "longitude": 86.7927},
    "samastipur": {"latitude": 25.8600, "longitude": 85.7810},
    "siwan": {"latitude": 26.2215, "longitude": 84.3588},
    "supaul": {"latitude": 26.1167, "longitude": 86.6000},
    "jamui": {"latitude": 24.9200, "longitude": 86.2200},
    "nalanda": {"latitude": 25.1357, "longitude": 85.4432},
    "munger": {"latitude": 25.3810, "longitude": 86.4651},
    "rohtas": {"latitude": 24.9436, "longitude": 84.1296},
    "aurangabad": {"latitude": 24.7500, "longitude": 84.3700},
    "gopalganj": {"latitude": 26.4680, "longitude": 84.4330},
    "kaimur": {"latitude": 25.0500, "longitude": 83.6000},
    "lakhisarai": {"latitude": 25.1700, "longitude": 86.1000},
    "nawada": {"latitude": 24.8839, "longitude": 85.5436},
    "sheikhpura": {"latitude": 25.1400, "longitude": 85.8500},
    "sheohar": {"latitude": 26.5200, "longitude": 85.3000},
    "sitamarhi": {"latitude": 26.6000, "longitude": 85.4830},
    "vaishali": {"latitude": 25.6900, "longitude": 85.2200},
    # Add more as needed
}

boundaries = {
    "patna": {"type": "Polygon", "coordinates": [[[85.0, 25.5], [85.2, 25.5], [85.2, 25.7], [85.0, 25.7], [85.0, 25.5]]]},
    "gaya": {"type": "Polygon", "coordinates": [[[84.9, 24.7], [85.0, 24.7], [85.0, 24.8], [84.9, 24.8], [84.9, 24.7]]]},
    "muzaffarpur": {"type": "Polygon", "coordinates": [[[85.3, 26.0], [85.5, 26.0], [85.5, 26.2], [85.3, 26.2], [85.3, 26.0]]]},
    "bhagalpur": {"type": "Polygon", "coordinates": [[[86.9, 25.3], [87.0, 25.3], [87.0, 25.4], [86.9, 25.4], [86.9, 25.3]]]},
    "darbhanga": {"type": "Polygon", "coordinates": [[[85.8, 26.1], [86.0, 26.1], [86.0, 26.3], [85.8, 26.3], [85.8, 26.1]]]},
    "purnia": {"type": "Polygon", "coordinates": [[[87.4, 25.7], [87.6, 25.7], [87.6, 25.9], [87.4, 25.9], [87.4, 25.7]]]},
    # Add more as needed
}

async def list_villages(state: str, district: str = None):
    """
    Returns a list of villages for a given state and optional district.
    """
    if state.lower() == 'bihar':
        if district:
            villages = BIHAR_DATA.get(district.title())
            if villages:
                return {"villages": villages}
            else:
                return {"error": "District not found"}
        return {"districts": list(BIHAR_DATA.keys())}
    return {"error": "State not found"}

async def reverse_geocode(location_name: str):
    """
    Returns the coordinates for a given location name.
    """
    return locations.get(location_name.lower(), {"error": "Location not found"})

async def get_administrative_bounds(village_id: str):
    """
    Returns the geographic boundaries for a given village ID.
    """
    return boundaries.get(village_id.lower(), {"error": "Village ID not found"})