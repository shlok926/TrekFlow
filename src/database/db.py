import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "planner.db")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            fullname TEXT,
            email TEXT,
            preferred_style TEXT,
            mobile_number TEXT,
            auth_provider TEXT DEFAULT 'local'
        )
    ''')
    
    # Migrations for existing databases
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN fullname TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN preferred_style TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN mobile_number TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN auth_provider TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN avatar TEXT DEFAULT '🎒'")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN currency TEXT DEFAULT 'INR'")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN temp_unit TEXT DEFAULT 'Celsius'")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN dist_unit TEXT DEFAULT 'Kilometers'")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN security_alerts INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN weather_warnings INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN eco_karma_milestones INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN theme_mode TEXT DEFAULT 'Dark Mode'")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'English'")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN bio TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN llm_model TEXT DEFAULT 'llama-3.3-70b-versatile'")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN emergency_contact TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN copilot_sms_enabled INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN copilot_email_enabled INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass
    
    # Trips table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            destination_city TEXT NOT NULL,
            trip_duration INTEGER NOT NULL,
            total_budget REAL NOT NULL,
            trip_type TEXT NOT NULL,
            num_people INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Itineraries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itineraries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            generated_text TEXT NOT NULL,
            sustainability_score REAL NOT NULL,
            FOREIGN KEY(trip_id) REFERENCES trips(id)
        )
    ''')
    
    # Document locker table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_locker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            encrypted_content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            paid_by TEXT NOT NULL,
            split_between TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(trip_id) REFERENCES trips(id)
        )
    ''')

    # Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            trip_id INTEGER,
            icon TEXT,
            title TEXT,
            text TEXT,
            timestamp TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # City FAQs table for local cache
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS city_faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            UNIQUE(city_name, question)
        )
    ''')
    
    seed_faqs(cursor)
    
    conn.commit()
    conn.close()

