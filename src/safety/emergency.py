# src/safety/emergency.py

CITY_EMERGENCY_DATA = {
    # INDIA
    "delhi": {
        "Nearest Hospital": "AIIMS (All India Institute of Medical Sciences), Safdarjung Enclave - Ph: 011-26588500",
        "Police Station": "Parliament Street Police Station, Connaught Place - Ph: 011-23742333",
        "Emergency Number": "112 (National Emergency), 102 (Ambulance), 100 (Police)",
        "Tourist Support": "1363 (24x7 Multi-lingual Tourist Helpline) or 1800-11-1363",
        "Embassy/Consular Info": "Chanakyapuri houses major embassies (US, UK, France, Germany, Japan). Keep contact details handy.",
        "Safety Tip": "Use app-based cabs (Uber, Ola, BluSmart) for safe late-night travel. Avoid unverified street autos after dark."
    },
    "mumbai": {
        "Nearest Hospital": "KEM Hospital, Parel (Ph: 022-24107000) or Lilavati Hospital, Bandra (Ph: 022-26751000)",
        "Police Station": "Colaba Police Station (near Gateway of India) - Ph: 022-22856817",
        "Emergency Number": "112 (National Emergency), 102 (Ambulance), 100 (Police)",
        "Tourist Support": "1363 (24x7 Multi-lingual Tourist Helpline) or 1800-11-1363",
        "Embassy/Consular Info": "Consulates are located in Bandra-Kurla Complex (BKC) and Nariman Point. Carry copy of visa.",
        "Safety Tip": "Insist on metered fares for local black-and-yellow taxis and auto-rickshaws, or use Uber/Ola apps."
    },
    "goa": {
        "Nearest Hospital": "Goa Medical College & Hospital, Bambolim - Ph: 0832-2458700",
        "Police Station": "Calangute Police Station (North Goa) - Ph: 0832-2278284",
        "Emergency Number": "112 (National Emergency), 108 (GVK EMRI Ambulance)",
        "Tourist Support": "Goa Tourism Department Helpline - Ph: 0832-2437026",
        "Embassy/Consular Info": "Foreign Consular Representatives are available in Panaji. Keep digital back-ups of passports.",
        "Safety Tip": "Follow local beach safety flags. Do not swim at night or in marked red-flagged high current zones."
    },
    "manali": {
        "Nearest Hospital": "Lady Willingdon Hospital, Old Manali - Ph: 01902-252379",
        "Police Station": "Manali Police Station, Mall Road - Ph: 01902-252326",
        "Emergency Number": "112 (National Emergency), 108 (Ambulance), 100 (Police)",
        "Tourist Support": "Himachal Pradesh Tourism Info Counter - Ph: 01902-253531",
        "Embassy/Consular Info": "No direct embassies in Himachal; contact your national embassy in New Delhi (Chanakyapuri).",
        "Safety Tip": "Verify weather & road blockages at Rohtang Pass before driving. Avoid driving on winding ghats after sunset."
    },
    "jaipur": {
        "Nearest Hospital": "SMS (Sawai Man Singh) Hospital, Ashok Nagar - Ph: 0141-2560291",
        "Police Station": "Manak Chowk Police Station (near Hawa Mahal) - Ph: 0141-2608444",
        "Emergency Number": "112 (National Emergency), 108 (Ambulance), 100 (Police)",
        "Tourist Support": "Rajasthan Tourist Reception Center, Jaipur - Ph: 0141-2200778",
        "Embassy/Consular Info": "Nearest consular resources are located in New Delhi, 260 km away.",
        "Safety Tip": "Avoid pushy gemstone vendors and tour guide touts outside Amber Palace. Buy from state-approved emporiums."
    },
    "bengaluru": {
        "Nearest Hospital": "St. John's Medical College & Hospital, Koramangala - Ph: 080-22065000",
        "Police Station": "Cubbon Park Police Station, Kasturba Road - Ph: 080-22942583",
        "Emergency Number": "112 (National Emergency), 108 (Ambulance), 100 (Police)",
        "Tourist Support": "Karnataka Tourism Development Corporation - Ph: 080-89517474",
        "Embassy/Consular Info": "Consulates (Germany, UK, US, France) are clustered in central Bangalore.",
        "Safety Tip": "Use Namma Yatri or Uber/Ola apps for local transport. Avoid auto-rickshaws that refuse to use digital fares."
    },
    "kolkata": {
        "Nearest Hospital": "SSKM Hospital, Acharya Jagadish Chandra Bose Road - Ph: 033-22235081",
        "Police Station": "Park Street Police Station, Mullick Bazar - Ph: 033-22849033",
        "Emergency Number": "112 (National Emergency), 102 (Ambulance), 100 (Police)",
        "Tourist Support": "West Bengal Tourism Info - Ph: 033-22436440",
        "Embassy/Consular Info": "US, UK, and major European consulates are situated in the Ho Chi Minh Sarani / Park Street area.",
        "Safety Tip": "Agree on a price before boarding yellow taxis, or book pre-paid cabs from Howrah/Sealdah station counters."
    },
    "kashmir": {
        "Nearest Hospital": "SMHS Hospital, Srinagar (Ph: 0194-2502104) or Sher-i-Kashmir Institute (SKIMS), Soura (Ph: 0194-2401013)",
        "Police Station": "Kothibagh Police Station, Srinagar - Ph: 0194-2452093",
        "Emergency Number": "112 (National Emergency), 102 (Ambulance), 100 (Police)",
        "Tourist Support": "J&K Tourism Reception Centre Srinagar - Ph: 0194-2502279",
        "Embassy/Consular Info": "Consular support must be coordinated via embassies in New Delhi.",
        "Safety Tip": "Buy Kashmiri handicrafts only from government-registered emporiums. Confirm pony ride rates at official booths."
    },
    "agra": {
        "Nearest Hospital": "District Hospital Agra, M.G. Road - Ph: 0562-2462521",
        "Police Station": "Tajganj Police Station (near Taj Mahal East Gate) - Ph: 0562-2230055",
        "Emergency Number": "112 (National Emergency), 108 (Ambulance), 100 (Police)",
        "Tourist Support": "UP Tourism Office Reception Counter - Ph: 0562-2226431",
        "Embassy/Consular Info": "No consular offices locally. Embassies are situated in New Delhi.",
        "Safety Tip": "Beware of 'hotel closed' or 'road block' lies by rickshaw drivers trying to divert you to commission shops."
    },
    "kochi": {
        "Nearest Hospital": "General Hospital Ernakulam - Ph: 0484-2361251",
        "Police Station": "Fort Kochi Police Station - Ph: 0484-2215058",
        "Emergency Number": "112 (National Emergency), 108 (Ambulance), 100 (Police)",
        "Tourist Support": "Kerala Tourism Desk Fort Kochi - Ph: 0484-221-6533",
        "Embassy/Consular Info": "Embassy help should be coordinated through consular offices in Chennai or New Delhi.",
        "Safety Tip": "Decline tuk-tuk tours offering free sights in exchange for visiting high-commission spice shops."
    },
    "hyderabad": {
        "Nearest Hospital": "NIMS (Nizam's Institute of Medical Sciences), Punjagutta - Ph: 040-23489000",
        "Police Station": "Charminar Police Station - Ph: 040-27853610",
        "Emergency Number": "112 (National Emergency), 108 (Ambulance), 100 (Police)",
        "Tourist Support": "Telangana Tourism Info, Hyderabad - Ph: 040-23262151",
        "Embassy/Consular Info": "US Consulate General is located in Financial District, Nanakramguda.",
        "Safety Tip": "Use Ola/Uber or metro to avoid auto overcharging. Buy pearls only from reputed, certified showrooms."
    },
    "chennai": {
        "Nearest Hospital": "Rajiv Gandhi Government General Hospital - Ph: 044-25305000",
        "Police Station": "Marina Beach Police Station - Ph: 044-23452618",
        "Emergency Number": "112 (National Emergency), 108 (Ambulance), 100 (Police)",
        "Tourist Support": "Tamil Nadu Tourism Complex, Wallajah Road - Ph: 044-25383333",
        "Embassy/Consular Info": "Major consulates (US, Japan, UK) are located on Cathedral Road and Anna Salai.",
        "Safety Tip": "Chennai auto drivers often refuse meters. Use Ola, Uber, or Rapido apps to secure fair fares."
    },
    "varanasi": {
        "Nearest Hospital": "Sir Sunderlal Hospital (BHU), Lanka - Ph: 0542-2367568",
        "Police Station": "Dashashwamedh Police Station (near Ghats) - Ph: 0542-2451000",
        "Emergency Number": "112 (National Emergency), 102 (Ambulance), 100 (Police)",
        "Tourist Support": "Varanasi Tourist Office, Cantonment - Ph: 0542-2502753",
        "Embassy/Consular Info": "No local consulates. Coordinate with New Delhi embassies.",
        "Safety Tip": "Haggle hard for boat rides at the Ghats, or check rates at government boards. Ignore fake pundits offering pujas."
    },
    "udaipur": {
        "Nearest Hospital": "Maharana Bhupal Government Hospital - Ph: 0294-2528811",
        "Police Station": "Clock Tower Police Station, Udaipur - Ph: 0294-2418501",
        "Emergency Number": "112 (National Emergency), 108 (Ambulance), 100 (Police)",
        "Tourist Support": "Tourist Information Centre, City Station - Ph: 0294-2411535",
        "Embassy/Consular Info": "No local consulates. Nearest help is in New Delhi.",
        "Safety Tip": "Only hire guides with official Tourism Department ID cards at the City Palace. Avoid street gemstone dealers."
    },
    "amritsar": {
        "Nearest Hospital": "Sri Guru Ram Das Charitable Hospital, Vallah - Ph: 0183-2870200",
        "Police Station": "Kotwali Police Station (near Golden Temple) - Ph: 0183-2545585",
        "Emergency Number": "112 (National Emergency), 108 (Ambulance), 100 (Police)",
        "Tourist Support": "Amritsar International Tourist Information Centre - Ph: 0183-2402452",
        "Embassy/Consular Info": "No consular offices. Coordinate with embassies in New Delhi.",
        "Safety Tip": "Wagah Border entry is free. Avoid touts selling VIP passes. Keep your footwear safe at Golden Temple lockers."
    },
    
    # INTERNATIONAL
    "london": {
        "Nearest Hospital": "St Thomas' Hospital, Westminster - Ph: +44 (0)20 7188 7188",
        "Police Station": "Charing Cross Police Station, Agar St - Ph: +44 101 (Non-emergency)",
        "Emergency Number": "999 (Emergency - Police/Ambulance/Fire), 111 (NHS Medical Advice)",
        "Tourist Support": "Visit London Official Information Desk - Ph: +44 (0)20 7234 5800",
        "Embassy/Consular Info": "London hosts embassy clusters in Belgravia and Kensington. Keep your passport copy safe.",
        "Safety Tip": "Keep an eye on bags in public transit. Beware of shell game scammers on Westminster Bridge."
    },
    "paris": {
        "Nearest Hospital": "Hôtel-Dieu de Paris, 1 Parvis Notre-Dame - Ph: +33 (0)1 42 34 82 34",
        "Police Station": "Commissariat de Police - 1er Arrondissement - Ph: +33 (0)1 44 88 18 00",
        "Emergency Number": "112 (European Emergency), 15 (SAMU Medical), 17 (Police), 18 (Fire)",
        "Tourist Support": "Paris Convention and Visitors Bureau Helpline - Ph: +33 (0)1 49 52 42 63",
        "Embassy/Consular Info": "Embassies are located in central Paris. Store digital scans of your visa/passport in your secure vault.",
        "Safety Tip": "Watch out for pickpockets near the Eiffel Tower and Metro. Ignore bracelet touts at Sacré-Cœur."
    },
    "tokyo": {
        "Nearest Hospital": "St. Luke's International Hospital, Tsukiji - Ph: +81 (0)3 3541 5151",
        "Police Station": "Shibuya Police Station, Shibuya 3-chome - Ph: +81 (0)3 3498 0110",
        "Emergency Number": "110 (Police), 119 (Ambulance/Fire)",
        "Tourist Support": "Japan National Tourism Organization Helpline - Ph: +81 (0)3 3813 4110",
        "Embassy/Consular Info": "Major diplomatic missions are located in Minato-ku and Chiyoda-ku.",
        "Safety Tip": "Extremely safe city, but avoid following street touts in Kabukicho (Shinjuku) to prevent bar bill padding."
    },
    "new york": {
        "Nearest Hospital": "NYU Langone Health Hospital, First Ave - Ph: +1 212-263-5800",
        "Police Station": "Midtown South Precinct (Times Square) - Ph: +1 212-244-1051",
        "Emergency Number": "911 (Police, Ambulance, Fire), 311 (Non-emergency Info)",
        "Tourist Support": "NYC Tourism Information Center - Ph: +1 212-484-1200",
        "Embassy/Consular Info": "Consulates are scattered across Midtown Manhattan. Permanent missions are near the UN Headquarters.",
        "Safety Tip": "Ignore costume characters in Times Square demanding money for photos. Keep wallets in front pockets."
    },
    "dubai": {
        "Nearest Hospital": "Rashid Hospital, Oud Metha - Ph: +971 (0)4 219 2000",
        "Police Station": "Al Muraqqabat Police Station, Deira - Ph: +971 (0)4 266 0555",
        "Emergency Number": "999 (Police), 998 (Ambulance), 997 (Fire)",
        "Tourist Support": "Dubai Tourism Helpline (24/7) - Ph: 800-4438 / +971 (0)4 201 0000",
        "Embassy/Consular Info": "Embassies are located in Abu Dhabi (capital), with major Consulates General located in Dubai's Umm Hurair area.",
        "Safety Tip": "Only buy gold/jewelry from licensed souk shops. Dress modestly in public malls and government buildings."
    },
    "singapore": {
        "Nearest Hospital": "Singapore General Hospital (SGH), Outram Rd - Ph: +65 6222 3322",
        "Police Station": "Marina Bay Neighborhood Police Centre - Ph: +65 1800 225 0000",
        "Emergency Number": "999 (Police), 995 (Ambulance/Fire), 1777 (Non-emergency Medical)",
        "Tourist Support": "Singapore Tourism Board Visitor Hotline - Ph: +65 1800 736 2000",
        "Embassy/Consular Info": "Embassies and High Commissions are concentrated in Tanglin and Orchard Road areas.",
        "Safety Tip": "Do not litter, spit, or chew gum in public. Fines are strictly enforced. Jaywalking is illegal."
    },
    "sydney": {
        "Nearest Hospital": "Sydney Hospital and Sydney Eye Hospital, Macquarie St - Ph: +61 (0)2 9382 7111",
        "Police Station": "The Rocks Police Station, George St - Ph: +61 (0)2 8220 6399",
        "Emergency Number": "000 (Police, Ambulance, Fire), 131 444 (Non-emergency Police)",
        "Tourist Support": "Sydney Visitor Centre, The Rocks - Ph: +61 (0)2 9240 8500",
        "Embassy/Consular Info": "Embassies are in Canberra (capital); major Consulates General are located in Sydney CBD.",
        "Safety Tip": "Swim only between the red and yellow flags at Bondi and Manly beaches to avoid dangerous rip currents."
    },
    "rome": {
        "Nearest Hospital": "Ospedale Santo Spirito, Lungotevere in Saxia - Ph: +39 06 68351",
        "Police Station": "Questura di Roma (Central Police Station) - Ph: +39 06 46861",
        "Emergency Number": "112 (European Emergency), 113 (Police), 118 (Ambulance), 115 (Fire)",
        "Tourist Support": "Rome Tourist Info Point Termini - Ph: +39 06 0608",
        "Embassy/Consular Info": "Embassies are located in central Rome. Note that Vatican City has separate diplomatic representation.",
        "Safety Tip": "Keep backpacks closed and in front of you on public buses and metro. Watch out for pickpocket groups."
    },
    "bangkok": {
        "Nearest Hospital": "Bangkok General Hospital, Huai Khwang - Ph: +66 (0)2 310 3000",
        "Police Station": "Pathum Wan Police Station, Bangkok - Ph: +66 (0)2 215 2991",
        "Emergency Number": "191 (General Emergency), 1669 (Ambulance), 1155 (Tourist Police - English spoken)",
        "Tourist Support": "Tourism Authority of Thailand Helpline - Ph: 1672 / +66 (0)2 250 5500",
        "Embassy/Consular Info": "Embassies are situated in Sathorn and Wireless Road areas. Always carry a copy of your passport ID page.",
        "Safety Tip": "Ignore strangers claiming temples or the Grand Palace are 'closed'. Insist on using taxi meters."
    },
    "barcelona": {
        "Nearest Hospital": "Hospital Clínic de Barcelona, Villarroel - Ph: +34 932 27 54 00",
        "Police Station": "Mossos d'Esquadra Police Station, Nou de la Rambla - Ph: +34 933 06 23 00",
        "Emergency Number": "112 (European Emergency), 061 (Ambulance), 091 (National Police)",
        "Tourist Support": "Barcelona Turisme Call Centre - Ph: +34 932 85 38 00",
        "Embassy/Consular Info": "Consular offices are located in Barcelona city center (Passeig de Gràcia and Diagonal areas).",
        "Safety Tip": "Watch your belongings closely on La Rambla, beaches, and Metro. Guard against bird droppings scam."
    },
    "amsterdam": {
        "Nearest Hospital": "OLVG Hospital, Oosterpark - Ph: +31 (0)20 599 9111",
        "Police Station": "Police Station Amsterdam Centre, Nieuwsingel - Ph: +31 (0)900-8844 (Non-emergency)",
        "Emergency Number": "112 (European Emergency), 0900-8844 (Police Support Line)",
        "Tourist Support": "I Amsterdam Visitor Centre Termini - Ph: +31 (0)20 702 6000",
        "Embassy/Consular Info": "Embassies are in The Hague; major Consulates General are in Amsterdam (Museumplein area).",
        "Safety Tip": "Do not walk in designated red bicycle lanes to avoid crashes. Only board official taxis from airport queues."
    },
    "bali": {
        "Nearest Hospital": "BIMC Hospital Kuta (Ph: +62 361 761263) or Sanglah General Hospital, Denpasar (Ph: +62 361 227911)",
        "Police Station": "Kuta Police Station, Jl. Raya Kuta - Ph: +62 361 751599",
        "Emergency Number": "112 (National Emergency), 110 (Police), 118 (Ambulance)",
        "Tourist Support": "Bali Tourist Police Command Center - Ph: +62 361 754599",
        "Embassy/Consular Info": "Consulates (Australia, US, UK, Japan) are located in Sanur and Renon (Denpasar).",
        "Safety Tip": "Use only official Bluebird Taxis or Grab apps. Avoid money changers operating in small alleyways."
    },
    "cairo": {
        "Nearest Hospital": "El Salam International Hospital, Maadi - Ph: +20 (0)2 2524 0250",
        "Police Station": "Kasr El Nil Police Station, Downtown Cairo - Ph: +20 (0)2 2794 8265",
        "Emergency Number": "122 (Police), 123 (Ambulance), 126 (Tourist Police), 180 (Fire)",
        "Tourist Support": "Egypt Ministry of Tourism Helpline - Ph: 19654 / +20 (0)2 2267 4830",
        "Embassy/Consular Info": "Embassies are clustered in Garden City, Maadi, and Zamalek neighborhoods.",
        "Safety Tip": "Confirm camel ride prices including the descend and tip before mounting. Ignore people claiming gates are closed."
    },
    "cape town": {
        "Nearest Hospital": "Groote Schuur Hospital, Observatory - Ph: +27 (0)21 404 9111",
        "Police Station": "Cape Town Central Police Station, Buitenkant St - Ph: +27 (0)21 467 8001",
        "Emergency Number": "112 (from cell), 10111 (Police), 10177 (Ambulance)",
        "Tourist Support": "Cape Town Tourism Visitor Support - Ph: +27 (0)21 487 6552",
        "Embassy/Consular Info": "Consulates are located in the CBD and southern suburbs. Keep emergency contacts programmed.",
        "Safety Tip": "Never accept help from anyone standing near ATMs. Do not walk alone in unlit areas or trails after dark."
    }
}

