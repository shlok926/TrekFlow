# src/core/itinerary_chain.py
import datetime
import calendar
import re
from src.core.planner import TIME_SLOTS
from src.chains.ai_suggester import get_spot_description

def generate_itinerary(city: str, day_wise_spots: list[list[str]], start_date=None, trip_mood="Relax"):
    """
    Generates a structured, date-aware travel itinerary that intercepts weekly closures,
    holidays/events, traffic conditions, and appends street food/shopping/sunset local highlights.
    """
    from src.core.fallback_data import (
        get_fallback_spots, 
        NATIONAL_HOLIDAYS, 
        CITY_HOLIDAYS_EVENTS, 
        FALLBACK_HIGHLIGHTS
    )

    if start_date is None:
        start_date = datetime.date.today()

    output = [f"✨ {city.title()} Travel Itinerary\n"]
    city_key = city.lower().strip()

    # Fetch highlights
    highlights = FALLBACK_HIGHLIGHTS.get(city_key, {
        "street_food": "Local street food market delicacies.",
        "fashion_street": "Main shopping bazaar / street market.",
        "sunset_point": "Highest local scenic viewpoint or park."
    })

    # Weekly closure mapping (weekday indexes: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6)
    SPOT_WEEKLY_CLOSURES = {
        "taj mahal": 4,          # Friday
        "red fort": 0,           # Monday
        "elephanta caves": 0,    # Monday
        "national gallery of modern art": 0, # Monday
    }

    used_spots = set()
    for day in day_wise_spots:
        for spot in day:
            used_spots.add(spot.lower().strip())

    # Pool of backups (all fallback spots not already in the plan)
    backup_pool = [s for s in get_fallback_spots(city) if s.lower().strip() not in used_spots]

    for day_no, spots in enumerate(day_wise_spots, start=1):
        current_date = start_date + datetime.timedelta(days=day_no - 1)
        day_name = calendar.day_name[current_date.weekday()]
        date_str = current_date.strftime("%d %b %Y")

        output.append(f"🟦 DAY {day_no} – {day_name}, {date_str} – {city.title()} Highlights\n")

        # Check for National Holidays
        h_key = (current_date.month, current_date.day)
        if h_key in NATIONAL_HOLIDAYS:
            output.append(f"[⚠️ HOLIDAY ALERT: Today is {NATIONAL_HOLIDAYS[h_key]}. Major monuments and offices may have restricted entry or closures!]\n")

        # Check for City Events
        city_events = CITY_HOLIDAYS_EVENTS.get(city_key, [])
        for evt in city_events:
            c_val = current_date.month * 100 + current_date.day
            s_val = evt["start_month"] * 100 + evt["start_day"]
            e_val = evt["end_month"] * 100 + evt["end_day"]
            if s_val <= c_val <= e_val:
                output.append(f"[📅 EVENT ALERT: {evt['name']}]\n")

        # Process spots for the day
        for slot, place in zip(TIME_SLOTS, spots):
            # Check weekly closure
            closure_day = None
            for k, v in SPOT_WEEKLY_CLOSURES.items():
                if k in place.lower():
                    closure_day = v
                    break

            final_place = place
            swap_msg = ""
            if closure_day is not None and current_date.weekday() == closure_day:
                if backup_pool:
                    backup_spot = backup_pool.pop(0)
                    swap_msg = f" [⚠️ {place} is CLOSED on {day_name}s! Auto-swapped with backup: {backup_spot}]"
                    final_place = backup_spot
                    used_spots.add(backup_spot.lower().strip())
                else:
                    swap_msg = f" [⚠️ {place} is CLOSED on {day_name}s! We recommend exploring local bazaars instead.]"

            desc = get_spot_description(city, final_place)

            # Traffic optimization message
            traffic_msg = ""
            if "9:00 AM" in slot or "6:00 PM" in slot:
                if current_date.weekday() < 5:  # Mon-Fri
                    traffic_msg = " [🚗 Traffic Alert: Peak Rush Hours - Use metro/walking if possible]"
                else:
                    traffic_msg = " [👥 Crowd Alert: High weekend tourist traffic]"

            output.append(f"{slot}: {final_place}{swap_msg}{traffic_msg}\n{desc}\n")

        # Append Daily Local Highlights
        output.append(f"💡 Day {day_no} Local Highlights Guide:\n"
                      f"• Best Street Food: Try {highlights['street_food']}\n"
                      f"• Shopping & Fashion: Explore {highlights['fashion_street']}\n"
                      f"• Sunset Viewpoint: Catch the sunset at {highlights['sunset_point']}\n")
        output.append("\n")

    return "\n".join(output)