def seed_faqs(cursor):
    faqs = [
        # --- General FAQs ---
        ("General", "What are some essential travel packing tips?", 
         "1. Pack light and roll clothes instead of folding to save space. 2. Keep both digital and physical copies of your travel documents. 3. Carry a basic first-aid kit and essential medications. 4. Carry a reliable power bank and multi-pin adapter."),
        ("General", "How can I travel sustainably?", 
         "1. Carry a reusable water bottle and avoid single-use plastics. 2. Choose public transit, trains, or walking over private cabs. 3. Respect local wildlife and stick to designated trails. 4. Support local restaurants, small businesses, and guides."),
        ("General", "How do I keep my travel documents safe?", 
         "1. Store them in the encrypted TrekFlow Document Locker. 2. Keep physical copies in a waterproof zip pouch. 3. Email copies of your passport/ID to yourself. 4. Never leave your main wallet or passport unattended in public."),
        ("General", "What should I do in case of a travel emergency?", 
         "1. Trigger the SOS alert inside the TrekFlow sidebar/app settings. 2. Contact the local emergency helpline. 3. Reach out to your country's embassy if traveling internationally. 4. Inform your designated emergency contact immediately."),
        ("General", "How do I beat jet lag on long-haul flights?", 
         "1. Adjust your sleep schedule to your destination time zone a few days early. 2. Stay hydrated and avoid alcohol or heavy caffeine. 3. Get natural sunlight once you arrive. 4. Take a short 20-minute power nap if exhausted."),
        ("General", "How can I find cheap flights and accommodation?", 
         "1. Book at least 3-6 weeks in advance. 2. Use incognito mode to search flights. 3. Be flexible with your dates and transit airports. 4. Check out local homestays or hostels for cheaper lodging."),
        ("General", "What are the rules for carrying liquids on flights?", 
         "1. Liquid containers must be 100ml (3.4 oz) or less. 2. All containers must fit in a single transparent, resealable plastic bag. 3. Keep the bag separate for security screening. 4. Exceptions apply to baby milk and medicines."),
        ("General", "How do I secure my luggage for travel?", 
         "1. Use TSA-approved locks on zippers. 2. Attach a luggage tag with your name and contact info. 3. Take a photo of your bag before check-in. 4. Keep valuables, electronics, and passports in your carry-on."),
        ("General", "Should I get travel insurance?", 
         "Yes, travel insurance is highly recommended. It covers unexpected medical emergencies, trip cancellations, lost baggage, and travel delays. Always read the policy details before buying."),
        ("General", "How do I handle money and currency exchange?", 
         "1. Notify your bank of your travel dates. 2. Carry a small amount of local cash for emergencies. 3. Use international credit/debit cards with low foreign transaction fees. 4. Avoid airport exchange counters as they have poor rates."),

        # --- Delhi FAQs ---
        ("Delhi", "What is the best time to visit Delhi?", 
         "The best time to visit Delhi is from October to March when the winter weather is cool, pleasant, and perfect for exploring historical monuments and street markets."),
        ("Delhi", "What are the must-try foods in Delhi?", 
         "Must-try foods in Delhi include Butter Chicken (at Moti Mahal/Daryaganj), Chole Bhature (Karol Bagh), Paranthas (Gali Paranthe Wali), and street chaat like Dahi Bhalla and Golgappas."),
        ("Delhi", "What are the top attractions in Delhi?", 
         "Top places to visit include the Red Fort, Qutub Minar, India Gate, Humayun's Tomb, Lotus Temple, Akshardham Temple, and shopping hubs like Chandni Chowk and Connaught Place."),
        ("Delhi", "How to travel locally in Delhi?", 
         "The Delhi Metro is fast, clean, and cheap. Auto-rickshaws and Uber/Ola are also widely available for first and last mile connectivity."),
        ("Delhi", "What are the best shopping places in Delhi?", 
         "Sarojini Nagar and Janpath for cheap clothes, Connaught Place for brands, Dilli Haat for traditional handicrafts, and Chandni Chowk for wholesale items and lehengas."),
        ("Delhi", "Is Delhi safe for tourists?", 
         "Generally safe, but be cautious at night, avoid isolated areas, use official app-based taxis, and keep your belongings secure in crowded markets."),
        ("Delhi", "What are the best historical walks in Delhi?", 
         "Heritage walks through Old Delhi's narrow lanes, Mehrauli Archaeological Park, and Lodhi Gardens are highly recommended."),
        ("Delhi", "How is the street shopping in Chandni Chowk?", 
         "Vibrant but extremely crowded. Bargain well, keep your bags safe in front, and go early in the morning around 11 AM when shops open."),
        ("Delhi", "What is Dilli Haat?", 
         "A government-run open-air food plaza and craft bazaar showcasing authentic items and regional cuisines from different Indian states."),
        ("Delhi", "Best weekend getaways from Delhi?", 
         "Agra (Taj Mahal) is a 3-hour drive via Taj Expressway. Jaipur (Pink City) and Neemrana Fort are also very popular weekend road trips."),

        # --- Mumbai FAQs ---
        ("Mumbai", "What is the best time to visit Mumbai?", 
         "The best time to visit Mumbai is from November to February (cool and pleasant) or during August-September to experience the grand Ganesh Chaturthi festival."),
        ("Mumbai", "What are the must-try foods in Mumbai?", 
         "Must-try local foods include Vada Pav, Pav Bhaji, Bhel Puri at Juhu Beach, Keema Pav at Irani cafes, Bombay Sandwich, and Misal Pav."),
        ("Mumbai", "What are the top attractions in Mumbai?", 
         "Top attractions include the Gateway of India, Marine Drive (Queen's Necklace), Chhatrapati Shivaji Terminus, Bandra-Worli Sea Link, Haji Ali Dargah, and Elephanta Caves."),
        ("Mumbai", "How to travel locally in Mumbai?", 
         "Local trains are fast but very crowded during rush hour. Cabs (black-and-yellow), auto-rickshaws (suburbs only), and local BEST buses are good alternatives."),
        ("Mumbai", "What are the best shopping places in Mumbai?", 
         "Colaba Causeway for junk jewelry and clothes, Linking Road in Bandra for boutique items, Crawford Market for wholesale goods, and Fashion Street."),
        ("Mumbai", "What is the significance of Marine Drive?", 
         "A 3.6 km C-shaped boulevard also known as the Queen's Necklace because of street lights reflecting like a pearl necklace at night along the Arabian Sea."),
        ("Mumbai", "What should I expect at Elephanta Caves?", 
         "A 1-hour ferry ride from Gateway of India to see rock-cut cave temples dedicated to Lord Shiva dating back to the 5th century. Watch out for monkeys!"),
        ("Mumbai", "What is the street food culture in Mumbai?", 
         "Huge! Street food stalls are very popular. Try food at Juhu Beach or Girgaon Chowpatty for the best beach-side culinary experience."),
        ("Mumbai", "How is the nightlife in Mumbai?", 
         "Very lively. Bandra, Lower Parel, and Colaba have great pubs, craft breweries, and lounge bars that stay open late into the night."),
        ("Mumbai", "Best weekend getaways from Mumbai?", 
         "Lonavala and Khandala (hill stations), Alibaug (beach resort, reachable by ferry/speed boat), and Matheran (automobile-free hill station)."),

        # --- Goa FAQs ---
        ("Goa", "What is the best time to visit Goa?", 
         "The best time to visit Goa is from November to February for beaches, water sports, and nightlife. Monsoons (June to September) are also beautiful for green landscapes."),
        ("Goa", "What are the must-try foods in Goa?", 
         "Must-try traditional Goan dishes include Goan Fish Thali, Bebinca (dessert), Chicken Xacuti, Pork Vindaloo, Shark Ambot Tik, and locally sourced Feni."),
        ("Goa", "What are the top attractions in Goa?", 
         "Top attractions include Calangute & Baga Beaches, Basilica of Bom Jesus, Fort Aguada, Dudhsagar Waterfalls, and the spice plantations in Ponda."),
        ("Goa", "What is the difference between North and South Goa?", 
         "North Goa is famous for party beaches, crowded markets, and water sports. South Goa is known for peaceful, clean, and scenic beaches with heritage stays."),
        ("Goa", "What are the best beaches for water sports in Goa?", 
         "Baga, Calangute, and Anjuna beaches in the north are famous for parasailing, jet skiing, banana boat rides, and bumper rides."),
        ("Goa", "How to travel locally in Goa?", 
         "Renting a self-drive scooter/bike (around Rs. 300-500/day) or self-drive car is the most popular and cheapest way. Taxis are expensive as there is no Uber/Ola."),
        ("Goa", "What are the best shopping spots in Goa?", 
         "Anjuna Wednesday Flea Market, Arpora Saturday Night Market, and Panaji local shops for cashew nuts, handicrafts, and Goan spices."),
        ("Goa", "What are Goan spice plantations?", 
         "Farms in Ponda where you can tour organic spices, see how local Feni is made, enjoy an elephant bath/ride, and eat a traditional Goan buffet lunch."),
        ("Goa", "Is Goa safe for solo female travelers?", 
         "Yes, Goa is one of the safest tourist destinations in India. Avoid dark, isolated beach stretches at night and hire verified cabs."),
        ("Goa", "What is Dudhsagar Falls?", 
         "A spectacular four-tiered waterfall on the Mandovi River, looking like milk flowing down, reachable by a forest jeep safari in Bhagwan Mahavir Sanctuary."),

        # --- Jaipur FAQs ---
        ("Jaipur", "What is the best time to visit Jaipur?", 
         "The best time to visit Jaipur is between October and March when temperatures are mild and ideal for walking tours through massive hill forts."),
        ("Jaipur", "What are the must-try foods in Jaipur?", 
         "Must-try foods in Jaipur include Dal Baati Churma, Pyaaz Kachori (Rawat Mishtan Bhandar), Laal Maas, Ghewar (traditional sweet), and fresh Lassi from Lassiwala."),
        ("Jaipur", "What are the top attractions in Jaipur?", 
         "Top attractions include Hawa Mahal (Palace of Winds), Amber Fort, City Palace, Jantar Mantar (UNESCO site), Albert Hall Museum, and shopping in Johri Bazaar."),
        ("Jaipur", "What is Chokhi Dhani?", 
         "A mock Rajasthani village resort showcasing traditional folk dance, puppet shows, camel rides, pottery making, and a traditional royal feast served on leaves."),
        ("Jaipur", "Best shopping places in Jaipur?", 
         "Johri Bazaar for precious gemstones and jewelry, Bapu Bazaar for block print textiles and leather mojris, and Tripolia Bazaar for lac bangles."),
        ("Jaipur", "How to travel locally in Jaipur?", 
         "Auto-rickshaws, e-rickshaws, and app-based cabs (Uber/Ola) are cheap and easy to find. Local city buses also cover major tourist attractions."),
        ("Jaipur", "What is the story of Hawa Mahal?", 
         "Built in 1799 with 953 small windows (jharokhas) so royal women could watch daily street life and processions without being seen from the outside."),
        ("Jaipur", "Which fort is best to watch the sunset in Jaipur?", 
         "Nahargarh Fort offers a spectacular panoramic view of the entire Jaipur city illuminated at sunset, with a heritage restaurant at the top."),
        ("Jaipur", "What is Amer Fort famous for?", 
         "Known for its artistic Hindu elements, sheesh mahal (mirror palace built with imported Belgian glass), and elephant rides up the fort path."),
        ("Jaipur", "Can I do a day trip from Jaipur to Pushkar?", 
         "Yes, Pushkar is around 2.5 hours away, famous for the rare Lord Brahma Temple, holy Pushkar Lake, and the annual camel fair."),

        # --- Kashmir FAQs ---
        ("Kashmir", "What is the best time to visit Kashmir?", 
         "Visit between March and August (spring/summer) for blooming tulip gardens and lush meadows. For snow and winter sports, Gulmarg is best from December to February."),
        ("Kashmir", "What are the must-try foods in Kashmir?", 
         "Must-try Kashmiri food includes Rogan Josh, Kashmiri Yakhni, Dum Aloo, Gushtaba, and traditional saffron-infused green tea called Kahwa."),
        ("Kashmir", "What are the top attractions in Kashmir?", 
         "Top attractions include Dal Lake in Srinagar (Shikara ride), Gulmarg (Gondola ride), Betaab Valley in Pahalgam, and the meadow of gold in Sonamarg."),
        ("Kashmir", "What should I expect on a Shikara ride?", 
         "A peaceful wooden boat ride on Dal Lake, visiting floating shops, vegetable markets, and historical gardens around the lake."),
        ("Kashmir", "What is Gulmarg famous for?", 
         "Famous for its ski slopes, snow-capped mountains, golf course, and the Gondola (one of the highest cable cars in Asia reaching 14,000 ft)."),
        ("Kashmir", "How to travel locally in Kashmir?", 
         "Prepaid/postpaid taxis and local shared cabs. Note that outside taxis are often not allowed in Gulmarg/Pahalgam, requiring local guides/ponies."),
        ("Kashmir", "Best shopping items in Kashmir?", 
         "Hand-knotted Pashmina shawls, organic saffron, saffron-infused Kahwa tea, walnuts, almonds, and hand-painted papier-mache crafts."),
        ("Kashmir", "What is Betaab Valley?", 
         "A scenic valley in Pahalgam named after the Bollywood movie 'Betaab' which was shot there. Known for rolling hills and clear mountain streams."),
        ("Kashmir", "Is Kashmir safe for tourists?", 
         "Yes, tourism is highly protected and locals are very welcoming. Stick to tourist areas, hire verified guides, and check local weather advisories."),
        ("Kashmir", "What is a Houseboat stay?", 
         "Staying in traditional carved cedar-wood boats floating on Dal or Nigeen lake, offering a vintage royal vibe and home-cooked Kashmiri food."),

        # --- Bengaluru FAQs ---
        ("Bengaluru", "What is the best time to visit Bengaluru?", 
         "Bengaluru has moderate, pleasant weather year-round, but the best time to visit is from October to February when the winter breeze is cool."),
        ("Bengaluru", "What are the must-try foods in Bengaluru?", 
         "Must-try items include Masala Dosa (CTR or Vidyarthi Bhavan), Idli Vada with filter coffee, Bisi Bele Bath, and craft beers at local microbreweries."),
        ("Bengaluru", "What are the top attractions in Bengaluru?", 
         "Top attractions include Lalbagh Botanical Garden, Bangalore Palace, Cubbon Park, Visvesvaraya Museum, and Nandi Hills (on the outskirts for sunrise)."),
        ("Bengaluru", "Why is Bengaluru called the Silicon Valley of India?", 
         "It is the hub of India's IT sector, hosting major tech startups and global software companies."),
        ("Bengaluru", "How to travel locally in Bengaluru?", 
         "Namma Metro is fast and traffic-free. Auto-rickshaws (Ola/Uber/Rapido) and city buses are also good."),
        ("Bengaluru", "Best weekend treks near Bengaluru?", 
         "Nandi Hills, Savandurga (largest monolith in Asia), and Skandagiri."),
        ("Bengaluru", "What is the pub culture in Bengaluru?", 
         "Known as the Pub Capital of India, the city is famous for craft breweries in Indiranagar and Koramangala."),
        ("Bengaluru", "What to buy in Bengaluru?", 
         "Mysore Silk sarees, sandalwood handicrafts, filter coffee powder, and incense sticks."),
        ("Bengaluru", "What is Cubbon Park?", 
         "A massive 300-acre green park in the middle of the city, perfect for morning walks and peaceful reading."),
        ("Bengaluru", "Best places to shop in Bengaluru?", 
         "Commercial Street, Brigade Road, MG Road, and luxury malls like UB City."),

        # --- Kolkata FAQs ---
        ("Kolkata", "What is the best time to visit Kolkata?", 
         "The best time is from October to February when the weather is pleasant. Visiting during Durga Puja (September/October) is a spectacular cultural experience."),
        ("Kolkata", "What are the must-try foods in Kolkata?", 
         "Must-try foods include Kolkata Biryani (with potato), Roshogolla, Sandesh, Mishti Doi, Puchka (pani puri), and Mughlai Paratha."),
        ("Kolkata", "What are the top attractions in Kolkata?", 
         "Top attractions include the Victoria Memorial, Howrah Bridge, Dakshineswar Kali Temple, Indian Museum, and Science City."),
        ("Kolkata", "What is the tram system in Kolkata?", 
         "Asia's oldest operating electric tram network, offering a nostalgic heritage ride through old streets."),
        ("Kolkata", "Best shopping places in Kolkata?", 
         "New Market, Gariahat, College Street (for books), and Dakshinapan (for handicrafts)."),
        ("Kolkata", "What to see at Victoria Memorial?", 
         "A white marble palace built in memory of Queen Victoria, housing a grand museum and lush gardens."),
        ("Kolkata", "How to travel locally in Kolkata?", 
         "Yellow taxis, hand-pulled rickshaws (in old parts), metro, trams, and ferry rides on the Hooghly River."),
        ("Kolkata", "What is College Street famous for?", 
         "Known as Boi Para (Book Town), it is the largest second-hand book market in the world."),
        ("Kolkata", "What to expect at Kumartuli?", 
         "A traditional potters' quarter in North Kolkata where clay idols of Durga and other deities are handcrafted."),
        ("Kolkata", "Best day trips from Kolkata?", 
         "Sundarbans (mangrove forests), Shantiniketan (Tagore's university town), and Digha (beach)."),

        # --- Paris FAQs ---
        ("Paris", "What is the best time to visit Paris?", 
         "The best time to visit Paris is from April to June (spring) or October to November (autumn) when temperatures are mild, and tourist crowds are thinner."),
        ("Paris", "What are the must-try foods in Paris?", 
         "Must-try foods in Paris include fresh Croissants, Macarons, Crepes, Escargot (snails), French Onion Soup, Duck Confit, and premium local cheeses."),
        ("Paris", "What are the top attractions in Paris?", 
         "Top attractions include the Eiffel Tower, Louvre Museum, Notre-Dame Cathedral, Arc de Triomphe, Seine River Cruise, and Palace of Versailles."),
        ("Paris", "How to travel locally in Paris?", 
         "The Paris Metro is extensive and the easiest way to travel. Walking is also highly recommended."),
        ("Paris", "What is the Louvre Museum famous for?", 
         "The world's largest art museum, home to the Mona Lisa, Venus de Milo, and glass pyramids."),
        ("Paris", "How to get to the top of the Eiffel Tower?", 
         "You can take stairs or lifts. Booking tickets online weeks in advance is highly recommended to avoid long queues."),
        ("Paris", "Best shopping areas in Paris?", 
         "Champs-Elysees, Galeries Lafayette, Le Marais district, and local flea markets."),
        ("Paris", "What is a Seine River Cruise?", 
         "A scenic boat tour along the Seine River, offering great views of Notre-Dame, Eiffel Tower, and historic bridges."),
        ("Paris", "Can I do a day trip to Disneyland Paris?", 
         "Yes, Disneyland Paris is easily reachable by RER A train from central Paris in about 40 minutes."),
        ("Paris", "What is the Palace of Versailles?", 
         "A royal château outside Paris, famous for the Hall of Mirrors and magnificent gardens."),

        # --- London FAQs ---
        ("London", "What is the best time to visit London?", 
         "The best time to visit London is between March and May for spring blooms, or during December for the festive Christmas lights and winter markets."),
        ("London", "What are the must-try foods in London?", 
         "Must-try British foods include Fish and Chips with mushy peas, a Full English Breakfast, Sunday Roast with Yorkshire Pudding, and traditional afternoon tea."),
        ("London", "What are the top attractions in London?", 
         "Top attractions include the British Museum, Tower of London (Crown Jewels), London Eye, Big Ben, Westminster Abbey, and Buckingham Palace."),
        ("London", "How to travel locally in London?", 
         "The Underground (Tube) is fast and easy. Use an Oyster card or contactless payment. Double-decker buses are also scenic."),
        ("London", "What is the London Eye?", 
         "A giant Ferris wheel on the South Bank of the River Thames, offering panoramic views of the city skyline."),
        ("London", "Best shopping districts in London?", 
         "Oxford Street, Regent Street, Covent Garden, Harrods in Knightsbridge, and Camden Market."),
        ("London", "What is the change of guard ceremony?", 
         "A formal ceremony outside Buckingham Palace where the King's Guard changes shifts, complete with a military band."),
        ("London", "Are museums free in London?", 
         "Yes, most major public museums (British Museum, Natural History Museum, Science Museum) have free general entry."),
        ("London", "What is the Tower of London?", 
         "A historic castle on the Thames, home to the Crown Jewels and guarded by Yeoman Warders (Beefeaters)."),
        ("London", "Best day trips from London?", 
         "Windsor Castle, Stonehenge, Oxford, Cambridge, and Bath are popular day trips by train."),

        # --- Tokyo FAQs ---
        ("Tokyo", "What is the best time to visit Tokyo?", 
         "The best time is from late March to April for the famous cherry blossoms (sakura), or from October to November for clear autumn skies and foliage."),
        ("Tokyo", "What are the must-try foods in Tokyo?", 
         "Must-try Japanese dishes include fresh Sushi (at Tsukiji), Tonkotsu Ramen, Tempura, Yakitori (skewered chicken), and Takoyaki (octopus balls)."),
        ("Tokyo", "What are the top attractions in Tokyo?", 
         "Top attractions include Senso-ji Temple in Asakusa, Shibuya Crossing, Meiji Shrine, Tokyo Skytree, Shinjuku Gyoen National Garden, and Harajuku."),
        ("Tokyo", "How to travel locally in Tokyo?", 
         "Tokyo's subway network is clean, fast, and punctual. JR trains are also convenient. Taxis are very expensive."),
        ("Tokyo", "What to expect at Shibuya Crossing?", 
         "The busiest pedestrian intersection in the world, where up to 3,000 people cross at the same time."),
        ("Tokyo", "What is Senso-ji Temple?", 
         "Tokyo's oldest Buddhist temple in Asakusa, famous for the large red Kaminarimon lantern and Nakamise shopping street."),
        ("Tokyo", "Best shopping hubs in Tokyo?", 
         "Ginza (luxury), Akihabara (electronics/anime), Shibuya (youth fashion), and Harajuku (alternative fashion)."),
        ("Tokyo", "What is a Shinto Shrine?", 
         "A sacred Shinto worship site. Meiji Shrine is the most famous in Tokyo, located in a quiet forest near Harajuku."),
        ("Tokyo", "Can I see Mount Fuji from Tokyo?", 
         "Yes, on clear days, you can see it from high observation decks (like Tokyo Metropolitan Gov Building) or take a day trip to Hakone."),
        ("Tokyo", "What is Tokyo Disney Resort?", 
         "A theme park resort consisting of Tokyo Disneyland and Tokyo DisneySea (unique to Japan), located in Chiba."),

        # --- New York FAQs ---
        ("New York", "What is the best time to visit New York?", 
         "Visit from September to November (crisp autumn weather) or April to June (spring). Visiting in December is also popular for the giant Rockefeller Christmas tree."),
        ("New York", "What are the must-try foods in New York?", 
         "Must-try foods in NYC include New York-style slice pizza, bagels with lox and cream cheese, pastrami sandwiches (Katz's), NY cheesecake, and street cart hot dogs."),
        ("New York", "What are the top attractions in New York?", 
         "Top attractions include Central Park, Times Square, Statue of Liberty & Ellis Island, Empire State Building, Broadway theatres, and the Metropolitan Museum of Art."),
        ("New York", "How to travel locally in New York?", 
         "The NYC Subway operates 24/7 and is the fastest way to get around. Yellow cabs and walking are also popular."),
        ("New York", "What to see in Central Park?", 
         "A massive 843-acre urban park with Bethesda Fountain, Strawberry Fields, Central Park Zoo, and rowboats on the lake."),
        ("New York", "How to visit the Statue of Liberty?", 
         "Take a ferry from Battery Park to Liberty Island. Book crown/pedestal tickets months in advance if you want to climb."),
        ("New York", "Best shopping areas in NYC?", 
         "Fifth Avenue, SoHo, Herald Square (Macy's), and Chelsea Market."),
        ("New York", "What to expect at a Broadway show?", 
         "World-class live theatre performances in the Theater District around Times Square. Buy tickets at TKTS booths for discounts."),
        ("New York", "What is the High Line?", 
         "A public park built on a historic elevated freight rail line on Manhattan's West Side, offering great street views."),
        ("New York", "Best viewpoints in New York?", 
         "Empire State Building, Top of the Rock, One World Observatory, and Edge at Hudson Yards.")
    ]
    
    # Insert or ignore to avoid duplicates
    cursor.executemany('''
        INSERT OR IGNORE INTO city_faqs (city_name, question, answer)
        VALUES (?, ?, ?)
    ''', faqs)

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