def get_emergency_intel(city: str) -> dict:
    """
    Logic that provides emergency intel based on the destination.
    A crucial socially-impactful feature.
    """
    city_lower = city.lower().strip()
    
    # Check if we have this city in our database
    if city_lower in CITY_EMERGENCY_DATA:
        return CITY_EMERGENCY_DATA[city_lower]
        
    # Generic defaults if not found
    intel = {
        "Nearest Hospital": f"City Care Hospital, Central {city.title()}",
        "Police Station": f"Main Branch Police Station, {city.title()}",
        "Emergency Number": "112 (National Emergency), 108 (Ambulance)",
        "Tourist Support": "112 / Local Tourism Information Bureau",
        "Embassy/Consular Info": "We recommend registering with your national embassy before travel.",
        "Safety Tip": "Always share your live location with a trusted contact and keep copies of your documents in the vault."
    }
    
    # Soft defaults for other states
    if city_lower in ["delhi", "mumbai"]:
        intel["Safety Tip"] = "Use official Cab options from Apps. Avoid unverified late-night autos."
    elif city_lower in ["goa", "kerala", "andaman"]:
        intel["Safety Tip"] = "Follow local beach safety flags. Do not swim at night or in unmarked zones."
    elif city_lower in ["manali", "shimla", "kashmir", "leh"]:
        intel["Safety Tip"] = "Carry thermal wear. Beware of altitude sickness and check weather before driving passes."
        
    return intel
