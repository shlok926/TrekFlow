# src/core/sustainability.py
import math

# Carbon emission factors in grams of CO2 per passenger-kilometer (g CO2 / p-km)
CARBON_FACTORS = {
    "Flight ✈️": 150.0,
    "Cab/Car 🚗": 120.0,
    "Bus 🚌": 40.0,
    "Train 🚆": 15.0
}

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two points on the Earth's surface
    using the Haversine formula (returns distance in km).
    """
    R = 6371.0  # Earth's radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_carbon_footprint(start_lat, start_lon, dest_lat, dest_lon, transport_mode, num_people=1):
    """
    Calculates carbon footprint (kg CO2) and Eco-Karma points.
    If coordinates are missing, falls back to a default distance estimate.
    """
    if start_lat and start_lon and dest_lat and dest_lon:
        distance = calculate_distance(start_lat, start_lon, dest_lat, dest_lon)
    else:
        # Default local commute/sightseeing sightseeing estimate inside city
        distance = 150.0

    factor = CARBON_FACTORS.get(transport_mode, 120.0) # default to car
    flight_factor = CARBON_FACTORS["Flight ✈️"]
    
    # Calculate carbon footprint in kg CO2
    footprint = (distance * factor * num_people) / 1000.0
    
    # Compare with flight baseline to calculate savings
    baseline = (distance * flight_factor * num_people) / 1000.0
    savings = max(0.0, baseline - footprint)
    
    # Eco Karma Points: 10 points per kg CO2 saved, plus bonus for picking train
    karma_points = int(savings * 10)
    if transport_mode == "Train 🚆":
        karma_points += 50
    elif transport_mode == "Bus 🚌":
        karma_points += 20
        
    return {
        "distance_km": round(distance, 1),
        "footprint_kg": round(footprint, 2),
        "savings_kg": round(savings, 2),
        "karma_points": karma_points
    }
