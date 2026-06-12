# src/transport/booking_links.py
import urllib.parse

# Local database of curated hotels for popular cities
CURATED_HOTELS = {
    "mumbai": [
        {"name": "Zostel Mumbai", "tier": "Budget 🎒", "cost": "₹1,200/night", "rating": "4.2⭐", "amenities": "Free Wi-Fi, Social Cafe, AC Dorms"},
        {"name": "Trident Nariman Point", "tier": "Mid-range 🏨", "cost": "₹9,500/night", "rating": "4.6⭐", "amenities": "Sea View, Outdoor Pool, Gym"},
        {"name": "The Taj Mahal Palace", "tier": "Luxury 👑", "cost": "₹28,000/night", "rating": "4.9⭐", "amenities": "Iconic Heritage, Spa, Fine Dining"}
    ],
    "delhi": [
        {"name": "Smyle Inn Connaught Place", "tier": "Budget 🎒", "cost": "₹1,500/night", "rating": "4.0⭐", "amenities": "Free Breakfast, Central Location"},
        {"name": "The Park New Delhi", "tier": "Mid-range 🏨", "cost": "₹7,200/night", "rating": "4.3⭐", "amenities": "Nightclub, Pool, Spa, Cafe"},
        {"name": "The Leela Palace New Delhi", "tier": "Luxury 👑", "cost": "₹22,000/night", "rating": "4.8⭐", "amenities": "Rooftop Pool, Luxury Spa, Butler Service"}
    ],
    "goa": [
        {"name": "Happy Panda Hostel Arambol", "tier": "Budget 🎒", "cost": "₹900/night", "rating": "4.4⭐", "amenities": "Walk to Beach, Shared Kitchen, Chill Zone"},
        {"name": "Lemon Tree Amarante Beach Resort", "tier": "Mid-range 🏨", "cost": "₹6,500/night", "rating": "4.3⭐", "amenities": "Close to Beach, Pool, Spa"},
        {"name": "Taj Exotica Resort & Spa Goa", "tier": "Luxury 👑", "cost": "₹24,000/night", "rating": "4.8⭐", "amenities": "Private Beach, Golf Course, Fine Dining"}
    ],
    "manali": [
        {"name": "Alt Life Hostel Manali", "tier": "Budget 🎒", "cost": "₹800/night", "rating": "4.5⭐", "amenities": "Mountain Views, Riverside, Coworking space"},
        {"name": "Solang Valley Resort", "tier": "Mid-range 🏨", "cost": "₹5,800/night", "rating": "4.2⭐", "amenities": "Valley Views, Gym, Adventure Activities"},
        {"name": "The Span Resort & Spa", "tier": "Luxury 👑", "cost": "₹16,000/night", "rating": "4.7⭐", "amenities": "Riverside Lawns, Private Pool, Luxury Spa"}
    ],
    "jaipur": [
        {"name": "Moustache Hostel Jaipur", "tier": "Budget 🎒", "cost": "₹1,000/night", "rating": "4.3⭐", "amenities": "Rooftop Restaurant, Pool, Boutique Decor"},
        {"name": "Umaid Bhawan - Heritage Hotel", "tier": "Mid-range 🏨", "cost": "₹4,200/night", "rating": "4.4⭐", "amenities": "Heritage Architecture, Folk Dances, Pool"},
        {"name": "The Rambagh Palace", "tier": "Luxury 👑", "cost": "₹35,000/night", "rating": "4.9⭐", "amenities": "Royal Palace, Peacock Gardens, Fine Dining"}
    ],
    "london": [
        {"name": "SoHostel London", "tier": "Budget 🎒", "cost": "£35/night (~₹3,700)", "rating": "4.1⭐", "amenities": "Soho Location, Bar, Modern Dorms"},
        {"name": "CitizenM Tower of London", "tier": "Mid-range 🏨", "cost": "£180/night (~₹19,000)", "rating": "4.5⭐", "amenities": "iPad Room Controls, Rooftop Bar, Central"},
        {"name": "The Savoy", "tier": "Luxury 👑", "cost": "£650/night (~₹69,000)", "rating": "4.8⭐", "amenities": "Historic Hotel, Butler Service, Award-winning Dining"}
    ],
    "paris": [
        {"name": "Les Piaules Nation Hostel", "tier": "Budget 🎒", "cost": "€40/night (~₹3,600)", "rating": "4.2⭐", "amenities": "Rooftop Bar, Cozy Pods, Cafe"},
        {"name": "Hotel Caron de Beaumarchais Marais", "tier": "Mid-range 🏨", "cost": "€190/night (~₹17,000)", "rating": "4.4⭐", "amenities": "Historic Decor, Marais District, French Balconies"},
        {"name": "The Ritz Paris", "tier": "Luxury 👑", "cost": "€1,200/night (~₹108,000)", "rating": "4.9⭐", "amenities": "Hemingway Bar, Private Gardens, Ultimate Luxury"}
    ]
}

def get_hotel_recommendations(city: str) -> list:
    """
    Returns curated hotel recommendations based on city name.
    If city not in database, generates generic hotel suggestions.
    """
    city_lower = city.lower().strip()
    
    # Check if city matches any key
    for key, hotels in CURATED_HOTELS.items():
        if key in city_lower:
            return hotels
            
    # Generic fallback hotels
    city_title = city.title()
    return [
        {
            "name": f"Backpackers Den {city_title}", 
            "tier": "Budget 🎒", 
            "cost": "₹1,200/night", 
            "rating": "4.1⭐", 
            "amenities": "Free Wi-Fi, Social lounge, Lockers"
        },
        {
            "name": f"Royal Plaza Hotel & Suites {city_title}", 
            "tier": "Mid-range 🏨", 
            "cost": "₹5,500/night", 
            "rating": "4.3⭐", 
            "amenities": "Swimming Pool, Multi-cuisine Restaurant, AC"
        },
        {
            "name": f"The Grand Palace Resort {city_title}", 
            "tier": "Luxury 👑", 
            "cost": "₹15,000/night", 
            "rating": "4.7⭐", 
            "amenities": "Wellness Spa, Fine Dining, Infinity Pool, Valet"
        }
    ]

def get_flight_suggestions(city: str) -> list:
    """
    Generates mock flight suggestions for the city with estimated pricing from Indian hubs.
    """
    city_title = city.title()
    return [
        {"from": "New Delhi (DEL)", "to": city_title, "type": "Direct Flight", "duration": "2h 15m", "cost": "₹4,500 - ₹7,000"},
        {"from": "Mumbai (BOM)", "to": city_title, "type": "Direct Flight", "duration": "1h 45m", "cost": "₹3,800 - ₹6,500"},
        {"from": "Bengaluru (BLR)", "to": city_title, "type": "1-Stop / Direct", "duration": "2h 30m", "cost": "₹5,200 - ₹8,500"}
    ]

def get_search_links(city: str) -> dict:
    """
    Constructs real search query URLs for flights and hotels on major travel websites.
    """
    city_encoded = urllib.parse.quote_plus(city.strip())
    
    return {
        "booking_hotels": f"https://www.booking.com/searchresults.html?ss={city_encoded}",
        "google_flights": f"https://www.google.com/travel/flights?q=Flights%20to%20{city_encoded}",
        "mmt_hotels": f"https://www.makemytrip.com/hotels/hotel-listing/?city={city_encoded}",
        "mmt_flights": f"https://www.makemytrip.com/flights/"
    }
