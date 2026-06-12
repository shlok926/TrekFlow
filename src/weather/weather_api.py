# src/weather/weather_api.py
import requests
import logging
import streamlit as st

logger = logging.getLogger(__name__)

# Map common weather descriptions to emojis
WEATHER_EMOJIS = {
    "sunny": "☀️",
    "clear": "☀️",
    "partly cloudy": "⛅",
    "cloudy": "☁️",
    "overcast": "☁️",
    "mist": "🌫️",
    "fog": "🌫️",
    "patchy rain nearby": "🌦️",
    "patchy rain": "🌦️",
    "light rain": "🌧️",
    "moderate rain": "🌧️",
    "heavy rain": "🌧️",
    "torrential rain": "⛈️",
    "thunder": "⛈️",
    "thundery outbreaks": "⛈️",
    "snow": "❄️",
    "sleet": "❄️",
    "blizzard": "❄️",
    "ice": "❄️"
}

def get_weather_emoji(desc: str) -> str:
    desc_lower = desc.lower().strip()
    for key, emoji in WEATHER_EMOJIS.items():
        if key in desc_lower:
            return emoji
    return "🌡️"

@st.cache_data(ttl=3600)
def get_city_weather(city: str) -> dict:
    """
    Fetches real-time weather and coordinates from wttr.in.
    Returns a dictionary with location info and 3-day forecast.
    """
    city_clean = city.strip()
    url = f"https://wttr.in/{city_clean}?format=j1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    # Defaults
    data = {
        "success": False,
        "latitude": 20.5937,  # Center of India
        "longitude": 78.9629,
        "country": "Unknown",
        "forecast": []
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            
            # Extract coordinates
            if "nearest_area" in res_json and len(res_json["nearest_area"]) > 0:
                area = res_json["nearest_area"][0]
                try:
                    data["latitude"] = float(area["latitude"])
                    data["longitude"] = float(area["longitude"])
                except Exception:
                    pass
                if "country" in area and len(area["country"]) > 0:
                    data["country"] = area["country"][0]["value"]
            
            # Extract forecast (usually 3 days)
            if "weather" in res_json:
                data["success"] = True
                for day in res_json["weather"]:
                    date_str = day.get("date", "")
                    max_temp = day.get("maxtempC", "")
                    min_temp = day.get("mintempC", "")
                    
                    # Get condition description from hourly
                    desc = "Clear"
                    if "hourly" in day and len(day["hourly"]) > 0:
                        # Grab mid-day forecast or first hourly
                        mid_index = min(4, len(day["hourly"]) - 1)
                        hourly_info = day["hourly"][mid_index]
                        if "weatherDesc" in hourly_info and len(hourly_info["weatherDesc"]) > 0:
                            desc = hourly_info["weatherDesc"][0]["value"]
                            
                    data["forecast"].append({
                        "date": date_str,
                        "max_temp": max_temp,
                        "min_temp": min_temp,
                        "condition": desc,
                        "emoji": get_weather_emoji(desc)
                    })
    except Exception as e:
        logger.error(f"Error fetching weather from wttr.in: {e}")
        
    # Generate mock/fallback forecast if API failed
    if not data["success"] or not data["forecast"]:
        # Fallback coordinates based on popular cities
        city_lower = city_clean.lower()
        if "mumbai" in city_lower:
            data["latitude"], data["longitude"] = 19.0760, 72.8777
            data["country"] = "India"
        elif "delhi" in city_lower:
            data["latitude"], data["longitude"] = 28.7041, 77.1025
            data["country"] = "India"
        elif "goa" in city_lower:
            data["latitude"], data["longitude"] = 15.2993, 74.1240
            data["country"] = "India"
        elif "manali" in city_lower:
            data["latitude"], data["longitude"] = 32.2396, 77.1887
            data["country"] = "India"
        elif "london" in city_lower:
            data["latitude"], data["longitude"] = 51.5074, -0.1278
            data["country"] = "United Kingdom"
        elif "paris" in city_lower:
            data["latitude"], data["longitude"] = 48.8566, 2.3522
            data["country"] = "France"
        elif "tokyo" in city_lower:
            data["latitude"], data["longitude"] = 35.6762, 139.6503
            data["country"] = "Japan"
        elif "new york" in city_lower:
            data["latitude"], data["longitude"] = 40.7128, -74.0060
            data["country"] = "United States"
            
        # Create a mock 3-day forecast
        data["forecast"] = [
            {"date": "Day 1", "max_temp": "28", "min_temp": "22", "condition": "Partly Cloudy", "emoji": "⛅"},
            {"date": "Day 2", "max_temp": "29", "min_temp": "23", "condition": "Sunny", "emoji": "☀️"},
            {"date": "Day 3", "max_temp": "27", "min_temp": "21", "condition": "Patchy rain", "emoji": "🌦️"}
        ]
        
    return data
