# ✈️ TrekFlow — AI-Powered Travel Co-Pilot & Journey Manager

An advanced, premium AI-driven travel planning and management application built using Python, Streamlit, and LangChain. TrekFlow offers a full-featured, multilingual ecosystem for personalized itineraries, dynamic budgeting, collaborative expense splitting, encrypted document lockers, and real-time situational alerting.

---

## 🌟 Key Features

* **🤖 AI Co-Pilot & Chat Assistant**: Interactive AI companion with dynamic LLM support (including Groq models) that dynamically structures trip ideas, plans routes, and suggests hidden spots based on your customized travel vibe.
* **📅 Date-Aware Smart Itineraries**: Generates customized day-wise itineraries that automatically intercept public holidays, regional events, traffic alerts, peak rush hours, and local highlights (street food, shopping, sunset spots).
* **💰 Pro Budget Allocator**: Smart estimation engine that validates travel budgets and splits expenses into visual allocation charts (Food, Stays, Transport, Shopping, Sightseeing).
* **🌐 Multilingual Localization**: Complete native language support for 8 languages including **English, Hindi, Spanish, French, German, Italian, Japanese, and Russian**.
* **📊 Split-Trip Manager**: Shared group ledger to log travel expenses, calculate splits, and settle debts dynamically among companions.
* **🔒 Encrypted Travel Shield & Vault**: Secure profile manager, encrypted document vault to store copies of tickets/IDs, and settings for real-time notifications.
* **🌧️ Real-Time Alerting Engine**: Real-time pop-up system and dashboard alerts for weather changes, transit blocks, security advisories, and eco-karma milestones.
* **🗺️ Interactive Map Visualizations**: Integrated map renderers to plot daily hotspots and sights.
* **📄 Beautiful PDF Export & Mobile Integration**: Generates customized, production-grade PDF travel guides using ReportLab. The PDF includes a built-in mobile QR code that allows users to instantly sync their itinerary and chat with the AI Co-Pilot on their phone.

---

## 🛠️ Technology Stack

* **Frontend/Interface**: [Streamlit](https://streamlit.io/) (with a responsive, modern Dark/Light glassmorphism UI)
* **AI Orchestration**: [LangChain](https://www.langchain.com/), LangChain-Groq, Groq APIs
* **Database**: SQLite3 (for local data persistence of trips, expenses, documents, and user preferences)
* **PDF Engine**: ReportLab (dynamic canvas rendering, tables, flowables)
* **Utilities**: Pillow (image processing), QRCode (mobile syncing), Python-Dotenv

---

## 📂 Project Structure

```text
AI_Travel_Planner/
├── app.py                   # Main Streamlit application and routing entrypoint
├── pdf_generate.py          # Custom ReportLab PDF builder with QR integration
├── requirements.txt         # Project package dependencies
├── .gitignore               # Ignored build caches, logs, databases, & envs
├── README.md                # System documentation
└── src/                     # Core application modules
    ├── auth/                # Session authentication and AES encryption
    │   ├── auth_manager.py
    │   └── encryption.py
    ├── budget/              # Budget validator and allocation modules
    │   ├── allocator.py
    │   └── feasibility.py
    ├── chains/              # LangChain execution logic and LLM connector
    │   ├── ai_suggester.py
    │   └── chat_assistant.py
    ├── core/                # Core assistant logic (Mood, sustainability, alerts)
    │   ├── fallback_data.py
    │   ├── itinerary_chain.py
    │   ├── mood_engine.py
    │   ├── packing_assistant.py
    │   ├── planner.py
    │   ├── smart_alerts.py
    │   └── sustainability.py
    ├── database/            # SQLite operations (trips, notifications, expenses)
    │   ├── db.py
    │   ├── document_locker.py
    │   ├── notifications_manager.py
    │   ├── split_trip.py
    │   └── trips_manager.py
    ├── safety/              # Emergency services intelligence
    │   └── emergency.py
    ├── transport/           # Booking helper and micromobility suggestor
    │   ├── booking_links.py
    │   ├── micro_mobility.py
    │   └── travel_type.py
    ├── ui/                  # Map rendering helpers and Auth sub-pages
    │   ├── auth_ui.py
    │   └── map_renderer.py
    └── weather/             # Weather API connector
        └── weather_api.py
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/shlok926/TrekFlow.git
cd TrekFlow
```

### 2️⃣ Create and Activate Virtual Environment
```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Keys
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5️⃣ Run the Application
```bash
streamlit run app.py
```

---

## 🔒 Security & Best Practices
* **Zero Exposure**: SQLite databases (`*.db`), local log files, generated PDFs, and virtual environments (`env/`) are automatically ignored via `.gitignore` to prevent any credential leaks on GitHub.
* **AES-256 Encryption**: Sensitive data uploaded to the Travel Vault is encrypted at rest using local cryptography keys.

---

## 📺 Project Demo Video

Watch the execution and walkthrough of the application:
👉 [TrekFlow Demo Video](https://drive.google.com/file/d/1APE-HorIK1KM5sN4h5OSQrYg2_auD6CN/view?usp=sharing)
