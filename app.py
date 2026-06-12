import streamlit as st

# Must be the first Streamlit command
st.set_page_config(page_title="TrekFlow - Pro Max Planner", layout="wide")

from src.chains.ai_suggester import suggest_spots_for_city, get_llm_instance
from src.ui.auth_ui import show_auth_page

# Phase 2 Core logic imports (lightweight)
from src.budget.feasibility import validate_budget
from src.budget.allocator import allocate_budget
from src.transport.travel_type import suggest_travel_type
from src.transport.micro_mobility import suggest_micro_mobility

# Phase 3 & 4 Pro Max logic imports (lightweight)
from src.safety.emergency import get_emergency_intel
from src.core.packing_assistant import generate_packing_list
from src.core.mood_engine import process_mood
from src.core.smart_alerts import generate_smart_alerts
from src.database.db import get_connection, init_db
init_db()

import base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except Exception:
        return ""

# Multilingual Translations Registry
TRANSLATIONS = {
    "English": {
        "nav_home": "Home Dashboard",
        "nav_plan": "Plan New Trip",
        "nav_itinerary": "Itinerary & Guides",
        "nav_analytics": "Analytics & Eco-Karma",
        "nav_bookings": "Bookings & Stays",
        "nav_shield": "Travel Shield & Vault",
        "nav_split": "Split-Trip Manager",
        "nav_copilot": "AI Co-Pilot",
        "nav_settings": "Settings",
        "nav_about": "About & Privacy",
        "welcome_back": "Welcome back",
        "ready_adventure": "Ready for your next adventure?",
        "logout": "Logout",
        "settings_title": "User Settings",
        "settings_desc": "Manage your user profile, preferences, and security options here.",
        "edit_profile": "Edit Profile Details",
        "full_name": "Full Name",
        "email_address": "Email Address",
        "mobile_number": "Mobile Number",
        "preferred_vibe": "Preferred Travel Vibe",
        "save_settings": "Save Profile Settings",
        "change_password": "Change Password",
        "curr_pass": "Current Password",
        "new_pass": "New Password",
        "theme_mode": "App Interface Theme",
        "app_lang": "App Interface Language",
        "data_privacy": "Data Export & Privacy",
        "export_data": "Export My Data (JSON)",
        "clear_cache": "Clear Offline Cache",
        "avatar": "Profile Avatar",
        "bio": "Travel Bio",
        "temp_unit": "Temperature Unit",
        "dist_unit": "Distance Unit",
        "security_alerts": "Travel Security Alerts",
        "weather_warnings": "Weather Alerts & Advisories",
        "eco_karma_milestones": "Eco-Karma Milestones",
        "llm_model": "AI Assistant LLM Model",
        "factory_reset": "Factory Reset Account",
        "advanced_api_settings": "⚙️ Advanced & API Configuration",
        "regional_settings": "⚖️ Regional & Measurement Units",
        "notification_settings": "🔔 Notification & Alert Preferences",
        "avatar_help": "Choose a travel-themed avatar icon.",
        "bio_placeholder": "Describe your travel style (e.g. Solo hiker, street food lover)",
        "reset_warning": "⚠️ CAUTION: This will delete your entire database profile (trips, expenses, documents) and log you out. This action cannot be undone!",
        "reset_btn": "Wipe All Data & Reset Account",
        "bell_alerts": "Alerts",
        "no_alerts": "No active notifications.",
        "sim_alert_btn": "⚡ Sim Real-Time Alert",
        "clear_all_btn": "🧹 Clear All",
        "realtime_status": "⚡ Real-Time AI Alerting Active",
    },
    "Hindi": {
        "nav_home": "होम डैशबोर्ड",
        "nav_plan": "नई यात्रा की योजना",
        "nav_itinerary": "यात्रा मार्गदर्शिका",
        "nav_analytics": "एनालिटिक्स और इको-कर्म",
        "nav_bookings": "बुकिंग और स्टे",
        "nav_shield": "ट्रैवल शील्ड और वॉल्ट",
        "nav_split": "स्प्लिट-ट्रिप मैनेजर",
        "nav_copilot": "एआई को-पायलट",
        "nav_settings": "सेटिंग्स",
        "nav_about": "हमारे बारे में",
        "welcome_back": "आपका स्वागत है",
        "ready_adventure": "क्या आप अपनी अगली यात्रा के लिए तैयार हैं?",
        "logout": "लॉगआउट",
        "settings_title": "यूज़र सेटिंग्स",
        "settings_desc": "यहाँ अपनी प्रोफाइल, प्राथमिकताएँ और सुरक्षा विकल्प प्रबंधित करें।",
        "edit_profile": "प्रोफ़ाइल विवरण संपादित करें",
        "full_name": "पूरा नाम",
        "email_address": "ईमेल पता",
        "mobile_number": "मोबाइल नंबर",
        "preferred_vibe": "पसंदीदा यात्रा वाइब",
        "save_settings": "सेटिंग्स सहेजें",
        "change_password": "पासवर्ड बदलें",
        "curr_pass": "वर्तमान पासवर्ड",
        "new_pass": "नया पासवर्ड",
        "theme_mode": "ऐप इंटरफ़ेस थीम",
        "app_lang": "ऐप इंटरफ़ेस भाषा",
        "data_privacy": "डेटा निर्यात और गोपनीयता",
        "export_data": "मेरा डेटा निर्यात करें (JSON)",
        "clear_cache": "ऑफ़लाइन कैश साफ़ करें",
        "avatar": "प्रोफ़ाइल अवतार",
        "bio": "यात्रा बायो",
        "temp_unit": "तापमान इकाई",
        "dist_unit": "दूरी इकाई",
        "security_alerts": "यात्रा सुरक्षा अलर्ट",
        "weather_warnings": "मौसम अलर्ट और चेतावनियां",
        "eco_karma_milestones": "इको-कर्म उपलब्धियां",
        "llm_model": "एआई सहायक एलएलएम मॉडल",
        "factory_reset": "खाता फ़ैक्टरी रीसेट करें",
        "advanced_api_settings": "⚙️ एडवांस्ड और एपीआई कॉन्फ़िगरेशन",
        "regional_settings": "⚖️ क्षेत्रीय और मापन इकाइयाँ",
        "notification_settings": "🔔 अधिसूचना और अलर्ट प्राथमिकताएं",
        "avatar_help": "एक यात्रा-थीम वाला अवतार आइकन चुनें।",
        "bio_placeholder": "अपनी यात्रा शैली का वर्णन करें (जैसे कि अकेले पर्वतारोही, स्ट्रीट फूड प्रेमी)",
        "reset_warning": "⚠️ चेतावनी: यह आपकी पूरी प्रोफाइल (यात्राएं, खर्च, दस्तावेज़) को हटा देगा और आपको लॉगआउट कर देगा। इसे वापस नहीं लाया जा सकता!",
        "reset_btn": "सभी डेटा मिटाएं और खाता रीसेट करें",
        "bell_alerts": "अलर्ट",
        "no_alerts": "कोई सक्रिय अलर्ट नहीं है।",
        "sim_alert_btn": "⚡ रियल-टाइम अलर्ट सिम्युलेट करें",
        "clear_all_btn": "🧹 सभी साफ करें",
        "realtime_status": "⚡ रियल-टाइम एआई अलर्टिंग सक्रिय",
    },
    "Spanish": {
        "nav_home": "Panel de Inicio",
        "nav_plan": "Planificar Nuevo Viaje",
        "nav_itinerary": "Itinerario y Guías",
        "nav_analytics": "Análisis y Eco-Karma",
        "nav_bookings": "Reservas y Estancias",
        "nav_shield": "Escudo y Bóveda",
        "nav_split": "Gestor de Gastos Compartidos",
        "nav_copilot": "Co-Piloto IA",
        "nav_settings": "Configuraciones",
        "nav_about": "Acerca de y Privacidad",
        "welcome_back": "Bienvenido de nuevo",
        "ready_adventure": "¿Listo para tu próxima aventura?",
        "logout": "Cerrar sesión",
        "settings_title": "Configuración de Usuario",
        "settings_desc": "Administre su perfil, preferencias y opciones de seguridad aquí.",
        "edit_profile": "Editar Detalles del Perfil",
        "full_name": "Nombre Completo",
        "email_address": "Correo Electrónico",
        "mobile_number": "Número de Teléfono",
        "preferred_vibe": "Vibra de Viaje Preferida",
        "save_settings": "Guardar Configuración",
        "change_password": "Cambiar Contraseña",
        "curr_pass": "Contraseña Actual",
        "new_pass": "Nueva Contraseña",
        "theme_mode": "Tema de Interfaz de la Aplicación",
        "app_lang": "Idioma de la Aplicación",
        "data_privacy": "Exportación de Datos y Privacidad",
        "export_data": "Exportar mis datos (JSON)",
        "clear_cache": "Borrar caché local",
        "avatar": "Avatar de Perfil",
        "bio": "Biografía de Viaje",
        "temp_unit": "Unidad de Temperatura",
        "dist_unit": "Unidad de Distancia",
        "security_alerts": "Alertas de Seguridad de Viaje",
        "weather_warnings": "Alertas y Avisos Meteorológicos",
        "eco_karma_milestones": "Hitos de Eco-Karma",
        "llm_model": "Modelo LLM de Asistente IA",
        "factory_reset": "Restablecimiento de Fábrica",
        "advanced_api_settings": "⚙️ Configuración Avanzada y API",
        "regional_settings": "⚖️ Unidades Regionales y de Medida",
        "notification_settings": "🔔 Preferencias de Notificaciones",
        "avatar_help": "Elige un icono de avatar con temática de viaje.",
        "bio_placeholder": "Describe tu estilo de viaje (ej. Senderista solitario, amante de la comida callejera)",
        "reset_warning": "⚠️ PRECAUCIÓN: Esto eliminará todo tu perfil de base de datos (viajes, gastos, documentos) y cerrará tu sesión. ¡Esta acción no se puede deshacer!",
        "reset_btn": "Borrar todos los datos y restablecer cuenta",
        "bell_alerts": "Alertas",
        "no_alerts": "No hay notificaciones activas.",
        "sim_alert_btn": "⚡ Simular Alerta en Tiempo Real",
        "clear_all_btn": "🧹 Limpiar Todo",
        "realtime_status": "⚡ Alerta de IA en Tiempo Real Activa",
    },
"French": {
        "nav_home": "Tableau de Bord",
        "nav_plan": "Planifier un Voyage",
        "nav_itinerary": "Itinéraire et Guides",
        "nav_analytics": "Analyses et Éco-Karma",
        "nav_bookings": "Réservations et Hôtels",
        "nav_shield": "Bouclier de Voyage",
        "nav_split": "Gestion des Dépenses",
        "nav_copilot": "Co-Pilote IA",
        "nav_settings": "Paramètres",
        "nav_about": "À Propos et Confidentialité",
        "welcome_back": "Bon retour",
        "ready_adventure": "Prêt pour votre prochaine aventure?",
        "logout": "Se déconnecter",
        "settings_title": "Paramètres Utilisateur",
        "settings_desc": "Gerez votre profil, vos préférences et vos options de sécurité ici.",
        "edit_profile": "Modifier le profil",
        "full_name": "Nom Complet",
        "email_address": "Adresse E-mail",
        "mobile_number": "Numéro de Téléphone",
        "preferred_vibe": "Ambiance de Voyage Préférée",
        "save_settings": "Sauvegarder",
        "change_password": "Changer le mot de passe",
        "curr_pass": "Mot de passe actuel",
        "new_pass": "Nouveau mot de passe",
        "theme_mode": "Thème de l'interface",
        "app_lang": "Langue de l'interface",
        "data_privacy": "Exportation de Données",
        "export_data": "Exporter mes données (JSON)",
        "clear_cache": "Effacer le cache hors ligne",
        "avatar": "Avatar de Profil",
        "bio": "Bio de Voyage",
        "temp_unit": "Unité de Température",
        "dist_unit": "Unité de Distance",
        "security_alerts": "Alertes de Sécurité de Voyage",
        "weather_warnings": "Alertes Météo & Conseils",
        "eco_karma_milestones": "Jalons Éco-Karma",
        "llm_model": "Modèle LLM de l'Assistant IA",
        "factory_reset": "Réinitialisation Complète",
        "advanced_api_settings": "⚙️ Configuration Avancée & API",
        "regional_settings": "⚖️ Unités Régionales & de Mesure",
        "notification_settings": "🔔 Préférences de Notifications",
        "avatar_help": "Choisissez une icône d'avatar sur le thème du voyage.",
        "bio_placeholder": "Décrivez votre style de voyage (ex: randonneur solo, amateur de street food)",
        "reset_warning": "⚠️ ATTENTION: Cela supprimera l'ensemble de votre profil (voyages, dépenses, documents) et vous déconnectera. Cette action est irréversible !",
        "reset_btn": "Effacer toutes les données & Réinitialiser le compte",
        "bell_alerts": "Alertes",
        "no_alerts": "Aucune notification active.",
        "sim_alert_btn": "⚡ Simuler Alerte en Temps Réel",
        "clear_all_btn": "🧹 Tout Effacer",
        "realtime_status": "⚡ Alertes IA en Temps Réel Actives",
    },
    "German": {
        "nav_home": "Startseite",
        "nav_plan": "Neue Reise planen",
        "nav_itinerary": "Reiseplan & Reiseführer",
        "nav_analytics": "Analysen & Öko-Karma",
        "nav_bookings": "Buchungen & Aufenthalte",
        "nav_shield": "Reiseschutz & Tresor",
        "nav_split": "Gruppenkasse",
        "nav_copilot": "KI-Co-Pilot",
        "nav_settings": "Einstellungen",
        "nav_about": "Über uns & Datenschutz",
        "welcome_back": "Willkommen zurück",
        "ready_adventure": "Bereit für dein nächstes Abenteuer?",
        "logout": "Abmelden",
        "settings_title": "Benutzereinstellungen",
        "settings_desc": "Verwalte hier dein Profil, deine Präferenzen und Sicherheitsoptionen.",
        "edit_profile": "Profildetails bearbeiten",
        "full_name": "Vollständiger Name",
        "email_address": "E-Mail-Adresse",
        "mobile_number": "Mobiltelefonnummer",
        "preferred_vibe": "Bevorzugter Reise-Vibe",
        "save_settings": "Profileinstellungen speichern",
        "change_password": "Kennwort ändern",
        "curr_pass": "Aktuelles Kennwort",
        "new_pass": "Neues Kennwort",
        "theme_mode": "App-Design",
        "app_lang": "App-Sprache",
        "data_privacy": "Datenexport & Datenschutz",
        "export_data": "Meine Daten exportieren (JSON)",
        "clear_cache": "Offline-Cache leeren",
        "avatar": "Profil-Avatar",
        "bio": "Reise-Bio",
        "temp_unit": "Temperatureinheit",
        "dist_unit": "Distanzeinheit",
        "security_alerts": "Sicherheitswarnungen",
        "weather_warnings": "Wetterwarnungen",
        "eco_karma_milestones": "Öko-Karma-Meilensteine",
        "llm_model": "KI-Modell",
        "factory_reset": "Konto zurücksetzen",
        "advanced_api_settings": "⚙️ Erweiterte- & API-Konfiguration",
        "regional_settings": "⚖️ Regionale- & Maßeinheiten",
        "notification_settings": "🔔 Benachrichtigungseinstellungen",
        "avatar_help": "Wähle einen Avatar passend zu deinem Reisestil.",
        "bio_placeholder": "Beschreibe deinen Reisestil (z.B. Solo-Wanderer, Street-Food-Liebhaber)",
        "reset_warning": "⚠️ ACHTUNG: Dadurch wird dein gesamtes Datenbankprofil (Reisen, Ausgaben, Dokumente) gelöscht und du wirst abgemeldet. Dies kann nicht rückgängig gemacht werden!",
        "reset_btn": "Alle Daten löschen & Konto zurücksetzen",
        "bell_alerts": "Warnungen",
        "no_alerts": "Keine aktiven Benachrichtigungen.",
        "sim_alert_btn": "⚡ Echtzeit-Alarm simulieren",
        "clear_all_btn": "🧹 Alle löschen",
        "realtime_status": "⚡ Echtzeit-KI-Benachrichtigung aktiv",
    },
    "Italian": {
        "nav_home": "Bacheca",
        "nav_plan": "Pianifica Nuovo Viaggio",
        "nav_itinerary": "Itinerario e Guide",
        "nav_analytics": "Analisi e Eco-Karma",
        "nav_bookings": "Prenotazioni e Soggiorni",
        "nav_shield": "Scudo di Viaggio e Cassaforte",
        "nav_split": "Gestione Spese",
        "nav_copilot": "Co-Pilota IA",
        "nav_settings": "Impostazioni",
        "nav_about": "Informazioni e Privacy",
        "welcome_back": "Bentornato",
        "ready_adventure": "Pronto per la tua prossima avventura?",
        "logout": "Esci",
        "settings_title": "Impostazioni Utente",
        "settings_desc": "Gestisci qui il tuo profilo, le preferenze e le opzioni di sicurezza.",
"edit_profile": "Modifica Dettagli Profilo",
        "full_name": "Nome Completo",
        "email_address": "Indirizzo Email",
        "mobile_number": "Numero di Cellulare",
        "preferred_vibe": "Stile di Viaggio Preferito",
        "save_settings": "Salva Impostazioni Profilo",
        "change_password": "Cambia Password",
        "curr_pass": "Password Attuale",
        "new_pass": "Nuova Password",
        "theme_mode": "Tema dell'App",
        "app_lang": "Lingua dell'App",
        "data_privacy": "Esportazione Dati e Privacy",
        "export_data": "Esporta i miei dati (JSON)",
        "clear_cache": "Cancella Cache Locale",
        "avatar": "Avatar del Profilo",
        "bio": "Bio di Viaggio",
        "temp_unit": "Unità di Temperatura",
        "dist_unit": "Unità di Distanza",
        "security_alerts": "Avvisi di Sicurezza",
        "weather_warnings": "Allerta Meteo",
        "eco_karma_milestones": "Traguardi Eco-Karma",
        "llm_model": "Modello IA LLM",
        "factory_reset": "Ripristino di Fabbrica",
        "advanced_api_settings": "⚙️ Configurazione Avanzata e API",
        "regional_settings": "⚖️ Unità Regionali e di Misura",
        "notification_settings": "🔔 Preferenze di Notifica",
        "avatar_help": "Scegli un avatar che rifletta il tuo stile di viaggio.",
        "bio_placeholder": "Descrivi il tuo stile di viaggio (es. Escursionista solitario, amante del cibo di strada)",
        "reset_warning": "⚠️ ATTENZIONE: Questo cancellerà l'intero profilo del database (viaggi, spese, documenti) e ti disconnetterà. Questa azione non può essere annullata!",
        "reset_btn": "Cancella tutti i dati e ripristina account",
        "bell_alerts": "Avvisi",
        "no_alerts": "Nessun avviso attivo.",
        "sim_alert_btn": "⚡ Simula Avviso in Tempo Real",
        "clear_all_btn": "🧹 Cancella Tutto",
        "realtime_status": "⚡ Monitoraggio IA in Tempo Reale Attivo",
    },
    "Japanese": {
        "nav_home": "ホームダッシュボード",
        "nav_plan": "新規旅行計画",
        "nav_itinerary": "旅程とガイド",
        "nav_analytics": "分析とエコカルマ",
        "nav_bookings": "予約と宿泊",
        "nav_shield": "トラベルシールド＆保管庫",
        "nav_split": "割り勘マネージャー",
        "nav_copilot": "AIコパイロット",
        "nav_settings": "設定",
        "nav_about": "概要とプライバシー",
        "welcome_back": "おかえりなさい",
        "ready_adventure": "次の冒険の準備はできましたか？",
        "logout": "ログアウト",
        "settings_title": "ユーザー設定",
        "settings_desc": "プロフィール、環境設定、セキュリティオプションを管理します。",
        "edit_profile": "プロフィールの編集",
        "full_name": "氏名",
        "email_address": "メールアドレス",
        "mobile_number": "携帯電話番号",
        "preferred_vibe": "お好みの旅行スタイル",
        "save_settings": "設定を保存",
        "change_password": "パスワード変更",
        "curr_pass": "現在のパスワード",
        "new_pass": "新しいパスワード",
        "theme_mode": "アプリのテーマ",
        "app_lang": "アプリの言語",
        "data_privacy": "データエクスポートとプライバシー",
        "export_data": "データをエクスポート (JSON)",
        "clear_cache": "キャッシュをクリア",
        "avatar": "プロフィールアバター",
        "bio": "旅行自己紹介",
        "temp_unit": "温度単位",
        "dist_unit": "距離単位",
        "security_alerts": "セキュリティアラート",
        "weather_warnings": "気象警告アドバイザリー",
        "eco_karma_milestones": "エコカルマのマイルストーン",
        "llm_model": "AIアシスタнтLLMモデル",
        "factory_reset": "アカウントの初期化",
        "advanced_api_settings": "⚙️ 高度な設定とAPIキー設定",
        "regional_settings": "⚖️ 地域設定と測定単位",
        "notification_settings": "🔔 通知とアラート設定",
        "avatar_help": "旅行スタイルに合ったアバターを選択してください。",
        "bio_placeholder": "旅行のスタイルを説明してください (例: 一人旅好き、B級グルメマニア)",
        "reset_warning": "⚠️ 注意: これにより、データベースの全プロフィール（旅行、出費、文書）が削除され、ログアウトされます。この操作は取り消せません！",
        "reset_btn": "全データを消去してアカウントを初期化",
        "bell_alerts": "アラート",
        "no_alerts": "アクティブなアラートはありません。",
        "sim_alert_btn": "⚡ リアルタイムアラートをシミュレート",
        "clear_all_btn": "🧹 すべてクリア",
        "realtime_status": "⚡ リアルタイムAIアラート稼働中",
    },
    "Russian": {
        "nav_home": "Главная панель",
        "nav_plan": "Планирование поездки",
        "nav_itinerary": "Маршрут и гиды",
        "nav_analytics": "Аналитика и Эко-Карма",
        "nav_bookings": "Бронирования и отели",
        "nav_shield": "Защита поездки и сейф",
        "nav_split": "Разделение расходов",
        "nav_copilot": "ИИ-соавтор",
        "nav_settings": "Настройки",
        "nav_about": "О нас и конфиденциальность","welcome_back": "С возвращением",
        "ready_adventure": "Готовы к новому приключению?",
        "logout": "Выйти",
        "settings_title": "Настройки пользователя",
        "settings_desc": "Управление профилем, предпочтениями и настройками безопасности.",
        "edit_profile": "Редактировать профиль",
        "full_name": "Полное имя",
        "email_address": "Электронная почта",
        "mobile_number": "Номер мобильного",
        "preferred_vibe": "Предпочтительный стиль поездки",
        "save_settings": "Сохранить настройки профиля",
        "change_password": "Изменить пароль",
        "curr_pass": "Текущий пароль",
        "new_pass": "Новый пароль",
        "theme_mode": "Тема приложения",
        "app_lang": "Язык приложения",
        "data_privacy": "Экспорт данных и приватность",
        "export_data": "Экспортировать мои данные (JSON)",
        "clear_cache": "Очистить локальный кэш",
        "avatar": "Аватар профиля",
        "bio": "Описание путешественника",
        "temp_unit": "Единица температуры",
        "dist_unit": "Единица расстояния",
        "security_alerts": "Оповещения безопасности",
        "weather_warnings": "Предупреждения о погоде",
        "eco_karma_milestones": "Достижения Эко-Кармы",
        "llm_model": "Модель ИИ LLM",
        "factory_reset": "Сброс аккаунта",
        "advanced_api_settings": "⚙️ Дополнительные настройки и API",
        "regional_settings": "⚖️ Региональные настройки и измерения",
        "notification_settings": "🔔 Настройки уведомлений",
        "avatar_help": "Выберите аватар, соответствующий вашему стилю путешествий.",
        "bio_placeholder": "Опишите ваш стиль путешествий (например, соло-турист, любитель уличной еды)",
        "reset_warning": "⚠️ ВНИМАНИЕ: Это действие удалит весь ваш профиль из базы данных (поездки, расходы, документы) и выйдет из системы. Это действие нельзя отменить!",
        "reset_btn": "Стереть все данные и сбросить аккаунт",
        "bell_alerts": "Предупреждения",
        "no_alerts": "Нет активных уведомлений.",
        "sim_alert_btn": "⚡ Симулировать оповещение",
        "clear_all_btn": "🧹 Очистить всё",
        "realtime_status": "⚡ Мониторинг ИИ в реальном времени активен",
    }
}

def tr(key):
    lang = st.session_state.get("language", "English")
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, TRANSLATIONS["English"][key])

def fmt_currency(amount_inr, is_inr_value=True):
    currency = st.session_state.get("currency", "INR")
    symbols = {"INR": "₹", "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}
    symbol = symbols.get(currency, "₹")
    if not is_inr_value:
        return f"{symbol}{amount_inr:,.2f}"
    if currency == "INR":
        return f"₹{amount_inr:,.0f}"
    rates = {"USD": 0.012, "EUR": 0.011, "GBP": 0.0094, "JPY": 1.85, "INR": 1.0}
    rate = rates.get(currency, 1.0)
    converted = amount_inr * rate
    return f"{symbol}{converted:,.2f}"

def format_temp(temp_c_str):
    if not temp_c_str:
        return ""
    try:
        temp_c = float(temp_c_str)
    except ValueError:
        return f"{temp_c_str}°C"
    unit = st.session_state.get("temp_unit", "Celsius")
    if unit == "Fahrenheit":
        temp_f = (temp_c * 9/5) + 32
        return f"{temp_f:.1f}°F"
    return f"{temp_c:.0f}°C"

def format_distance(dist_km_str_or_num):
    if dist_km_str_or_num is None:
        return ""
    try:
        dist_km = float(dist_km_str_or_num)
    except ValueError:
        return f"{dist_km_str_or_num} km"
    unit = st.session_state.get("distance_unit", "Kilometers")
    if unit == "Miles":
        dist_mi = dist_km * 0.621371
        return f"{dist_mi:,.1f} miles"
    return f"{dist_km:,.1f} km"

def sync_notifications():
    import datetime
    import random
    from src.database.notifications_manager import add_db_notification, get_db_notifications
    
    notifications = []
    active_city = st.session_state.get("city")
    user_id = st.session_state.get("user_id")
    
    if not user_id:
        st.session_state["notifications"] = []
        return
        
    show_security = st.session_state.get("security_alerts", True)
    show_weather = st.session_state.get("weather_warnings", True)
    show_eco = st.session_state.get("eco_karma_milestones", True)
    
    trip_id = st.session_state.get("trip_id")
    if not trip_id and active_city:
        # Resolve trip_id from DB
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM trips WHERE user_id=? AND destination_city=? ORDER BY id DESC LIMIT 1", (user_id, active_city))
        row = cursor.fetchone()
        conn.close()
        if row:
            trip_id = row[0]
            st.session_state["trip_id"] = trip_id

    # Load notifications from database
    db_notes = []
    if user_id:
        db_notes = get_db_notifications(user_id, trip_id)
        
    # If a trip is active and database has no alerts yet, generate the initial smart alerts
    if active_city and trip_id and not db_notes:
        if "smart_alerts" not in st.session_state:
            st.session_state["smart_alerts"] = generate_smart_alerts(active_city)
            
        raw_alerts = st.session_state.get("smart_alerts", [])
        for alert in raw_alerts:
            icon, title = "🛡️", "System Scan"
            if "Weather AI" in alert:
                icon, title = "🌧️", "Weather Warning"
            elif "Crowd AI" in alert or "Time-Saver AI" in alert:
                icon, title = "🚦", "Security & Transit"
            elif "Hidden Cost AI" in alert:
                icon, title = "💰", "Budget Alert"
                
            add_db_notification(user_id, trip_id, icon, title, alert, "Just now")
            
        # Add initial eco milestones
        add_db_notification(
            user_id, 
            trip_id, 
            "🌿", 
            "Eco-Karma Milestone", 
            f"🎉 Congratulations! You earned 100 Eco-Karma points for planning your trip to **{active_city.title()}**.", 
            "Just now"
        )
        # Refetch
        db_notes = get_db_notifications(user_id, trip_id)

    # Background Real-Time Alert Generation (every 40 seconds)
    if active_city and trip_id:
        now = datetime.datetime.now()
        last_check = st.session_state.get("last_realtime_check")
        if last_check is None:
            st.session_state["last_realtime_check"] = now
            last_check = now
            
        if (now - last_check).total_seconds() >= 40:
            st.session_state["last_realtime_check"] = now
            
            # Pool of simulated alerts
            sim_pool = [
                {"icon": "🚨", "title": "Urgent Transit Alert", "text": f"🚨 **Real-Time Security AI:** Public transit disruption reported near major intersections in {active_city.title()} starting tomorrow. Plan alternate routes."},
                {"icon": "🌧️", "title": "Weather Alert", "text": f"🌧️ **Real-Time Weather AI:** Flood watch warning issued for the {active_city.title()} region. Flash storms expected soon."},
                {"icon": "⚠️", "title": "Security Alert", "text": f"⚠️ **Real-Time Safety AI:** Unofficial tour guide scam reported near {active_city.title()} monument hotspots in the last hour."},
                {"icon": "🎉", "title": "Eco Milestone", "text": f"🌿 **Real-Time Eco-Karma:** Green Travel Milestone unlocked for {active_city.title()}! You earned 100 points."}
            ]
            triggered = random.choice(sim_pool)
            
            # Check if this type is enabled in Settings
            is_valid = False
            if triggered["icon"] in ["🚨", "⚠️"] and show_security:
                is_valid = True
            elif triggered["icon"] == "🌧️" and show_weather:
                is_valid = True
            elif triggered["icon"] == "🎉" and show_eco:
                is_valid = True
                
            if is_valid:
                add_db_notification(
                    user_id,
                    trip_id,
                    triggered["icon"],
                    triggered["title"],
                    triggered["text"],
                    "Just now"
                )
                st.toast(f"🔔 {triggered['title']}: {triggered['text']}")
                # Refetch
                db_notes = get_db_notifications(user_id, trip_id)

    # Filter alerts on-the-fly based on Settings preferences
    filtered_notes = []
    for note in db_notes:
        icon = note.get("icon")
        # Security: 🚨, ⚠️, 🚦
        if icon in ["🚨", "⚠️", "🚦"] and not show_security:
            continue
        # Weather: 🌧️, 🌦️
        if icon in ["🌧️", "🌦️"] and not show_weather:
            continue
        # Eco-karma: 🌿, 🎉
        if icon in ["🌿", "🎉"] and not show_eco:
            continue
        filtered_notes.append(note)
        
    # If no active trip, show welcome default message in list
    if not active_city:
        filtered_notes.append({
            "id": 0,
            "trip_id": None,
            "icon": "🎒",
            "title": "Get Started",
            "text": "Welcome to TrekFlow! Head over to the 'Plan New Trip' page to generate your first AI travel itinerary and unlock real-time alerts.",
            "timestamp": "Just now"
        })
        
    st.session_state["notifications"] = filtered_notes

@st.fragment(run_every=15)
def render_notification_header():
    import random
    from src.database.notifications_manager import add_db_notification, clear_db_notifications
    
    # 1. Sync notifications to load from DB and run periodic background checks
    sync_notifications()
    
    active_city = st.session_state.get("city")
    trip_id = st.session_state.get("trip_id")
    user_id = st.session_state.get("user_id")
    
    # 2. Render columns
    col_hdr, col_bell = st.columns([2, 1])
    with col_hdr:
        display_name = st.session_state.get("fullname") or st.session_state.get("username", "Traveler")
        st.markdown(f"## 🏠 Home Dashboard")
        st.markdown(f"Hello, **{display_name}**! Manage your trips, view eco-stats, and access secure vault operations here.")
        if active_city:
            status_text = tr("realtime_status")
            st.markdown(f"<span style='font-size: 0.85rem; color: #1E90FF; font-weight: bold;'>{status_text}</span>", unsafe_allow_html=True)
            
    with col_bell:
        active_notes = st.session_state.get("notifications", [])
        alerts_count = len(active_notes)
        bell_text = f"🔔 {tr('bell_alerts')} ({alerts_count})"
        
        with st.expander(bell_text, expanded=False):
            if active_notes:
                for item in active_notes:
                    icon = item.get("icon", "🔔")
                    title = item.get("title", "Alert")
                    text = item.get("text", "")
                    timestamp = item.get("timestamp", "Just now")
                    
                    st.markdown(
                        f"""
                        <div style="padding: 10px; border-radius: 8px; background: rgba(255, 255, 255, 0.03); border-left: 4px solid #1E90FF; margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <strong style="color: #1E90FF;">{icon} {title}</strong>
                                <span style="font-size: 0.75rem; opacity: 0.6;">{timestamp}</span>
                            </div>
                            <div style="font-size: 0.85rem; margin-top: 4px;">{text}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.write(tr("no_alerts"))
                
            st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 10px 0;'/>", unsafe_allow_html=True)
            
            # Action buttons
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button(tr("sim_alert_btn"), key="btn_trigger_sim_bell_alert_frag", use_container_width=True):
                    # Spawn a simulated alert instantly into DB
                    if active_city and trip_id:
                        sim_pool = [
                            {"icon": "🚨", "title": "Urgent Transit Alert", "text": f"🚨 **Real-Time Security AI:** Public transit disruption reported near major intersections in {active_city.title()} starting tomorrow. Plan alternate routes."},
                            {"icon": "🌧️", "title": "Weather Alert", "text": f"🌧️ **Real-Time Weather AI:** Flood watch warning issued for the {active_city.title()} region. Flash storms expected soon."},
                            {"icon": "⚠️", "title": "Security Alert", "text": f"⚠️ **Real-Time Safety AI:** Unofficial tour guide scam reported near {active_city.title()} hotspots in the last hour."},
                            {"icon": "🎉", "title": "Eco Milestone", "text": f"🌿 **Real-Time Eco-Karma:** Green Travel Milestone unlocked for {active_city.title()}! You earned 100 points."}
                        ]
                        triggered = random.choice(sim_pool)
                        
                        show_sec = st.session_state.get("security_alerts", True)
                        show_wea = st.session_state.get("weather_warnings", True)
                        show_eco = st.session_state.get("eco_karma_milestones", True)
                        
                        is_valid = False
                        if triggered["icon"] in ["🚨", "⚠️"] and show_sec:
                            is_valid = True
                        elif triggered["icon"] == "🌧️" and show_wea:
                            is_valid = True
                        elif triggered["icon"] == "🎉" and show_eco:
                            is_valid = True
                            
                        if is_valid:
                            add_db_notification(
                                user_id, 
                                trip_id, 
                                triggered["icon"], 
                                triggered["title"], 
                                triggered["text"], 
                                "Just now"
                            )
                            st.toast(f"🔔 {triggered['title']}: {triggered['text']}")
                            st.rerun()
                        else:
                            st.warning("Alert filtered out by active Settings.")
                    else:
                        st.warning("Plan a trip first to simulate real-time alerts!")
            
            with col_b2:
                if st.button(tr("clear_all_btn"), key="btn_clear_all_bell_alerts", use_container_width=True):
                    if user_id:
                        clear_db_notifications(user_id, trip_id)
                        st.toast("🧹 Notifications cleared!")
                        st.rerun()

def show_main_app():
    # Load user settings from SQLite database if not loaded yet
    if "copilot_logs" not in st.session_state:
        st.session_state["copilot_logs"] = []
        
    if "user_settings_loaded" not in st.session_state:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT avatar, currency, temp_unit, dist_unit, security_alerts, weather_warnings, eco_karma_milestones, theme_mode, language, bio, llm_model, fullname, emergency_contact, copilot_sms_enabled, copilot_email_enabled, email, mobile_number FROM users WHERE id=?", (st.session_state["user_id"],))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            avatar, currency, temp_unit, dist_unit, security_alerts, weather_warnings, eco_karma_milestones, theme_mode, language, bio, llm_model, fullname, emergency_contact, copilot_sms, copilot_email, email_addr, mob_num = row
            st.session_state["avatar"] = avatar or "🎒"
            st.session_state["currency"] = currency or "INR"
            st.session_state["temp_unit"] = temp_unit or "Celsius"
            st.session_state["distance_unit"] = dist_unit or "Kilometers"
            st.session_state["security_alerts"] = True if security_alerts is None or security_alerts == 1 else False
            st.session_state["weather_warnings"] = True if weather_warnings is None or weather_warnings == 1 else False
            st.session_state["eco_karma_milestones"] = True if eco_karma_milestones is None or eco_karma_milestones == 1 else False
            st.session_state["theme_mode"] = theme_mode or "Dark Mode"
            st.session_state["language"] = language or "English"
            st.session_state["user_bio"] = bio or ""
            st.session_state["llm_model"] = llm_model or "llama-3.3-70b-versatile"
            st.session_state["fullname"] = fullname or ""
            st.session_state["emergency_contact"] = emergency_contact or ""
            st.session_state["copilot_sms_enabled"] = True if copilot_sms is None or copilot_sms == 1 else False
            st.session_state["copilot_email_enabled"] = True if copilot_email is None or copilot_email == 1 else False
            st.session_state["email"] = email_addr or ""
            st.session_state["mobile_number"] = mob_num or ""
        else:
            st.session_state["avatar"] = "🎒"
            st.session_state["currency"] = "INR"
            st.session_state["temp_unit"] = "Celsius"
            st.session_state["distance_unit"] = "Kilometers"
            st.session_state["security_alerts"] = True
            st.session_state["weather_warnings"] = True
            st.session_state["eco_karma_milestones"] = True
            st.session_state["theme_mode"] = "Dark Mode"
            st.session_state["language"] = "English"
            st.session_state["user_bio"] = ""
            st.session_state["llm_model"] = "llama-3.3-70b-versatile"
            st.session_state["fullname"] = ""
            st.session_state["emergency_contact"] = ""
            st.session_state["copilot_sms_enabled"] = True
            st.session_state["copilot_email_enabled"] = True
            st.session_state["email"] = ""
            st.session_state["mobile_number"] = ""
        st.session_state["user_settings_loaded"] = True

    # Ensure theme and language session state variables are initialized
    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "Dark Mode"
    if "language" not in st.session_state:
        st.session_state["language"] = "English"

    # Inject Custom CSS (Horizon AI - Calm Exploration Design System)
    theme = st.session_state.get("theme_mode", "Dark Mode")
    if theme == "Light Mode":
        bg_color = "linear-gradient(180deg, #F0F9FF 0%, #E0F2FE 100%)"
        surf_color = "#FFFFFF"
        primary_color = "#2563EB"
        accent_color = "#14B8A6"
        success_color = "#22C55E"
        text_p = "#1E293B"
        text_s = "#64748B"
        border_color = "rgba(37,99,235,0.08)"
        shadow_val = "0 10px 25px rgba(37,99,235,0.05)"
        
        # Sidebar selection colors for Ocean Blue light theme
        nav_selected_bg = primary_color
        nav_selected_color = "#FFFFFF"
        nav_selected_border = "none"
        nav_selected_radius = "12px"
        nav_selected_icon = "#FFFFFF"
    else:
        bg_color = "#0B1220"
        surf_color = "#111827"
        primary_color = "#3B82F6"
        accent_color = "#14B8A6"
        success_color = "#22C55E"
        text_p = "#F9FAFB"
        text_s = "#9CA3AF"
        border_color = "rgba(255,255,255,0.08)"
        shadow_val = "0 10px 30px rgba(0,0,0,0.4)"
        
        # Sidebar selection colors for dark theme
        nav_selected_bg = "rgba(37, 99, 235, 0.08)"
        nav_selected_color = primary_color
        nav_selected_border = f"4px solid {primary_color}"
        nav_selected_radius = "0px 12px 12px 0px"
        nav_selected_icon = primary_color
        
    st.markdown(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        
        <style>
        html, body, .stApp {{
            font-family: 'Inter', sans-serif;
        }}
        h1, h2, h3, h4, h5, h6, .main-title {{
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            color: {text_p} !important;
        }}
        .stApp {{
            background: {bg_color} !important;
            color: {text_p} !important;
        }}
        
        /* Sidebar Restyling */
        [data-testid="stSidebar"] {{
            background-color: {surf_color} !important;
            border-right: 1px solid {border_color} !important;
        }}
        [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
            color: {text_p} !important;
        }}
        .nav-link {{
            border-radius: 12px !important;
            padding: 12px 16px !important;
            color: {text_s} !important;
            font-weight: 500 !important;
            margin: 4px 0 !important;
            transition: all 0.2s ease !important;
        }}
        .nav-link:hover {{
            background-color: rgba(37, 99, 235, 0.05) !important;
            color: {primary_color} !important;
        }}
        .nav-link-selected {{
            background: {nav_selected_bg} !important;
            color: {nav_selected_color} !important;
            font-weight: 600 !important;
            border-left: {nav_selected_border} !important;
            border-radius: {nav_selected_radius} !important;
        }}
        .nav-link i {{
            font-size: 1.15rem !important;
            color: {text_s} !important;
            margin-right: 8px !important;
        }}
        .nav-link-selected i {{
            color: {nav_selected_icon} !important;
        }}
        
        /* Forms & Inputs styling */
        .stTextInput input, .stSelectbox [data-baseweb="select"], .stTextArea textarea {{
            background-color: {surf_color} !important;
            color: {text_p} !important;
            border: 1px solid {border_color} !important;
            border-radius: 14px !important;
            padding: 10px 16px !important;
            font-size: 0.95rem !important;
            transition: all 0.2s ease-in-out !important;
        }}
        .stTextInput input:focus, .stSelectbox [data-baseweb="select"]:focus-within, .stTextArea textarea:focus {{
            border-color: {primary_color} !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
        }}
        
        /* Buttons styling */
        /* Primary Buttons */
        button[data-testid="stBaseButton-primary"] {{
            background: linear-gradient(135deg, {primary_color}, {accent_color}) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
        }}
        button[data-testid="stBaseButton-primary"]:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important;
        }}
        /* Secondary Buttons (Ghost / Outline style) */
        button[data-testid="stBaseButton-secondary"] {{
            background-color: {surf_color} !important;
            color: {primary_color} !important;
                        border: 1px solid {border_color} !important;
            border-radius: 14px !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            transition: all 0.2s ease !important;
        }}
        button[data-testid="stBaseButton-secondary"]:hover {{
            background-color: rgba(37, 99, 235, 0.05) !important;
            border-color: {primary_color} !important;
        }}
        
        /* Cards */
        .glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: {surf_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 20px !important;
            padding: 28px 32px !important;
            margin-bottom: 24px !important;
            box-shadow: {shadow_val} !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        .glass-card:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
            border-color: {primary_color} !important;
        }}
        
        /* Spacing for headers inside cards */
        div[data-testid="stVerticalBlockBorderWrapper"] h3 {{
            margin-top: 0px !important;
            margin-bottom: 20px !important;
        }}
        
        /* Spacing for buttons inside cards */
        div[data-testid="stVerticalBlockBorderWrapper"] button {{
            margin-top: 12px !important;
        }}
        
        .weather-card {{
            background: {surf_color} !important;
            color: {text_p} !important;
            border-radius: 20px !important;
            padding: 20px !important;
            text-align: center;
            border: 1px solid {border_color} !important;
            box-shadow: {shadow_val} !important;
            transition: all 0.3s ease !important;
        }}
        .weather-card:hover {{
            transform: translateY(-5px) !important;
            border-color: {primary_color} !important;
        }}
        
        .booking-card {{
            background: {surf_color} !important;
            color: {text_p} !important;
            border-radius: 16px !important;
            padding: 18px !important;
            margin-bottom: 15px !important;
            border-left: 5px solid {primary_color} !important;
            border-top: 1px solid {border_color} !important;
            border-right: 1px solid {border_color} !important;
            border-bottom: 1px solid {border_color} !important;
            box-shadow: {shadow_val} !important;
            transition: transform 0.2s ease !important;
        }}
        .booking-card:hover {{
            transform: translateX(4px) !important;
        }}
        
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }}
        .grid-card {{
            background: {surf_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 20px !important;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: {shadow_val};
            color: {text_p} !important;
        }}
        .grid-card:hover {{
            border-color: {primary_color} !important;
            transform: translateY(-3px) !important;
        }}
        
        /* Other standard text and labels */
        .stMarkdown, p, span, label {{
            color: {text_p} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Rebrand header: clean, minimal, premium top bar
    hdr_col1, hdr_col2 = st.columns([8, 2])
    with hdr_col1:
        logo_base64 = get_base64_image("trekflow_logo.png")
        if logo_base64:
            st.markdown(f"<div style='display: inline-flex; align-items: center; gap: 10px; font-size: 2.1rem; font-weight: 800; font-family: Poppins; letter-spacing: -0.8px; margin-top: -5px;'><img src='data:image/png;base64,{logo_base64}' style='width: 38px; height: 38px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);'/><span>TrekFlow</span><span style='color: {primary_color}; font-weight: 700; font-size: 1.1rem; padding: 3px 8px; border-radius: 8px; background: rgba(37,99,235,0.08); margin-left: 5px;'>PRO MAX</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='display: inline-flex; align-items: center; gap: 10px; font-size: 2.1rem; font-weight: 800; font-family: Poppins; letter-spacing: -0.8px; margin-top: -5px;'><span>🧳</span><span>TrekFlow</span><span style='color: {primary_color}; font-weight: 700; font-size: 1.1rem; padding: 3px 8px; border-radius: 8px; background: rgba(37,99,235,0.08); margin-left: 5px;'>PRO MAX</span></div>", unsafe_allow_html=True)
    with hdr_col2:
        if st.button("Lock App 🔒", key="btn_global_logout_minimal", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.session_state["user_id"] = None
            st.session_state["vault_key"] = None
            st.session_state["active_menu_index"] = 0
            st.rerun()
    st.markdown(f"<div style='margin-bottom: 20px; border-bottom: 1px solid {border_color};'></div>", unsafe_allow_html=True)

    # Initialize session state variables
    if "destination_city" not in st.session_state:
        st.session_state["destination_city"] = ""
    if "starting_point" not in st.session_state:
        st.session_state["starting_point"] = ""
    if "interests" not in st.session_state:
        st.session_state["interests"] = ""
    if "prev_city" not in st.session_state:
        st.session_state["prev_city"] = ""
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "active_menu_index" not in st.session_state:
        st.session_state["active_menu_index"] = 0

    # Load shared layout variables globally to prevent UnboundLocalError
    days = st.session_state.get("days", 4)
    trip_mood = st.session_state.get("trip_mood", "Relax")

    # ---------------- Query Params Listener & Auto-Sync Hook ----------------
    q_params = st.query_params
    if "city" in q_params and q_params["city"]:
        q_city = q_params["city"]
        q_start = q_params.get("start", "")
        q_action = q_params.get("action", "")
        
        if st.session_state.get("processed_query_city") != q_city:
            st.session_state["processed_query_city"] = q_city
            
            # Check if this trip exists in history
            from src.database.trips_manager import get_user_trips
            user_trips = get_user_trips(st.session_state["user_id"])
            matching_trip = None
            for t in user_trips:
                if t["destination_city"].lower() == q_city.lower():
                    matching_trip = t
                    break
            
            if matching_trip:
                st.session_state["city"] = matching_trip["destination_city"]
                st.session_state["destination_city"] = matching_trip["destination_city"]
                st.session_state["prev_city"] = matching_trip["destination_city"]
                st.session_state["itinerary_text"] = matching_trip["generated_text"]
                st.session_state["total_budget"] = matching_trip["total_budget"]
                st.session_state["num_people"] = matching_trip["num_people"]
                st.session_state["days"] = matching_trip["trip_duration"]
                st.session_state["trip_type"] = matching_trip["trip_type"]
                
                st.session_state["budget_alloc"] = allocate_budget(matching_trip["total_budget"])
                st.session_state["per_person_budget"] = matching_trip["total_budget"] / matching_trip["num_people"]
                st.session_state["travel_type_suggestion"] = suggest_travel_type(st.session_state["per_person_budget"], matching_trip["num_people"])
                st.session_state["micro_mobility_sug"] = suggest_micro_mobility(matching_trip["destination_city"], st.session_state["per_person_budget"] / matching_trip["trip_duration"])
                st.session_state["emergency_intel"] = get_emergency_intel(matching_trip["destination_city"])
                st.session_state["packing_list"] = generate_packing_list(matching_trip["destination_city"], "Relax", matching_trip["trip_duration"])
                st.session_state["smart_alerts"] = generate_smart_alerts(matching_trip["destination_city"])
                
                from src.weather.weather_api import get_city_weather
                weather_data = get_city_weather(matching_trip["destination_city"])
                st.session_state["weather_data"] = weather_data
                st.session_state["instant_weather"] = weather_data
                st.session_state["instant_weather_city"] = matching_trip["destination_city"]
                
                city_lat = weather_data.get("latitude", 20.5937)
                city_lon = weather_data.get("longitude", 78.9629)
                st.session_state["destination_city_info"] = {
                    "name": matching_trip["destination_city"].title(),
                    "latitude": city_lat,
                    "longitude": city_lon
                }
                
                raw_interests = [s.strip() for s in matching_trip["generated_text"].split("\n") if s.strip() and "-" in s][:8]
                spots_info = []
                for spot in raw_interests:
                    offset_lat = (hash(spot) % 100 - 50) * 0.0004
                    offset_lon = (hash(spot) % 1000 % 100 - 50) * 0.0004
                    spots_info.append({
                        "name": spot,
                        "latitude": city_lat + offset_lat,
                        "longitude": city_lon + offset_lon
                    })
                st.session_state["spots_info"] = spots_info
                
                from src.transport.booking_links import get_hotel_recommendations, get_flight_suggestions, get_search_links
                st.session_state["hotels_list"] = get_hotel_recommendations(matching_trip["destination_city"])
                st.session_state["flights_list"] = get_flight_suggestions(matching_trip["destination_city"])
                st.session_state["booking_links"] = get_search_links(matching_trip["destination_city"])
                
                pdft = f"---- TRIP ITINERARY ----\n\n" + matching_trip["generated_text"] + "\n\n"
                st.session_state["final_pdf_text"] = pdft
                
                if q_action == "chat":
                    st.session_state["active_menu_index"] = 7
                else:
                    st.session_state["active_menu_index"] = 2
                st.rerun()
            else:
                st.session_state["destination_city"] = q_city
                st.session_state["starting_point"] = q_start
                st.session_state["days"] = 4
                st.session_state["trip_mood"] = "Relax"
                st.session_state["total_budget"] = 15000
                st.session_state["trip_type"] = "Solo"
                st.session_state["num_people"] = 1
                
                spots = suggest_spots_for_city(q_city)
                st.session_state["spots_pool"] = list(spots)
                st.session_state["selected_spots"] = list(spots)
                st.session_state["prev_city"] = q_city
                
                with st.spinner("🧠 AI Co-Pilot is crafting your personalized itinerary..."):
                    total_budget = 15000
                    num_people = 1
                    days = 4
                    per_person_budget = 15000
                    daily_pp_budget = 3750
                    budget_alloc = allocate_budget(total_budget)
                    travel_type_suggestion = suggest_travel_type(per_person_budget, num_people)
                    micro_mobility_sug = suggest_micro_mobility(q_city, daily_pp_budget)
                    
                    emergency_intel = get_emergency_intel(q_city)
                    packing_list = generate_packing_list(q_city, "Relax", days)
                    smart_alerts = generate_smart_alerts(q_city)
                    
                    from src.core.planner import TravelPlanner
                    from src.core.itinerary_chain import generate_itinerary
                    
                    planner = TravelPlanner()
                    day_wise_spots = planner.split_days(st.session_state["selected_spots"], days)
                    itinerary_text = generate_itinerary(
                        q_city, 
                        day_wise_spots, 
                        start_date=st.session_state.get("start_date"), 
                        trip_mood="Relax"
                    )
                    
                    st.session_state["itinerary_text"] = itinerary_text
                    st.session_state["city"] = q_city
                    st.session_state["budget_alloc"] = budget_alloc
                    st.session_state["total_budget"] = total_budget
                    st.session_state["num_people"] = num_people
                    st.session_state["per_person_budget"] = per_person_budget
                    st.session_state["travel_type_suggestion"] = travel_type_suggestion
                    st.session_state["micro_mobility_sug"] = micro_mobility_sug
                    st.session_state["emergency_intel"] = emergency_intel
                    st.session_state["packing_list"] = packing_list
                    st.session_state["smart_alerts"] = smart_alerts
                    
                    from src.weather.weather_api import get_city_weather
                    weather_data = get_city_weather(q_city)
                    st.session_state["weather_data"] = weather_data
                    st.session_state["instant_weather"] = weather_data
                    st.session_state["instant_weather_city"] = q_city
                    
                    city_lat = weather_data.get("latitude", 20.5937)
                    city_lon = weather_data.get("longitude", 78.9629)
                    st.session_state["destination_city_info"] = {
                        "name": q_city.title(),
                        "latitude": city_lat,
                        "longitude": city_lon
                    }
                    
                    spots_info = []
                    for spot in st.session_state["selected_spots"]:
                        offset_lat = (hash(spot) % 100 - 50) * 0.0004
                        offset_lon = (hash(spot) % 1000 % 100 - 50) * 0.0004
                        spots_info.append({
                            "name": spot,
                            "latitude": city_lat + offset_lat,
                            "longitude": city_lon + offset_lon
                        })
                    st.session_state["spots_info"] = spots_info
                    
                    from src.transport.booking_links import get_hotel_recommendations, get_flight_suggestions, get_search_links
                    st.session_state["hotels_list"] = get_hotel_recommendations(q_city)
                    st.session_state["flights_list"] = get_flight_suggestions(q_city)
                    st.session_state["booking_links"] = get_search_links(q_city)
                    
                    pdft = f"---- TRIP ITINERARY (RELAX VIBE) ----\n\n" + itinerary_text + "\n\n"
                    pdft += "---- BUDGET SUMMARY ----\n"
                    pdft += f"Total: Rs {total_budget} | Per Person: Rs {per_person_budget:.2f}\n\n"
                    pdft += "---- SMART ALERTS ----\n" + "\n".join(smart_alerts)
                    st.session_state["final_pdf_text"] = pdft
                    
                    from src.database.trips_manager import save_generated_trip
                    trip_id = save_generated_trip(
                        user_id=st.session_state["user_id"],
                        destination_city=q_city,
                        trip_duration=days,
                        total_budget=total_budget,
                        trip_type="Solo",
                        num_people=num_people,
                        generated_text=itinerary_text
                    )
                    st.session_state["trip_id"] = trip_id
                    
                    if q_action == "chat":
                        st.session_state["active_menu_index"] = 7
                    else:
                        st.session_state["active_menu_index"] = 2
                    st.rerun()

    # ---------------- Sidebar Navigation ----------------
    from streamlit_option_menu import option_menu
    
    with st.sidebar:
        # Sidebar Logo
        logo_base64 = get_base64_image("trekflow_logo.png")
        if logo_base64:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px; padding-left: 5px;">
                    <img src="data:image/png;base64,{logo_base64}" style="width: 32px; height: 32px; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.15);"/>
                    <div>
                        <div style="font-size: 1.25rem; font-weight: 700; font-family: Poppins; line-height: 1.1; color: {primary_color};">TrekFlow</div>
                        <div style="font-size: 0.75rem; font-weight: 600; color: {text_s}; text-transform: uppercase; letter-spacing: 0.5px;">Pro Max</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px; padding-left: 5px;">
                    <span style="font-size: 1.8rem; filter: drop-shadow(0 4px 6px rgba(37,99,235,0.15));">💼</span>
                    <div>
                        <div style="font-size: 1.25rem; font-weight: 700; font-family: Poppins; line-height: 1.1; color: {primary_color};">TrekFlow</div>
                        <div style="font-size: 0.75rem; font-weight: 600; color: {text_s}; text-transform: uppercase; letter-spacing: 0.5px;">Pro Max</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        avatar = st.session_state.get("avatar", "🎒")
        username = st.session_state.get("username", "Traveler")
        display_name = st.session_state.get("fullname") or username
        
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 25px; padding: 12px; border-radius: 16px; background: rgba(0, 0, 0, 0.02); border: 1px solid {border_color};">
                <span style="font-size: 2.2rem; filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.05));">{avatar}</span>
                <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    <div style="font-size: 0.75rem; opacity: 0.7; color: {text_s}; font-weight: 500;">Logged in as</div>
                    <div style="font-size: 0.95rem; font-weight: 700; color: {text_p};" title="{display_name}">{display_name}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(f"<div style='font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: {text_s}; margin-bottom: 10px;'>🗺️ Navigation</div>", unsafe_allow_html=True)
        default_idx = st.session_state["active_menu_index"]
        
        # Intercept action from QR code parameters
        if "action" in q_params and q_params["action"] == "chat" and "itinerary_text" in st.session_state:
            default_idx = 7
            
        selected_nav = option_menu(
            menu_title=None,
            options=[
                tr("nav_home"),
                tr("nav_plan"),
                tr("nav_itinerary"),
                tr("nav_analytics"),
                tr("nav_bookings"),
                tr("nav_shield"),
                tr("nav_split"),
                tr("nav_copilot"),
                tr("nav_settings"),
                tr("nav_about")
            ],
            icons=["house-door", "compass", "calendar3", "bar-chart-line", "airplane", "shield-lock", "people", "chat-quote", "gear", "info-circle"],
            menu_icon=None,
            default_index=default_idx,
            styles={
                "container": {"padding": "0px!important", "background-color": "transparent"},
                "icon": {"color": text_s, "font-size": "1.15rem"}, 
                "nav-link": {"font-size": "0.95rem", "font-family": "Inter", "text-align": "left", "margin":"4px 0px", "padding": "10px 14px", "border-radius": "12px", "color": text_s, "font-weight": "500"},
                "nav-link-selected": {"background": nav_selected_bg, "color": nav_selected_color, "font-weight": "600", "border-left": nav_selected_border, "border-radius": nav_selected_radius},
            }
        )
        # Reverse translation map back to English
        translation_map_back = {
            tr("nav_home"): "Home Dashboard",
            tr("nav_plan"): "Plan New Trip",
            tr("nav_itinerary"): "Itinerary & Guides",
            tr("nav_analytics"): "Analytics & Eco-Karma",
            tr("nav_bookings"): "Bookings & Stays",
            tr("nav_shield"): "Travel Shield & Vault",
            tr("nav_split"): "Split-Trip Manager",
            tr("nav_copilot"): "AI Co-Pilot",
            tr("nav_settings"): "Settings",
            tr("nav_about"): "About & Privacy"
        }
        english_nav = translation_map_back.get(selected_nav, selected_nav)
        
        # Save active index
        nav_options = [
            "Home Dashboard",
            "Plan New Trip",
            "Itinerary & Guides",
            "Analytics & Eco-Karma",
            "Bookings & Stays",
            "Travel Shield & Vault",
            "Split-Trip Manager",
            "AI Co-Pilot",
            "Settings",
            "About & Privacy"
        ]
        st.session_state["active_menu_index"] = nav_options.index(english_nav)
        selected_nav = english_nav
        
    st.sidebar.markdown("---")

# ---------------- Sidebar API Settings ----------------
    with st.sidebar.expander("🔑 API Configuration", expanded=False):
        if "groq_api_key" not in st.session_state:
            st.session_state["groq_api_key"] = ""
        groq_api_key_input = st.text_input(
            "GROQ API Key", 
            type="password", 
            value=st.session_state["groq_api_key"],
            help="Enter your Groq API Key to query the LLM. If blank, local curated spots fallback data will be used."
        )
        if groq_api_key_input != st.session_state["groq_api_key"]:
            st.session_state["groq_api_key"] = groq_api_key_input
            from src.chains.ai_suggester import init_llm
            init_llm(groq_api_key_input)
            
    # Optional QR parameter load hook
    if "city" in q_params and st.session_state.get("prev_city", "").lower() != q_params["city"].lower():
        st.session_state["destination_city"] = q_params["city"]
        st.session_state["starting_point"] = q_params.get("start", "")
        st.session_state["auto_generate"] = True

    # ---------------- Auto-generation QR parameter handler ----------------
    if st.session_state.get("auto_generate", False):
        st.session_state["auto_generate"] = False
        city = st.session_state["destination_city"]
        starting_point = st.session_state["starting_point"]
        
        # Load defaults
        days = 4
        trip_mood = "Relax"
        total_budget = 25000
        trip_type = "Solo"
        num_people = 1
        
        # Calculate values
        per_person_budget = total_budget / num_people
        budget_alloc = allocate_budget(total_budget)
        travel_type_suggestion = suggest_travel_type(per_person_budget, num_people)
        micro_mobility_sug = suggest_micro_mobility(city, per_person_budget / days)
        
        raw_interests = suggest_spots_for_city(city)
        st.session_state["spots_pool"] = list(raw_interests)
        st.session_state["selected_spots"] = list(raw_interests)
        st.session_state["prev_city"] = city
        mood_interests = process_mood(trip_mood, raw_interests)
        
        emergency_intel = get_emergency_intel(city)
        packing_list = generate_packing_list(city, trip_mood, days)
        smart_alerts = generate_smart_alerts(city)

        from src.core.planner import TravelPlanner
        from src.core.itinerary_chain import generate_itinerary
        
        planner = TravelPlanner()
        day_wise_spots = planner.split_days(mood_interests, days)
        itinerary_text = generate_itinerary(
            city, 
            day_wise_spots, 
            start_date=st.session_state.get("start_date"), 
            trip_mood=trip_mood
        )

        # Store in session state
        st.session_state["itinerary_text"] = itinerary_text
        st.session_state["city"] = city
        st.session_state["days"] = days
        st.session_state["trip_mood"] = trip_mood
        st.session_state["budget_alloc"] = budget_alloc
        st.session_state["total_budget"] = total_budget
        st.session_state["num_people"] = num_people
        st.session_state["per_person_budget"] = per_person_budget
        st.session_state["travel_type_suggestion"] = travel_type_suggestion
        st.session_state["micro_mobility_sug"] = micro_mobility_sug
        st.session_state["emergency_intel"] = emergency_intel
        st.session_state["packing_list"] = packing_list
        st.session_state["smart_alerts"] = smart_alerts

        # Weather
        from src.weather.weather_api import get_city_weather
        weather_data = get_city_weather(city)
        st.session_state["weather_data"] = weather_data
        st.session_state["instant_weather"] = weather_data
        st.session_state["instant_weather_city"] = city

        city_lat = weather_data.get("latitude", 20.5937)
        city_lon = weather_data.get("longitude", 78.9629)
        
        st.session_state["destination_city_info"] = {
            "name": city.title(),
            "latitude": city_lat,
            "longitude": city_lon
        }

        starting_point_info = None
        if starting_point.strip():
            start_w = get_city_weather(starting_point)
            if start_w and "latitude" in start_w:
                starting_point_info = {
                    "name": starting_point.title(),
                    "latitude": start_w["latitude"],
                    "longitude": start_w["longitude"]
                }
        st.session_state["starting_point_info"] = starting_point_info

        spots_info = []
        for spot in raw_interests:
            if len(spot) < 50:
                offset_lat = (hash(spot) % 100 - 50) * 0.0004
                offset_lon = (hash(spot) % 1000 % 100 - 50) * 0.0004
                spots_info.append({
                    "name": spot,
                    "latitude": city_lat + offset_lat,
                    "longitude": city_lon + offset_lon
                })
        st.session_state["spots_info"] = spots_info

        from src.transport.booking_links import get_hotel_recommendations, get_flight_suggestions, get_search_links
        st.session_state["hotels_list"] = get_hotel_recommendations(city)
        st.session_state["flights_list"] = get_flight_suggestions(city)
        st.session_state["booking_links"] = get_search_links(city)

        pdft = f"---- TRIP ITINERARY ({trip_mood.upper()} VIBE) ----\n\n" + itinerary_text + "\n\n"
        pdft += "---- BUDGET SUMMARY ----\n"
        pdft += f"Total: Rs {total_budget} | Per Person: Rs {per_person_budget:.2f}\n\n"
        pdft += "---- SMART ALERTS ----\n" + "\n".join(smart_alerts)
        st.session_state["final_pdf_text"] = pdft
        
        from src.database.trips_manager import save_generated_trip
        trip_id = save_generated_trip(
            user_id=st.session_state["user_id"],
            destination_city=city,
            trip_duration=days,
            total_budget=total_budget,
            trip_type=trip_type,
            num_people=num_people,
            generated_text=itinerary_text
        )
        st.session_state["trip_id"] = trip_id
        st.session_state["active_menu_index"] = 2 # Switch directly to Itinerary view
        st.rerun()

    # ---------------- Display Selected Page Content ----------------
    if selected_nav == "Home Dashboard":
        render_notification_header()
        
        # Load user history from database
        from src.database.trips_manager import get_user_trips
        trips = get_user_trips(st.session_state["user_id"])
        
        # Sum up stats
        total_trips = len(trips)
        total_karma = sum([100 for t in trips]) # 100 base karma points per saved trip!
        
        # Dynamic time-based greeting
        import datetime
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "Good Morning"
        elif hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
            
        display_name = st.session_state.get("fullname") or st.session_state.get("username", "Traveler")
        
        # 1. Top Hero Section with Greeting and Search Input
        st.markdown(
            f"""
            <div class="glass-card" style="background: linear-gradient(135deg, rgba(37,99,235,0.06) 0%, rgba(20,184,166,0.06) 100%); border: 1px solid {border_color}; margin-top: 10px; padding: 25px; display: flex; align-items: center; gap: 15px;">
                <span style="font-size: 2.2rem; filter: drop-shadow(0 4px 6px rgba(37,99,235,0.2));">🧳</span>
                <div>
                    <h3 style="margin: 0; font-size: 1.35rem; font-weight: 700;">Welcome back, {display_name}! Ready for your next adventure?</h3>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 2. Hero Search Input
        hero_search = st.text_input("🔍 Search a city to instantly start planning (e.g. Paris, Goa, Tokyo, Mumbai)...", key="hero_search_input", placeholder="Enter city name...")
        if hero_search.strip():
            st.session_state["destination_city"] = hero_search.strip()
            st.session_state["active_menu_index"] = 1 # Redirect to Plan New Trip
            st.rerun()
            
        st.markdown("---")
        
        # 3. Quick Actions
        st.markdown("### ⚡ Quick Actions")
        qa_cols = st.columns(4)
        with qa_cols[0]:
            if st.button("✈️ Plan Trip", use_container_width=True, key="qa_plan_trip"):
                st.session_state["active_menu_index"] = 1
                st.rerun()
        with qa_cols[1]:
            if st.button("🔒 Vault Locker", use_container_width=True, key="qa_vault"):
                st.session_state["active_menu_index"] = 5
                st.rerun()
        with qa_cols[2]:
            if st.button("📊 Eco-Karma", use_container_width=True, key="qa_analytics"):
                st.session_state["active_menu_index"] = 3
                st.rerun()
        with qa_cols[3]:
            if st.button("💬 Co-Pilot Chat", use_container_width=True, key="qa_copilot"):
                st.session_state["active_menu_index"] = 7
                st.rerun()
                
        st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
        
        # 4. Your Travel Overview (3 horizontal cards)
        st.markdown("### 🗺️ Your Travel Overview")
        ov_cols = st.columns(3)
        with ov_cols[0]:
            st.markdown(
                f"""
                <div class="glass-card" style="text-align: center; padding: 25px; margin-bottom: 15px;">
                    <span style="font-size: 2.2rem; filter: drop-shadow(0 4px 6px rgba(37,99,235,0.15));">✈️</span>
                    <div style="font-weight: 600; margin-top: 10px; font-size: 0.95rem; color: {text_s};">Trips Planned</div>
                    <div style="font-size: 2rem; color: {primary_color}; font-weight: 800; margin-top: 5px;">{total_trips}</div>
                    <div style="font-size: 0.85rem; color: {primary_color}; font-weight: 500; margin-top: 5px; cursor: pointer;">View all trips</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with ov_cols[1]:
            st.markdown(
                f"""
                <div class="glass-card" style="text-align: center; padding: 25px; margin-bottom: 15px;">
                    <span style="font-size: 2.2rem; filter: drop-shadow(0 4px 6px rgba(34,197,94,0.15));">🌿</span>
                    <div style="font-weight: 600; margin-top: 10px; font-size: 0.95rem; color: {text_s};">Eco-Karma Level</div>
                    <div style="font-size: 2rem; color: {success_color}; font-weight: 800; margin-top: 5px;">{total_karma} Points</div>
                    <div style="font-size: 0.85rem; color: {success_color}; font-weight: 500; margin-top: 5px;">Keep exploring green</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with ov_cols[2]:
            st.markdown(
                f"""
                <div class="glass-card" style="text-align: center; padding: 25px; margin-bottom: 15px;">
                    <span style="font-size: 2.2rem; filter: drop-shadow(0 4px 6px rgba(20,184,166,0.15));">🛡️</span>
                    <div style="font-weight: 600; margin-top: 10px; font-size: 0.95rem; color: {text_s};">Security Status</div>
                    <div style="font-size: 2rem; color: {accent_color}; font-weight: 800; margin-top: 5px;">Protected</div>
                    <div style="font-size: 0.85rem; color: {text_s}; margin-top: 5px;">Your data is safe</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
        
        # 5. Saved Trips History (3 horizontal cards in grid)
        st.markdown("### 📂 Your Saved Trips History")
        if trips:
            cols = st.columns(3)
            # Display latest 3 trips
            for idx, trip in enumerate(reversed(trips[-3:])):
                with cols[idx % 3]:
                    st.markdown(
                        f"""
                        <div class="glass-card" style="text-align: left; padding: 20px; min-height: 180px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 15px;">
                            <div>
                                <div style="font-size: 1.15rem; font-weight: 700; color: {primary_color};">🛫 {trip['destination_city'].title()}</div>
                                <div style="font-size: 0.85rem; margin-top: 10px; line-height: 1.6; color: {text_p};">
                                    📅 <b>Duration:</b> {trip['trip_duration']} Days<br/>
                                    💰 <b>Total Budget:</b> {fmt_currency(trip['total_budget'])}<br/>
                                    👥 <b>Group Size:</b> {trip['num_people']} ({trip.get('trip_type', 'Solo')})
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    # Load button
                    if st.button("📂 Load Itinerary", key=f"load_home_{trip['trip_id']}", use_container_width=True):
                        # Restore variables into session state
                        st.session_state["city"] = trip["destination_city"]
                        st.session_state["prev_city"] = trip["destination_city"]
                        st.session_state["itinerary_text"] = trip["generated_text"]
                        st.session_state["total_budget"] = trip["total_budget"]
                        st.session_state["num_people"] = trip["num_people"]
                        
                        # Re-calculate parameters
                        st.session_state["budget_alloc"] = allocate_budget(trip["total_budget"])
                        st.session_state["per_person_budget"] = trip["total_budget"] / trip["num_people"]
                        st.session_state["travel_type_suggestion"] = suggest_travel_type(st.session_state["per_person_budget"], trip["num_people"])
                        st.session_state["micro_mobility_sug"] = suggest_micro_mobility(trip["destination_city"], st.session_state["per_person_budget"] / trip["trip_duration"])
                        st.session_state["emergency_intel"] = get_emergency_intel(trip["destination_city"])
                        st.session_state["packing_list"] = generate_packing_list(trip["destination_city"], "Relax", trip["trip_duration"])
                        st.session_state["smart_alerts"] = generate_smart_alerts(trip["destination_city"])
                        
                        # Weather
                        from src.weather.weather_api import get_city_weather
                        weather_data = get_city_weather(trip["destination_city"])
                        st.session_state["weather_data"] = weather_data
                        st.session_state["instant_weather"] = weather_data
                        st.session_state["instant_weather_city"] = trip["destination_city"]
                        
                        city_lat = weather_data.get("latitude", 20.5937)
                        city_lon = weather_data.get("longitude", 78.9629)
                        
                        st.session_state["destination_city_info"] = {
                            "name": trip["destination_city"].title(),
                            "latitude": city_lat,
                            "longitude": city_lon
                        }
                        
                        # Spots
                        raw_interests = [s.strip() for s in trip["generated_text"].split("\n") if s.strip() and "-" in s][:8]
                        spots_info = []
                        for spot in raw_interests:
                            offset_lat = (hash(spot) % 100 - 50) * 0.0004
                            offset_lon = (hash(spot) % 1000 % 100 - 50) * 0.0004
                            spots_info.append({
                                "name": spot,
                                "latitude": city_lat + offset_lat,
                                "longitude": city_lon + offset_lon
                            })
                        st.session_state["spots_info"] = spots_info
                        
                        # Recommendations
                        from src.transport.booking_links import get_hotel_recommendations, get_flight_suggestions, get_search_links
                        st.session_state["hotels_list"] = get_hotel_recommendations(trip["destination_city"])
                        st.session_state["flights_list"] = get_flight_suggestions(trip["destination_city"])
                        st.session_state["booking_links"] = get_search_links(trip["destination_city"])
                        
                        # PDF Text
                        pdft = f"---- TRIP ITINERARY ----\n\n" + trip["generated_text"] + "\n\n"
                        st.session_state["final_pdf_text"] = pdft
                        
                        # Redirect
                        st.session_state["active_menu_index"] = 2 # Switch to Itinerary
                        st.success("🔄 Trip loaded successfully!")
                        st.rerun()
        else:
            st.info("You haven't saved any trips yet. Use the 'Plan Trip' action or search above to create your first adventure!")
            
        st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
        
        # 6. Sidebar/Auxiliary Grid: activity, insights, recommendations
        col_timeline, col_insights = st.columns([1, 1])
        with col_timeline:
            st.markdown("### ⏱️ Recent Activity")
            st.markdown(
                f"""
                <div class="glass-card" style="padding: 20px;">
                    <div style="border-left: 2px solid {border_color}; margin-left: 10px; padding-left: 20px;">
                        <div style="position: relative; margin-bottom: 20px;">
                            <div style="position: absolute; left: -27px; top: 2px; width: 12px; height: 12px; border-radius: 50%; background: {primary_color}; border: 2px solid {surf_color};"></div>
                            <div style="font-size: 0.85rem; font-weight: 700;">Safe Vault Setup</div>
                            <div style="font-size: 0.75rem; color: {text_s};">Two-Factor OTP Security active</div>
                        </div>
                        <div style="position: relative; margin-bottom: 20px;">
                            <div style="position: absolute; left: -27px; top: 2px; width: 12px; height: 12px; border-radius: 50%; background: {accent_color}; border: 2px solid {surf_color};"></div>
                            <div style="font-size: 0.85rem; font-weight: 700;">Co-Pilot Integrated</div>
                            <div style="font-size: 0.75rem; color: {text_s};">Real-time SMS/Email alerts linked</div>
                        </div>
                        <div style="position: relative;">
                            <div style="position: absolute; left: -27px; top: 2px; width: 12px; height: 12px; border-radius: 50%; background: {success_color}; border: 2px solid {surf_color};"></div>
                            <div style="font-size: 0.85rem; font-weight: 700;">Eco Level Up</div>
                            <div style="font-size: 0.75rem; color: {text_s};">Earned points for green transit choices</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_insights:
            st.markdown("### 💡 AI Travel Insights")
            st.markdown(
                f"""
                <div class="glass-card" style="padding: 20px; display: flex; flex-direction: column; gap: 15px;">
                    <div style="display: flex; gap: 12px; align-items: start;">
                        <span style="font-size: 1.5rem;">🌿</span>
                        <div>
                            <div style="font-size: 0.85rem; font-weight: 700;">Carbon Savings</div>
                            <div style="font-size: 0.75rem; color: {text_s}; margin-top: 2px; line-height: 1.4;">
                                Your focus on micro-mobility options has avoided an estimated <b>12kg</b> of CO2 emissions.
                            </div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 12px; align-items: start;">
                        <span style="font-size: 1.5rem;">💰</span>
                        <div>
                            <div style="font-size: 0.85rem; font-weight: 700;">Smart Allocator</div>
                            <div style="font-size: 0.75rem; color: {text_s}; margin-top: 2px; line-height: 1.4;">
                                Grouping budgets by category helps save an average of <b>18%</b> on unexpected transit expenses.
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
        
        # 7. AI Recommended Escapes (3 columns grid at bottom)
        st.markdown("### 🌟 AI Recommended Escapes")
        rec_cols = st.columns(3)
        recommendations_list = [
            {"city": "Paris", "desc": "Eiffel Tower & Louvre art museums.", "temp": "22°C ☀️", "cost": "Premium"},
            {"city": "Goa", "desc": "Sun-kissed beaches & watersports.", "temp": "31°C 🏖️", "cost": "Budget"},
            {"city": "Tokyo", "desc": "Modern tech, shrines & cherry blossoms.", "temp": "19°C 🌸", "cost": "Moderate"}
        ]
        
        for idx, item in enumerate(recommendations_list):
            with rec_cols[idx]:
                st.markdown(
                    f"""
                    <div class="glass-card" style="padding: 16px; min-height: 180px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 15px;">
                        <div>
                            <div style="font-size: 1.15rem; font-weight: 700; color: {primary_color};">🛫 {item['city']}</div>
                            <div style="font-size: 0.8rem; margin-top: 6px; line-height: 1.4; color: {text_s};">{item['desc']}</div>
                        </div>
                        <div style="margin-top: 10px; border-top: 1px solid {border_color}; padding-top: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; font-weight: 600;">
                            <span>🌡️ {item['temp']}</span>
                            <span style="color: {accent_color};">{item['cost']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button(f"Explore {item['city']}", key=f"rec_exp_{item['city']}", use_container_width=True):
                    st.session_state["destination_city"] = item["city"]
                    st.session_state["active_menu_index"] = 1
                    st.rerun()

    elif selected_nav == "Plan New Trip":
        st.markdown("## ✈️ Plan a New Adventure")
        st.markdown("Enter your travel details below and let our AI plan the perfect trip for you!")

        # Draw a beautiful glassmorphic container card
        with st.container(border=True):
        
            # 2-column layout for basic info
            col1, col2 = st.columns(2)
        
            with col1:
                starting_point = st.text_input(
                    "Starting Point (Optional)",
                    value=st.session_state.get("starting_point", ""),
                    help="Enter your starting city (e.g. Mumbai, Delhi, Bengaluru) to see destination suggestions."
                )
                st.session_state["starting_point"] = starting_point
            
                # Show suggestions below starting point
                if starting_point.strip():
                    sp_clean = starting_point.strip().lower()
                    STARTING_POINT_RECOMMENDATIONS = {
                        "delhi": [
                            {"city": "Jaipur", "reason": "3h drive | Heritage 🏰"},
                            {"city": "Manali", "reason": "Overnight drive | Mountains 🏔️"},
                            {"city": "Agra", "reason": "2h expressway | Taj Mahal 🕌"},
                            {"city": "Kashmir", "reason": "Short flight | Paradise 🌸"}
                        ],
                        "mumbai": [
                            {"city": "Goa", "reason": "Scenic flight/drive | Beaches 🏖️"},
                            {"city": "Pune", "reason": "3h expressway | Forts ⛰️"},
                            {"city": "Lonavala", "reason": "1.5h drive | Hills 🌧️"},
                            {"city": "Jaipur", "reason": "Short flight | Royal Palace 👑"}
                        ],
                        "bengaluru": [
                            {"city": "Ooty", "reason": "5h drive | Tea Gardens ☕"},
                            {"city": "Coorg", "reason": "5h drive | Coffee Estate 🌲"},
                            {"city": "Mysore", "reason": "2h drive | Heritage 🏰"},
                            {"city": "Goa", "reason": "Short flight | Beaches 🏖️"}
                        ],
                        "kolkata": [
                            {"city": "Darjeeling", "reason": "Overnight train | Tea & Hills 🏔️"},
                            {"city": "Sunderbans", "reason": "3h drive | Tiger Reserve 🐅"},
                            {"city": "Puri", "reason": "Overnight train | Temple & Beach 🌊"},
                            {"city": "Kashmir", "reason": "Flight | Snow & Valley ❄️"}
                        ]
                    }
                    recs = STARTING_POINT_RECOMMENDATIONS.get(sp_clean, [
                        {"city": "Goa", "reason": "Beaches & Nightlife 🏖️"},
                        {"city": "Jaipur", "reason": "Royal Heritage 🏰"},
                        {"city": "Manali", "reason": "Mountains & Snow 🏔️"},
                        {"city": "Kashmir", "reason": "Valleys & Lakes 🌸"}
                    ])
                    st.markdown("<p style='font-size:0.85rem; font-weight:bold; margin-top:5px; margin-bottom:5px;'>💡 Recommended for you:</p>", unsafe_allow_html=True)
                    # Render suggestions in mini columns
                    rec_cols = st.columns(2)
                    for idx, r in enumerate(recs[:4]):
                        with rec_cols[idx % 2]:
                            if st.button(f"👉 {r['city']}", key=f"plan_rec_{r['city']}_{idx}", use_container_width=True, help=r['reason']):
                                st.session_state["destination_city"] = r["city"]
                                st.rerun()

                city = st.text_input("Destination (City Name)", value=st.session_state.get("destination_city", ""))
                st.session_state["destination_city"] = city

                # Weather Card inside page
                if city.strip():
                    if "instant_weather" not in st.session_state or st.session_state.get("instant_weather_city", "").lower() != city.lower():
                        from src.weather.weather_api import get_city_weather
                        with st.spinner("Fetching live weather..."):
                            w_data = get_city_weather(city)
                            st.session_state["instant_weather"] = w_data
                            st.session_state["instant_weather_city"] = city
                
                    w = st.session_state.get("instant_weather")
                    if w and "forecast" in w and len(w["forecast"]) > 0:
                        today = w["forecast"][0]
                        st.markdown(
                            f"""
                            <div class="weather-card" style="padding: 12px; margin-top: 10px; border-radius:10px; background:rgba(30, 144, 255, 0.05); border:1px solid rgba(30, 144, 255, 0.15);">
                                <div style="font-size: 0.85rem; font-weight: bold; color: #1E90FF;">LIVE WEATHER: {city.title()} ({w.get('country', 'India')})</div>
                                <div style="display: flex; align-items: center; justify-content: start; gap: 15px; margin: 8px 0;">
                                    <span style="font-size: 2.2rem; line-height: 1;">{today['emoji']}</span>
                                    <span style="font-size: 1.2rem; font-weight: bold;">{format_temp(today['min_temp'])} - {format_temp(today['max_temp'])}</span>
                                    <span style="font-size: 0.85rem; opacity: 0.8;">{today['condition']}</span>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            with col2:
                import datetime
                today_date = datetime.date.today()
            
                # Start date input
                start_date = st.date_input(
                    "Start Date", 
                    value=st.session_state.get("start_date", today_date),
                    min_value=today_date,
                    help="Select your departure date."
                )
                st.session_state["start_date"] = start_date
            
                # End date input
                end_date = st.date_input(
                    "End Date", 
                    value=st.session_state.get("end_date", start_date + datetime.timedelta(days=3)),
                    min_value=start_date,
                    help="Select your return date. Days limit is unlocked!"
                )
                st.session_state["end_date"] = end_date
            
                # Calculate days dynamically
                days = (end_date - start_date).days + 1
                st.session_state["days"] = days
            
                # Show calculated duration
                st.info(f"📅 Selected Duration: {days} Day(s)")
            
                # Safe mood selector index matching
                saved_mood = st.session_state.get("trip_mood", "Relax")
                mood_options = ["Relax", "Adventure", "Spiritual", "Party"]
                mood_index = mood_options.index(saved_mood) if saved_mood in mood_options else 0
            
                trip_mood = st.selectbox("Trip Mood / Vibe", mood_options, index=mood_index)
                st.session_state["trip_mood"] = trip_mood

                total_budget = st.number_input("Total Budget (INR)", min_value=1000, value=int(st.session_state.get("total_budget", 15000)), step=500)
                st.session_state["total_budget"] = total_budget

                # Safe trip type index matching
                saved_type = st.session_state.get("trip_type", "Solo")
                type_options = ["Solo", "Group", "Family"]
                type_index = type_options.index(saved_type) if saved_type in type_options else 0

                trip_type = st.radio("Trip Type", type_options, index=type_index)
                st.session_state["trip_type"] = trip_type

                num_people = 1
                if trip_type in ["Group", "Family"]:
                    num_people = st.number_input("Number of People", min_value=2, value=max(2, int(st.session_state.get("num_people", 2))))
                st.session_state["num_people"] = num_people

            # Sightseeing Spots Selection
            st.markdown("---")
            st.markdown("### 🎯 Select Sightseeing Spots")
            if "spots_pool" not in st.session_state:
                st.session_state["spots_pool"] = []
            if "selected_spots" not in st.session_state:
                st.session_state["selected_spots"] = []

            if city.strip() and city.lower() != st.session_state.get("prev_city", "").lower():
                spots = suggest_spots_for_city(city)
                st.session_state["spots_pool"] = list(spots)
                st.session_state["selected_spots"] = list(spots)
                st.session_state["prev_city"] = city

            selected_spots = st.multiselect(
                "Choose spots for your itinerary:",
                options=st.session_state["spots_pool"],
                default=st.session_state["selected_spots"]
            )
            st.session_state["selected_spots"] = selected_spots

            # Custom Spot Adder
            col_add1, col_add2 = st.columns([5, 1])
            with col_add1:
                custom_spot = st.text_input("Add Custom Spot:", key="custom_spot_plan_input", placeholder="Type a custom spot name...", label_visibility="collapsed")
            with col_add2:
                if st.button("➕ Add", key="add_spot_plan_btn", use_container_width=True) and custom_spot.strip():
                    new_spot = custom_spot.strip()
                    if new_spot not in st.session_state["spots_pool"]:
                        st.session_state["spots_pool"].append(new_spot)
                    if new_spot not in st.session_state["selected_spots"]:
                        st.session_state["selected_spots"].append(new_spot)
                    st.rerun()

            # Feasibility check
            st.markdown("---")
            feasibility_res = validate_budget(total_budget, days, num_people)
            if not feasibility_res["feasible"]:
                st.error(feasibility_res["message"])
                can_generate = False
            else:
                st.success(feasibility_res["message"])
                can_generate = True


        # Generate Button
        if st.button("✨ Generate AI Smart Plan", key="main_generate_btn", use_container_width=True):
            if not can_generate:
                st.error("Cannot generate itinerary. Please increase your budget to meet the minimum feasibility criteria.")
            elif not city.strip():
                st.error("Please enter a destination city name.")
            else:
                # RUN GENERATION PROCESS DIRECTLY
                with st.spinner("🧠 AI Co-Pilot is crafting your personalized itinerary..."):
                    # Calculate values
                    per_person_budget = total_budget / num_people if num_people > 0 else total_budget
                    daily_pp_budget = per_person_budget / days if days > 0 else 0
                    budget_alloc = allocate_budget(total_budget)
                    travel_type_suggestion = suggest_travel_type(per_person_budget, num_people)
                    micro_mobility_sug = suggest_micro_mobility(city, daily_pp_budget)
                    
                    raw_interests = st.session_state.get("selected_spots", [])
                    mood_interests = process_mood(trip_mood, raw_interests)
                    
                    emergency_intel = get_emergency_intel(city)
                    packing_list = generate_packing_list(city, trip_mood, days)
                    smart_alerts = generate_smart_alerts(city)

                    from src.core.planner import TravelPlanner
                    from src.core.itinerary_chain import generate_itinerary
                    
                    planner = TravelPlanner()
                    day_wise_spots = planner.split_days(mood_interests, days)
                    itinerary_text = generate_itinerary(
                        city, 
                        day_wise_spots, 
                        start_date=st.session_state.get("start_date"), 
                        trip_mood=trip_mood
                    )

                    # Store results in session state
                    st.session_state["itinerary_text"] = itinerary_text
                    st.session_state["city"] = city
                    st.session_state["budget_alloc"] = budget_alloc
                    st.session_state["total_budget"] = total_budget
                    st.session_state["num_people"] = num_people
                    st.session_state["per_person_budget"] = per_person_budget
                    st.session_state["travel_type_suggestion"] = travel_type_suggestion
                    st.session_state["micro_mobility_sug"] = micro_mobility_sug
                    st.session_state["emergency_intel"] = emergency_intel
                    st.session_state["packing_list"] = packing_list
                    st.session_state["smart_alerts"] = smart_alerts

                    # Weather
                    weather_data = st.session_state.get("instant_weather")
                    if not weather_data:
                        from src.weather.weather_api import get_city_weather
                        weather_data = get_city_weather(city)
                    st.session_state["weather_data"] = weather_data

                    city_lat = weather_data.get("latitude", 20.5937)
                    city_lon = weather_data.get("longitude", 78.9629)
                    
                    st.session_state["destination_city_info"] = {
                        "name": city.title(),
                        "latitude": city_lat,
                        "longitude": city_lon
                    }

                    starting_point_info = None
                    if starting_point.strip():
                        from src.weather.weather_api import get_city_weather
                        start_w = get_city_weather(starting_point)
                        if start_w and "latitude" in start_w:
                            starting_point_info = {
                                "name": starting_point.title(),
                                "latitude": start_w["latitude"],
                                "longitude": start_w["longitude"]
                            }
                    st.session_state["starting_point_info"] = starting_point_info

                    spots_info = []
                    for spot in raw_interests:
                        if len(spot) < 50:
                            offset_lat = (hash(spot) % 100 - 50) * 0.0004
                            offset_lon = (hash(spot) % 1000 % 100 - 50) * 0.0004
                            spots_info.append({
                                "name": spot,
                                "latitude": city_lat + offset_lat,
                                "longitude": city_lon + offset_lon
                            })
                    st.session_state["spots_info"] = spots_info

                    from src.transport.booking_links import get_hotel_recommendations, get_flight_suggestions, get_search_links
                    st.session_state["hotels_list"] = get_hotel_recommendations(city)
                    st.session_state["flights_list"] = get_flight_suggestions(city)
                    st.session_state["booking_links"] = get_search_links(city)

                    pdft = f"---- TRIP ITINERARY ({trip_mood.upper()} VIBE) ----\n\n" + itinerary_text + "\n\n"
                    pdft += "---- BUDGET SUMMARY ----\n"
                    pdft += f"Total: Rs {total_budget} | Per Person: Rs {per_person_budget:.2f}\n\n"
                    pdft += "---- SMART ALERTS ----\n" + "\n".join(smart_alerts)
                    st.session_state["final_pdf_text"] = pdft
                    
                    from src.database.trips_manager import save_generated_trip
                    trip_id = save_generated_trip(
                        user_id=st.session_state["user_id"],
                        destination_city=city,
                        trip_duration=days,
                        total_budget=total_budget,
                        trip_type=trip_type,
                        num_people=num_people,
                        generated_text=itinerary_text
                    )
                    st.session_state["trip_id"] = trip_id
                    st.success("✅ AI Trip Plan Generated Successfully!")
                    st.session_state["active_menu_index"] = 2 # Switch directly to Itinerary view
                    st.rerun()

    elif selected_nav == "Itinerary & Guides":
        if "itinerary_text" in st.session_state:
            st.markdown(f"## {days}-Day Itinerary for **{st.session_state['city'].title()}**")
            st.info(f"✨ Geoclustering Applied. Powered by **{trip_mood}** Mood Engine.")
            
            # Weather cards widget
            if "weather_data" in st.session_state and st.session_state["weather_data"]:
                wdata = st.session_state["weather_data"]
                st.markdown(f"#### ⛅ 3-Day Weather Forecast ({wdata.get('country', 'India')})")
                w_cols = st.columns(3)
                for idx, day_forecast in enumerate(wdata["forecast"][:3]):
                    with w_cols[idx]:
                        st.markdown(
                            f"""
                            <div class="weather-card">
                                <div class="weather-date">{day_forecast['date']}</div>
                                <div class="weather-emoji">{day_forecast['emoji']}</div>
                                <div class="weather-temp">{format_temp(day_forecast['min_temp'])} - {format_temp(day_forecast['max_temp'])}</div>
                                <div class="weather-desc">{day_forecast['condition']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                st.write("")
                
            col_text, col_map = st.columns([5, 4])
            with col_text:
                st.markdown(st.session_state["itinerary_text"])
            with col_map:
                st.markdown("### 🗺️ Interactive Route Map (Google Maps Style)")
                if "destination_city_info" in st.session_state:
                    from src.ui.map_renderer import generate_google_map_html
                    import streamlit.components.v1 as components
                    
                    start_info = st.session_state.get("starting_point_info")
                    dest_info = st.session_state.get("destination_city_info")
                    spots_info = st.session_state.get("spots_info", [])
                    
                    map_html = generate_google_map_html(start_info, dest_info, spots_info)
                    components.html(map_html, height=520, scrolling=False)
                else:
                    st.info("Map not available. Please generate a plan first.")
            
            st.markdown("---")
            
            # Local Food & Culinary Guide
            from src.core.fallback_data import get_fallback_culinary
            st.markdown("### 🍲 Local Food & Culinary Guide")
            culinary_list = get_fallback_culinary(st.session_state["city"])
            
            if culinary_list:
                food_cols = st.columns(len(culinary_list))
                for idx, food in enumerate(culinary_list):
                    with food_cols[idx]:
                        st.markdown(
                            f"""
                            <div class="grid-card">
                                <div style="font-size:1.5rem;">🍲</div>
                                <div style="font-weight:bold; margin-top:5px; font-size:1.1rem; color:#1E90FF;">{food['food']}</div>
                                <div style="font-size:0.9rem; margin-top:5px;"><b>Famous Spot:</b><br/>{food['spot']}</div>
                                <div style="font-size:0.95rem; font-weight:bold; color:#2e7d32; margin-top:5px;">{food['price']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.write("Culinary guide not available for this city.")
            st.markdown("---")
            
            # Local Phrases language guide
            from src.core.fallback_data import get_fallback_phrases
            st.markdown("### 🗣️ Local Language Helper")
            phrases = get_fallback_phrases(st.session_state["city"])
            
            if phrases:
                phrase_cols = st.columns(len(phrases))
                for idx, p in enumerate(phrases):
                    with phrase_cols[idx]:
                        st.markdown(
                            f"""
                            <div class="grid-card">
                                <div style="font-size:1.5rem;">🗣️</div>
                                <div style="font-weight:bold; margin-top:5px; font-size:1rem; color:#1E90FF;">{p['phrase']}</div>
                                <div style="font-size:1.1rem; font-weight:bold; margin-top:5px; color:#2e7d32;">{p['translation']}</div>
                                <div style="font-size:0.8rem; font-style:italic; opacity:0.8; margin-top:5px;">Pronounce: {p['pronunciation']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            
            st.markdown("---")

            # Interactive Checklist
            st.markdown("### 🎒 Interactive Packing Checklist")
            if "packing_checklist_states" not in st.session_state:
                st.session_state["packing_checklist_states"] = {}
                
            packing_cols = st.columns(3)
            for idx, item in enumerate(st.session_state["packing_list"]):
                with packing_cols[idx % 3]:
                    key = f"chk_{st.session_state['city']}_{item}"
                    checked = st.checkbox(item, value=st.session_state["packing_checklist_states"].get(key, False), key=key)
                    st.session_state["packing_checklist_states"][key] = checked
        else:
            st.markdown("## 🗓️ AI Itineraries & Destination Guides")
            st.markdown("Welcome to the Itinerary Hub! Since you don't have an active trip configured, explore some of our most popular pre-configured destination guides below. **Click one to load it instantly!**")
            
            # Cards for popular cities
            col1, col2, col3 = st.columns(3)
            popular_destinations = [
                {"city": "Goa", "vibe": "Relax", "days": 4, "emoji": "🏖️", "desc": "Sunny beaches, historic churches, and delicious seafood guides."},
                {"city": "Kashmir", "vibe": "Spiritual", "days": 5, "emoji": "🏔️", "desc": "Snow-capped peaks, serene Dal lake shikaras, and heritage tours."},
                {"city": "Mumbai", "vibe": "Adventure", "days": 3, "emoji": "🌆", "desc": "Bustling street life, historic monuments, and marine drive vibes."}
            ]
            
            # Helper to mock-load a popular trip
            for idx, dest in enumerate(popular_destinations):
                cols = [col1, col2, col3]
                with cols[idx]:
                    st.markdown(
                        f"""
                        <div class="grid-card" style="min-height: 180px;">
                            <div style="font-size:2rem;">{dest['emoji']}</div>
                            <div style="font-weight:bold; font-size:1.2rem; color:#1E90FF; margin-top:5px;">{dest['city']}</div>
                            <div style="font-size:0.85rem; opacity:0.8; margin-top:5px;">{dest['desc']}</div>
                            <div style="font-size:0.9rem; font-weight:bold; margin-top:8px;">{dest['days']} Days | {dest['vibe']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if st.button(f"Load {dest['city']} Guide ⚡", key=f"guide_load_{dest['city']}", use_container_width=True):
                        # Set session state to simulate loading
                        st.session_state["city"] = dest["city"]
                        st.session_state["days"] = dest["days"]
                        st.session_state["trip_mood"] = dest["vibe"]
                        st.session_state["num_people"] = 1
                        st.session_state["total_budget"] = 25000.0
                        st.session_state["starting_point"] = "Delhi"
                        
                        # Generate or fetch mock itinerary from core fallback
                        from src.core.fallback_data import get_fallback_phrases, get_fallback_culinary
                        st.session_state["packing_list"] = ["Comfortable Clothes", "Sunscreen", "Camera", "Chargers", "Emergency Contacts"]
                        
                        # Generate mock text
                        st.session_state["itinerary_text"] = f"""
### 🗓️ Day 1: Welcome to {dest['city']}!
- **Morning**: Arrive at the airport/station and check into your lodging. Freshen up and grab a local breakfast.
- **Afternoon**: Visit the city center or local market area. Capture the initial atmosphere.
- **Evening**: Relax at a popular local spot (cafe/beach/viewpoint) and enjoy a delicious dinner.

### 🗓️ Day 2: Signature Highlights
- **Morning**: Explore the primary historical or cultural site of {dest['city']}.
- **Afternoon**: Taste the signature local culinary dishes.
- **Evening**: Take a local ferry, walk, or guided experience to wind down.
"""
                        # Set coordinates for map
                        coords = {"Goa": (15.2993, 74.1240), "Kashmir": (34.0837, 74.7973), "Mumbai": (19.0760, 72.8777)}
                        lat, lon = coords.get(dest["city"], (15.2993, 74.1240))
                        st.session_state["destination_city_info"] = {"latitude": lat, "longitude": lon, "name": dest["city"]}
                        st.session_state["starting_point_info"] = {"latitude": 28.7041, "longitude": 77.1025, "name": "Delhi"}
                        st.session_state["spots_info"] = [
                            {"latitude": lat + 0.02, "longitude": lon - 0.01, "name": "Sightseeing Spot A"},
                            {"latitude": lat - 0.01, "longitude": lon + 0.02, "name": "Sightseeing Spot B"}
                        ]
                        st.success(f"Loaded {dest['city']} trip successfully!")
                        st.rerun()
            
            st.markdown("---")
            st.markdown("### 💡 Why Generate an AI Itinerary?")
            st.markdown(
                """
                - **Customized Day-by-Day schedule** tailored to your travel mood (Relax, Adventure, Spiritual, or Party).
                - **Interactive Route Map** mapping your starting point, destination, and selected hotspots.
                - **Culinary guides** listing the top famous local delicacies, specific eateries, and price ranges.
                - **Local language dictionary** with key useful phrases, phonetic pronunciations, and translations.
                - **Smart weather warning system** adapting the travel advice to live conditions.
                
                *Select ✈️ **Plan New Trip** in the navigation menu to customize your own!*
                """
            )
            if st.button("✈️ Plan A New Trip Now", key="redir_plan_trip_btn", use_container_width=True):
                st.session_state["active_menu_index"] = 1 # Plan New Trip index
                st.rerun()

    elif selected_nav == "Analytics & Eco-Karma":
        if "itinerary_text" in st.session_state:
            st.markdown("## 📊 Gamification & Analytics")
            
            # Calculate carbon footprint and eco-karma points
            from src.core.sustainability import calculate_carbon_footprint
            start_info = st.session_state.get("starting_point_info")
            dest_info = st.session_state.get("destination_city_info")
            
            start_lat = start_info["latitude"] if start_info else None
            start_lon = start_info["longitude"] if start_info else None
            dest_lat = dest_info["latitude"]
            dest_lon = dest_info["longitude"]
            
            st.markdown("### 🌿 Carbon Footprint & Eco-Karma Tracker")
            transport_mode = st.selectbox(
                "Select your main Travel Transit Mode:", 
                ["Flight ✈️", "Cab/Car 🚗", "Bus 🚌", "Train 🚆"],
                help="Compare emissions across transport modes to earn sustainability points."
            )
            
            res = calculate_carbon_footprint(start_lat, start_lon, dest_lat, dest_lon, transport_mode, st.session_state["num_people"])
            
            # Display sustainability dashboard in glowing grid cards
            st.markdown(
                f"""
                <div class="dashboard-grid">
                    <div class="grid-card">
                        <div style="font-size:1.5rem;">📏</div>
                        <div style="font-weight:bold; margin-top:5px;">Travel Distance</div>
                        <div style="font-size:1.3rem; color:#1E90FF; font-weight:bold;">{format_distance(res['distance_km'])}</div>
                    </div>
                    <div class="grid-card">
                        <div style="font-size:1.5rem;">💨</div>
                        <div style="font-weight:bold; margin-top:5px;">CO2 Emissions</div>
                        <div style="font-size:1.3rem; color:#e53935; font-weight:bold;">{res['footprint_kg']} kg</div>
                    </div>
                    <div class="grid-card">
                        <div style="font-size:1.5rem;">🌲</div>
                        <div style="font-weight:bold; margin-top:5px;">Carbon Saved</div>
                        <div style="font-size:1.3rem; color:#2e7d32; font-weight:bold;">{res['savings_kg']} kg</div>
                    </div>
                    <div class="grid-card" style="border-color:#2e7d32;">
                        <div style="font-size:1.5rem;">🌿</div>
                        <div style="font-weight:bold; margin-top:5px;">Eco-Karma Earned</div>
                        <div style="font-size:1.3rem; color:#2e7d32; font-weight:bold;">+{res['karma_points']} Points</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("---")
            
            # Currency Converter
            st.markdown("### 💱 Dynamic Currency Converter")
            target_currencies = {
                "mumbai": "INR", "delhi": "INR", "goa": "INR", "jaipur": "INR", "manali": "INR",
                "london": "GBP", "paris": "EUR", "tokyo": "JPY", "new york": "USD"
            }
            dest_curr = target_currencies.get(st.session_state["city"].lower(), "USD")
            
            amount_inr = st.number_input("Enter Amount to Convert (INR):", min_value=1.0, value=float(st.session_state["total_budget"]))
            
            # Live fetch or fallback
            import requests
            rate = 1.0
            if dest_curr != "INR":
                try:
                    r = requests.get("https://open.er-api.com/v6/latest/INR")
                    if r.status_code == 200:
                        rate = r.json().get("rates", {}).get(dest_curr, 1.0)
                except Exception:
                    fallbacks = {"USD": 0.012, "EUR": 0.011, "GBP": 0.0094, "JPY": 1.85}
                    rate = fallbacks.get(dest_curr, 1.0)
                    
            converted = amount_inr * rate
            currency_symbols = {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "INR": "₹"}
            symbol = currency_symbols.get(dest_curr, "$")
            st.info(f"💰 **Converted Amount:** {symbol}{converted:,.2f} (Rate: 1 INR = {rate:.6f} {dest_curr})")
            
            st.markdown("---")

            st.markdown("### 💼 Budget Allocation & Transport Suggestions")
            col_chart, col_stats = st.columns([5, 4])
            
            with col_chart:
                import pandas as pd
                import plotly.express as px
                
                currency = st.session_state.get("currency", "INR")
                symbols = {"INR": "₹", "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}
                symbol = symbols.get(currency, "₹")
                rates = {"USD": 0.012, "EUR": 0.011, "GBP": 0.0094, "JPY": 1.85, "INR": 1.0}
                rate = rates.get(currency, 1.0)
                
                alloc_dict = st.session_state["budget_alloc"]
                df_budget = pd.DataFrame({
                    "Category": list(alloc_dict.keys()),
                    f"Amount ({symbol})": [v * rate for v in alloc_dict.values()]
                })
                
                fig = px.pie(
                    df_budget,
                    names="Category",
                    values=f"Amount ({symbol})",
                    hole=0.45,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig.update_layout(
                    margin=dict(t=20, b=20, l=10, r=10),
                    height=280,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig, use_container_width=True)
                
            with col_stats:
                st.write("Your budget is automatically allocated according to travel advisory standards:")
                for k, v in st.session_state["budget_alloc"].items():
                    st.write(f"- **{k}**: {fmt_currency(v)}")
                st.write("")
                st.write(f"**Travel Type**: {st.session_state['travel_type_suggestion']['type']} ({st.session_state['travel_type_suggestion']['description']})")
                st.write(f"**Local Commute**: {st.session_state['micro_mobility_sug']}")
        else:
            st.markdown("## 📊 Gamification & Analytics Hub")
            st.markdown("Welcome to the Analytics dashboard! Since you don't have an active trip loaded, you can still test out our sustainability calculator and live currency converter below.")
            
            # Standalone Currency Converter
            st.markdown("### 💱 Quick Currency Converter")
            c_col1, c_col2, c_col3 = st.columns([3, 3, 4])
            with c_col1:
                src_curr = st.selectbox("Source Currency:", ["INR", "USD", "EUR", "GBP", "JPY"], index=0, key="std_src_curr")
            with c_col2:
                target_currencies_list = ["USD", "EUR", "GBP", "JPY", "INR"]
                target_default = "USD" if src_curr == "INR" else "INR"
                tgt_curr = st.selectbox("Target Currency:", target_currencies_list, index=target_currencies_list.index(target_default), key="std_tgt_curr")
            with c_col3:
                conv_amount = st.number_input("Amount to Convert:", min_value=1.0, value=100.0, key="std_conv_amount")
                
            # Fetch conversion
            import requests
            rate = 1.0
            if src_curr != tgt_curr:
                try:
                    r = requests.get(f"https://open.er-api.com/v6/latest/{src_curr}")
                    if r.status_code == 200:
                        rate = r.json().get("rates", {}).get(tgt_curr, 1.0)
                except Exception:
                    # fallbacks for offline testing
                    fallbacks = {
                        "INR": {"USD": 0.012, "EUR": 0.011, "GBP": 0.0094, "JPY": 1.85},
                        "USD": {"INR": 83.5, "EUR": 0.92, "GBP": 0.78, "JPY": 155.0}
                    }
                    rate = fallbacks.get(src_curr, {}).get(tgt_curr, 1.0)
            
            converted_amount = conv_amount * rate
            currency_symbols = {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "INR": "₹"}
            st.info(f"💰 **Converted Result:** {currency_symbols.get(tgt_curr, '')}{converted_amount:,.2f} (Rate: 1 {src_curr} = {rate:.6f} {tgt_curr})")
            
            st.markdown("---")
            
            # Standalone Eco-Karma Calculator
            st.markdown("### 🌿 Carbon Footprint & Eco-Karma Calculator")
            st.markdown("Estimate the emissions of any travel distance and earn hypothetical Eco-Karma points!")
            
            e_col1, e_col2, e_col3 = st.columns([3, 3, 4])
            with e_col1:
                test_dist = st.number_input("Travel Distance (km):", min_value=1.0, value=500.0, key="std_test_dist")
            with e_col2:
                test_transit = st.selectbox("Transit Mode:", ["Flight ✈️", "Cab/Car 🚗", "Bus 🚌", "Train 🚆"], index=3, key="std_test_transit")
            with e_col3:
                test_people = st.number_input("Number of People:", min_value=1, value=1, key="std_test_people")
                
            # Carbon logic
            from src.core.sustainability import calculate_carbon_footprint
            res = calculate_carbon_footprint(0, 0, 0, test_dist/111.0, test_transit, test_people) # Mock coordinates using simple lat diff
            
            st.markdown(
                f"""
<div class="dashboard-grid">
                    <div class="grid-card">
                        <div style="font-size:1.5rem;">📏</div>
                        <div style="font-weight:bold; margin-top:5px;">Distance Entered</div>
                        <div style="font-size:1.3rem; color:#1E90FF; font-weight:bold;">{format_distance(test_dist)}</div>
                    </div>
                    <div class="grid-card">
                        <div style="font-size:1.5rem;">💨</div>
                        <div style="font-weight:bold; margin-top:5px;">Est. CO2 Emissions</div>
                        <div style="font-size:1.3rem; color:#e53935; font-weight:bold;">{res['footprint_kg']} kg</div>
                    </div>
                    <div class="grid-card">
                        <div style="font-size:1.5rem;">🌲</div>
                        <div style="font-weight:bold; margin-top:5px;">Emissions Saved (vs Flight)</div>
                        <div style="font-size:1.3rem; color:#2e7d32; font-weight:bold;">{res['savings_kg']} kg</div>
                    </div>
                    <div class="grid-card" style="border-color:#2e7d32;">
                        <div style="font-size:1.5rem;">🌿</div>
                        <div style="font-weight:bold; margin-top:5px;">Eco-Karma Points</div>
                        <div style="font-size:1.3rem; color:#2e7d32; font-weight:bold;">+{res['karma_points']} Points</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    elif selected_nav == "Bookings & Stays":
        if "itinerary_text" in st.session_state:
            st.markdown("## 🏨 Lodging & Travel Bookings")
            st.write("Compare curated hotel options and hub flight details below. Use the real-time search links to finalize your bookings.")
            
            links = st.session_state["booking_links"]
            
            st.markdown("### ✈️ Flights from Major Hubs")
            f_cols = st.columns(3)
            for idx, flight in enumerate(st.session_state["flights_list"]):
                with f_cols[idx]:
                    st.markdown(
                        f"""
                        <div class="booking-card" style="border-left-color: #1E90FF;">
                            <div class="booking-header">
                                <span>✈️ {flight['from']} → {flight['to']}</span>
                            </div>
                            <div style="margin-top: 8px; font-size: 0.9rem;">
                                <strong>Type:</strong> {flight['type']}<br/>
                                <strong>Duration:</strong> {flight['duration']}<br/>
                                <strong>Est. Price:</strong> <span class="booking-cost">{flight['cost']}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            st.markdown(f'<a href="{links["google_flights"]}" target="_blank" style="text-decoration:none;"><button style="background: linear-gradient(135deg, #1E90FF, #8A2BE2); color:white; border:none; padding:8px 16px; border-radius:6px; font-weight:bold; cursor:pointer;">Search Flights on Google Flights ✈️</button></a>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown("### 🏨 Curated Stays & Hotels")
            h_cols = st.columns(3)
            for idx, hotel in enumerate(st.session_state["hotels_list"]):
                with h_cols[idx]:
                    st.markdown(
                        f"""
                        <div class="booking-card">
                            <div class="booking-header">
                                <span>{hotel['name']}</span>
                                <span class="booking-rating">{hotel['rating']}</span>
                            </div>
                            <div style="margin-top: 8px; font-size: 0.9rem; min-height: 80px;">
                                <strong>Tier:</strong> {hotel['tier']}<br/>
                                <strong>Price:</strong> <span class="booking-cost">{hotel['cost']}</span><br/>
                                <strong>Amenities:</strong> {hotel['amenities']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                st.markdown(f'<a href="{links["booking_hotels"]}" target="_blank" style="text-decoration:none;"><button style="background: linear-gradient(135deg, #003580, #006ce4); color:white; border:none; padding:8px 16px; border-radius:6px; font-weight:bold; cursor:pointer; width:100%;">Search Hotels on Booking.com 🏨</button></a>', unsafe_allow_html=True)
            with btn_col2:
                st.markdown(f'<a href="{links["mmt_hotels"]}" target="_blank" style="text-decoration:none;"><button style="background: linear-gradient(135deg, #e53935, #b71c1c); color:white; border:none; padding:8px 16px; border-radius:6px; font-weight:bold; cursor:pointer; width:100%;">Search Hotels on MakeMyTrip 🧳</button></a>', unsafe_allow_html=True)
        else:
            st.markdown("## 🏨 Lodging & Travel Bookings Hub")
            st.markdown("Compare flight options and hotel availability globally. Fill out your requirements below to get direct booking redirection links!")
            
            b_col1, b_col2, b_col3 = st.columns(3)
            with b_col1:
                b_start = st.text_input("From City:", value="Delhi", placeholder="e.g. Mumbai, Delhi", key="std_b_start")
            with b_col2:
                b_dest = st.text_input("To City:", value="Goa", placeholder="e.g. Goa, Paris", key="std_b_dest")
            with b_col3:
                b_tier = st.selectbox("Hotel Preference:", ["Luxury Stays ⭐⭐⭐⭐⭐", "Mid-Range Comfort ⭐⭐⭐", "Budget Hostels ⭐"], key="std_b_tier")
                
            # Create dynamic links based on inputs
            import urllib.parse
            q_start = urllib.parse.quote(b_start)
            q_dest = urllib.parse.quote(b_dest)
  
            link_flights = f"https://www.google.com/travel/flights?q=Flights%20from%20{q_start}%20to%20{q_dest}"
            link_booking = f"https://www.booking.com/searchresults.html?ss={q_dest}"
            link_mmt = f"https://www.makemytrip.com/hotels/hotel-listing/?dest={q_dest}"
            
            st.markdown("---")
            st.markdown("### ✈️ Flight Booking Redirector")
            st.write(f"Compare and book flight tickets from **{b_start.title()}** to **{b_dest.title()}** on official platforms:")
            st.markdown(f'<a href="{link_flights}" target="_blank" style="text-decoration:none;"><button style="background: linear-gradient(135deg, #1E90FF, #8A2BE2); color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer;">Search Flights on Google Flights ✈️</button></a>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 🏨 Hotel Stays Redirector")
            st.write(f"Compare and book hotels in **{b_dest.title()}** matching **{b_tier}**:")
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                st.markdown(f'<a href="{link_booking}" target="_blank" style="text-decoration:none;"><button style="background: linear-gradient(135deg, #003580, #006ce4); color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer; width:100%;">Search Hotels on Booking.com 🏨</button></a>', unsafe_allow_html=True)
            with btn_col2:
                st.markdown(f'<a href="{link_mmt}" target="_blank" style="text-decoration:none;"><button style="background: linear-gradient(135deg, #e53935, #b71c1c); color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer; width:100%;">Search Hotels on MakeMyTrip 🧳</button></a>', unsafe_allow_html=True)

    elif selected_nav == "Travel Shield & Vault":
        st.markdown("## 🛡️ Travel Security Shield")
        
        # Destination scams widget
        from src.core.fallback_data import get_fallback_scams
        active_city = st.session_state.get("city", "Mumbai")
        st.markdown(f"### 🚨 Tourist Scam & Trap Shield ({active_city.title()})")
        scams = get_fallback_scams(active_city)
        for s in scams:
            st.warning(f"⚠️ **{s['scam']}:** {s['description']}")
            
        st.markdown("---")
        
        # Cyber Alerts grid
        st.markdown("### 📡 Travel Cyber-Alerts")
        st.markdown(
            """
            <div class="dashboard-grid">
                <div class="grid-card" style="border-color:#b71c1c;">
                    <div style="font-size:1.5rem;">📶</div>
                    <div style="font-weight:bold; margin-top:5px; color:#e53935;">Public Wi-Fi Warning</div>
                    <div style="font-size:0.85rem; margin-top:5px;">Avoid entering passwords or credit cards on airport or hotel Wi-Fi. Always use a VPN.</div>
                </div>
                <div class="grid-card" style="border-color:#e65100;">
                    <div style="font-size:1.5rem;">💳</div>
                    <div style="font-weight:bold; margin-top:5px; color:#e65100;">RFID Skimming Shield</div>
                    <div style="font-size:0.85rem; margin-top:5px;">Crowded railway stations and transit hubs are risk zones. Use RFID-blocking sleeves for cards and passports.</div>
                </div>
                <div class="grid-card" style="border-color:#0d47a1;">
                    <div style="font-size:1.5rem;">📱</div>
                    <div style="font-weight:bold; margin-top:5px; color:#1E90FF;">Bluetooth Hijack Prevention</div>
                    <div style="font-size:0.85rem; margin-top:5px;">Turn off Bluetooth and AirDrop in crowded terminals to prevent malicious file pushing and scanning.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        # Document Vault Locker
        from src.database.document_locker import add_document, get_documents, delete_document
        st.markdown("### 🔑 Document Locker (Vault)")
        vault_key = None
        is_2fa_verified = st.session_state.get("vault_2fa_verified", False)
        
        if not is_2fa_verified:
            st.markdown(
                """
                <div style="padding: 15px; border-radius: 8px; background: rgba(230, 81, 0, 0.05); border-left: 4px solid #e65100; margin-bottom: 15px;">
                    <strong style="color: #e65100;">🔓 Two-Factor Authentication (2FA) Gate</strong>
                    <div style="font-size: 0.9rem; margin-top: 5px;">Accessing your encrypted passport/ticket vault requires verifying your identity.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            col_otp_btn, col_otp_inp = st.columns([1, 1])
            with col_otp_btn:
                st.write("") 
                st.write("") 
                if st.button("Request 2FA OTP", key="btn_request_vault_2fa_otp", use_container_width=True):
                    import random
                    import datetime
                    otp_code = str(random.randint(100000, 999999))
                    st.session_state["vault_otp"] = otp_code
                    st.session_state["vault_otp_generated_at"] = datetime.datetime.now()
                    
                    log_msg = f"Vault 2FA Verification: Your OTP is {otp_code} (Valid for 5 minutes)."
                    st.session_state["copilot_logs"].insert(0, {
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "type": "💬 SMS/OTP",
                        "details": log_msg
                    })
                    st.toast(f"📱 [Mock SMS] OTP to access Vault: {otp_code}")
                    st.success("📩 OTP generated! Check the mock SMS toast or the Mobile Co-Pilot Transmission log console.")
            
            with col_otp_inp:
                entered_otp = st.text_input("Enter 6-digit OTP:", placeholder="000000", max_chars=6, key="entered_vault_otp")
                if entered_otp:
                    correct_otp = st.session_state.get("vault_otp")
                    if entered_otp == correct_otp:
                        st.session_state["vault_2fa_verified"] = True
                        st.toast("✅ 2FA Verification Successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid OTP. Please try again.")
        else:
            st.markdown(
                """
                <div style="padding: 10px; border-radius: 8px; background: rgba(76, 175, 80, 0.05); border-left: 4px solid #4CAF50; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #4CAF50; font-weight: bold;">✅ Two-Factor Authentication Verified</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            col_k_inp, col_k_lock = st.columns([3, 1])
            with col_k_inp:
                vault_key = st.text_input("Enter Vault Key / PIN:", type="password", key="vault_key_input")
            with col_k_lock:
                st.write("") 
                st.write("") 
                if st.button("Lock Vault 🔒", use_container_width=True, key="btn_lock_vault_now"):
                    st.session_state["vault_2fa_verified"] = False
                    st.session_state["vault_otp"] = None
                    st.toast("🔒 Vault access locked.")
                    st.rerun()
            
            if vault_key:
                docs = get_documents(st.session_state["user_id"], vault_key)
            
                with st.expander("Lock New Document"):
                    doc_title = st.text_input("Document Title (e.g. Passport, Flight Ticket confirmation)")
                    
                    doc_mode = st.radio("Choose Input Type:", ["Text Details", "File Upload"], horizontal=True)
                    
                    doc_content = ""
                    if doc_mode == "Text Details":
                        doc_content = st.text_area("Document Details (Secure content)")
                    else:
                        uploaded_file = st.file_uploader("Upload File (PDF, Images, TXT)", type=["pdf", "png", "jpg", "jpeg", "txt", "docx", "xlsx"])
                        if uploaded_file is not None:
                            if not doc_title:
                                doc_title = uploaded_file.name
                            file_bytes = uploaded_file.read()
                            import base64
                            import mimetypes
                            b64_content = base64.b64encode(file_bytes).decode('utf-8')
                            mime_type = mimetypes.guess_type(uploaded_file.name)[0] or "application/octet-stream"
                            doc_content = f"file:{uploaded_file.name}:{mime_type}:{b64_content}"
                            
                    if st.button("Encrypt & Secure", key="btn_encrypt_secure_doc"):
                        if doc_title and doc_content:
                            if add_document(st.session_state["user_id"], doc_title, doc_content, vault_key):
                                st.success("Document encrypted and locked successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to store document.")
                        else:
                            st.warning("Please fill out both title and content/file.")
                
                if docs:
                    st.write("#### Locked Vault Items:")
                    for d in docs:
                        with st.container():
                            col_doc, col_del = st.columns([8, 2])
                            with col_doc:
                                st.markdown(f"**{d['title']}** (Created: {d['created_at']})")
                                if d["decrypted"]:
                                    content_str = d["content"]
                                    if content_str.startswith("file:"):
                                        try:
                                            parts = content_str.split(":", 3)
                                            filename = parts[1]
                                            mime_type = parts[2]
                                            b64_data = parts[3]
                                            import base64
                                            file_bytes = base64.b64decode(b64_data.encode('utf-8'))
                                            
                                            # Display inline if it's an image
                                            if "image" in mime_type:
                                                st.image(file_bytes, caption=filename, width=300)
                                            
                                            st.download_button(
                                                label=f"Download {filename}",
                                                data=file_bytes,
                                                file_name=filename,
                                                mime=mime_type,
                                                key=f"dl_btn_{d['id']}"
                                            )
                                        except Exception as e:
                                            st.error(f"Error parsing file: {e}")
                                    else:
                                        st.code(content_str)
                                else:
                                    st.error(content_str)
                            with col_del:
                                if st.button("Delete", key=f"del_doc_{d['id']}"):
                                    if delete_document(st.session_state["user_id"], d["id"]):
                                        st.success("Deleted!")
                                        st.rerun()
                            st.markdown("---")
                else:
                    st.write("No documents found in vault.")
                
        # Smart alerts and emergency if plan is generated
        if "itinerary_text" in st.session_state:
            st.markdown("---")
            col_packs, col_emg = st.columns(2)
            
            intel = st.session_state.get("emergency_intel", {})
            
            with col_packs:
                st.markdown("### 🔮 Predictive Trip Alerts")
                st.markdown("### Predictive Trip Alerts")
                for alert in st.session_state["smart_alerts"]:
                    st.warning(alert)
                
                # Render Tourist Support & Embassy Info below alerts to fill the empty space
                if "Tourist Support" in intel or "Embassy/Consular Info" in intel:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 📞 Tourist & Consular Support")
                    st.markdown("### Tourist & Consular Support")
                    tourist_val = intel.get("Tourist Support", "Not available")
                    embassy_val = intel.get("Embassy/Consular Info", "Register with your embassy before departure.")
                    
                    st.markdown(
                        f"""
                        <div class="glass-card" style="padding: 15px; border-left: 4px solid #2563EB; margin-bottom: 15px; border-radius: 8px; background: rgba(37, 99, 235, 0.03); border: 1px solid rgba(37, 99, 235, 0.1); border-left: 4px solid #2563EB;">
                            <strong style="color: #2563EB; font-size: 0.95rem;">🌐 Official Tourism Helpline</strong>
                            <strong style="color: #2563EB; font-size: 0.95rem;">Official Tourism Helpline</strong>
                            <div style="font-size: 0.9rem; margin-top: 5px; font-weight: 500;">{tourist_val}</div>
                            <hr style="margin: 10px 0; opacity: 0.1;">
                            <strong style="color: #2563EB; font-size: 0.95rem;">🏛️ Embassy / Consular Advisory</strong>
                            <strong style="color: #2563EB; font-size: 0.95rem;">Embassy / Consular Advisory</strong>
                            <div style="font-size: 0.85rem; margin-top: 5px; opacity: 0.85;">{embassy_val}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
            with col_emg:
                st.markdown("### 🚨 Emergency Contacts")
                st.markdown("### Emergency Contacts")
                # Render core physical emergency contacts
                core_keys = ["Nearest Hospital", "Police Station", "Emergency Number", "Safety Tip"]
                for key in core_keys:
                    if key in intel:
                        st.write(f"**{key}**: {intel[key]}")
                        
                # Render any other custom items just in case
                for key, val in intel.items():
                    if key not in core_keys and key not in ["Tourist Support", "Embassy/Consular Info"]:
                        st.write(f"**{key}**: {val}")
                    
                st.markdown(
                    """
                    <div style="margin-top: 15px; padding: 12px; border-radius: 8px; border: 1px solid #ff1744; background: rgba(255, 23, 68, 0.04);">
                        <strong style="color: #ff1744; font-size: 1.0rem;">🚨 SOS Emergency Broadcast Hub</strong>
                        <div style="font-size: 0.8rem; margin-top: 3px; opacity: 0.85;">Trigger an instant location broadcast to local authorities and emergency contacts.</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.write("") 
                
                if st.session_state.get("sos_countdown_active", False):
                    val = st.session_state["sos_countdown_value"]
                    if val > 0:
                        st.error(f"🚨 SOS BROADCAST INITIATED! Sending in {val}s...")
                        if st.button("❌ CANCEL SOS BROADCAST", key="btn_cancel_sos_emergency", type="primary", use_container_width=True):
                            st.session_state["sos_countdown_active"] = False
                            st.session_state["sos_countdown_value"] = 0
                            st.toast("❌ SOS Canceled.")
                            st.rerun()
                        import time
                        time.sleep(1)
                        st.session_state["sos_countdown_value"] = val - 1
                        st.rerun()
                    else:
                        st.session_state["sos_countdown_active"] = False
                        st.session_state["sos_active"] = True
                        
                        import datetime
                        import random
                        lat = round(random.uniform(18.9, 19.1), 6)
                        lon = round(random.uniform(72.8, 73.0), 6)
                        contact_num = st.session_state.get("emergency_contact") or st.session_state.get("mobile_number", "+91 99999 99999")
                        log_msg = f"SOS BROADCASTED! GPS location ({lat}, {lon}) sent to Embassy and emergency contact ({contact_num}). Local emergency units notified."
                        st.session_state["copilot_logs"].insert(0, {
                            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "🚨 SOS",
                            "details": log_msg
                        })
                        st.toast("🚨 EMERGENCY SOS BROADCASTED!")
                        
                        # Trigger simulated mock SMS alert if enabled
                        if st.session_state.get("copilot_sms_enabled", True):
                            sms_text = f"SOS! My current GPS location is ({lat}, {lon}). Please dispatch emergency help immediately!"
                            st.toast(f"📱 [Mock SMS] Sent to {contact_num}: '{sms_text}'")
                            st.session_state["copilot_logs"].insert(0, {
                                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "type": "📱 SMS",
                                "details": f"Simulated SOS SMS dispatched to {contact_num}: '{sms_text}'"
                            })
                            
                        # Trigger simulated mock Email alert if enabled
                        if st.session_state.get("copilot_email_enabled", True):
                            user_email = st.session_state.get("email") or "traveler@trekflow.com"
                            email_text = f"TrekFlow SOS Alert: GPS location ({lat}, {lon})"
                            st.toast(f"✉️ [Mock Email] Sent to {user_email}: '{email_text}'")
                            st.session_state["copilot_logs"].insert(0, {
                                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "type": "✉️ Email",
                                "details": f"Simulated SOS Email dispatched to {user_email}: '{email_text}'"
                            })
                        st.rerun()
                elif st.session_state.get("sos_active", False):
                    st.error("🚨 SOS ACTIVE: Emergency services and contacts have been notified. Keep GPS active.")
                    if st.button("✅ RESOLVE SOS STATUS / STAND DOWN", key="btn_disarm_sos", use_container_width=True):
                        st.session_state["sos_active"] = False
                        st.toast("✅ SOS resolved.")
                        st.rerun()
                else:
                    if st.button("🚨 TRIGGER EMERGENCY SOS", key="btn_trigger_sos_broadcast", type="primary", use_container_width=True):
                        st.session_state["sos_countdown_active"] = True
                        st.session_state["sos_countdown_value"] = 5
                        st.rerun()

    elif selected_nav == "Split-Trip Manager":
        st.markdown("## 👥 Split-Trip Group Expenses")
        col_left, col_right = st.columns([1, 1])
        
        # Check if we have an active trip, otherwise choose from past trips or create a global one
        active_city = st.session_state.get("city")
        if not active_city:
            # Query the user's latest trip or default to a generic trip
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, destination_city FROM trips WHERE user_id=? ORDER BY id DESC LIMIT 1", (st.session_state["user_id"],))
            latest_row = cursor.fetchone()
            conn.close()
            if latest_row:
                trip_id = latest_row[0]
                active_city = latest_row[1]
                st.info(f"💼 Managing expenses for your saved trip: **{active_city.title()}**")
            else:
                trip_id = 1
                active_city = "Global Account"
                st.info("💼 Logged in global account. To split specific travel expenses, generate a plan first!")
        else:
            # Get trip id for active trip
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM trips WHERE user_id=? AND destination_city=? LIMIT 1",
                (st.session_state["user_id"], active_city)
            )
            trip_row = cursor.fetchone()
            if trip_row:
                trip_id = trip_row[0]
            else:
                cursor.execute(
                    "INSERT INTO trips (user_id, destination_city, trip_duration, total_budget, trip_type, num_people) VALUES (?, ?, ?, ?, ?, ?)",
                    (st.session_state["user_id"], active_city, days, st.session_state["total_budget"], "Group", st.session_state["num_people"])
                )
                conn.commit()
                trip_id = cursor.lastrowid
            conn.close()
            st.success(f"👥 Active Trip: **{active_city.title()}**")

        col_left, col_right = st.columns([1, 1])
        # Get settlements and expenses
        from src.database.split_trip import calculate_settlements, get_expenses, delete_expense, add_expense
        res = calculate_settlements(trip_id)
        expenses_history = get_expenses(trip_id)
        
        with col_left:
            st.markdown("### Group Setup & Expense Logger")
            
            # Group members card
            with st.container(border=True):
                st.markdown("##### Configure Group Members")
                default_members = f"{st.session_state['username']}, Partner, Friend"
                members_str = st.text_input("Group Members (comma-separated):", value=default_members, key="group_members_input")
                members = [m.strip() for m in members_str.split(",") if m.strip()]
                
                # Render active member chips
                badge_html = "".join([
                    f'<span style="background: rgba(37, 99, 235, 0.08); color: #2563EB; border: 1px solid rgba(37, 99, 235, 0.15); padding: 5px 12px; border-radius: 20px; margin-right: 6px; font-weight: 600; font-size: 0.8rem; display: inline-block; margin-bottom: 6px;">{m}</span>'
                    for m in members
                ])
                st.markdown(badge_html, unsafe_allow_html=True)
                
            # Log Expense Form
            with st.container(border=True):
                st.markdown("##### Add New Group Expense")
                exp_desc = st.text_input("Expense Description (e.g. Flight Tickets, Seafood Dinner)", placeholder="What was this for?")
                
                col_amt, col_payer = st.columns([1, 1])
                with col_amt:
                    exp_amt = st.number_input("Amount (INR)", min_value=1.0, value=1000.0, step=100.0)
                with col_payer:
                    paid_by = st.selectbox("Paid By:", members)
                    
                split_with = st.multiselect("Split Between:", members, default=members)
                
                if st.button("Log Expense", use_container_width=True):
                    if exp_desc and exp_amt and paid_by and split_with:
                        if add_expense(trip_id, exp_desc, exp_amt, paid_by, split_with):
                            st.success("Expense logged successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to save expense.")
                    else:
                        st.warning("Please fill out all fields.")
                        
            # Group Spend Share Visualization
            if expenses_history:
                with st.container(border=True):
                    st.markdown("##### Group Spend Share")
                    total_spend = sum(exp["amount"] for exp in expenses_history)
                    member_spends = {m: 0.0 for m in members}
                    for exp in expenses_history:
                        payer = exp["paid_by"]
                        if payer in member_spends:
                            member_spends[payer] += exp["amount"]
                            
                    st.markdown(f"**Total Trip Expenditure**: {fmt_currency(total_spend)}")
                    for m in members:
                        m_spend = member_spends.get(m, 0.0)
                        percentage = (m_spend / total_spend * 100) if total_spend > 0 else 0
                        
                        col_lbl, col_val = st.columns([3, 1])
                        with col_lbl:
                            st.write(f"{m}")
                        with col_val:
                            st.write(f"**{percentage:.1f}%**")
                            
                        st.markdown(
                            f"""
                            <div style="background: rgba(0, 0, 0, 0.05); border-radius: 4px; height: 8px; width: 100%; margin-top: -8px; margin-bottom: 12px; overflow: hidden;">
                                <div style="background: linear-gradient(90deg, #2563EB 0%, #14B8A6 100%); height: 8px; border-radius: 4px; width: {percentage}%;"></div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
        with col_right:
            st.markdown("### Balances & Settlements")
            
            # Expense History Card
            with st.container(border=True):
                st.markdown("##### Expense History")
                if expenses_history:
                    for idx, exp in enumerate(expenses_history):
                        col_details, col_action = st.columns([4, 1])
                        with col_details:
                            st.markdown(f"**{exp['description']}**")
                            st.markdown(f"<span style='font-size: 0.8rem; opacity: 0.8;'>Paid: **{fmt_currency(exp['amount'])}** by **{exp['paid_by']}**</span>", unsafe_allow_html=True)
                            st.markdown(f"<span style='font-size: 0.75rem; opacity: 0.6;'>Shared with: {', '.join(exp['split_between'])}</span>", unsafe_allow_html=True)
                        with col_action:
                            st.write("")
                            if st.button("Delete", key=f"del_exp_{exp['id']}"):
                                if delete_expense(trip_id, exp["id"]):
                                    st.success("Deleted!")
                                    st.rerun()
                        st.markdown("<hr style='margin: 8px 0; opacity: 0.1;'>", unsafe_allow_html=True)
                else:
                    st.write("No expenses logged yet.")
                    
            # Net Balances Card
            with st.container(border=True):
                st.markdown("##### Net Balances")
                if not res["balances"]:
                    st.info("No balances to calculate yet.")
                for name, bal in res["balances"].items():
                    if bal > 0:
                        st.markdown(
                            f"""
                            <div style="padding: 8px 12px; border-radius: 6px; background: rgba(34, 197, 94, 0.08); border-left: 4px solid #22C55E; margin-bottom: 8px;">
                                <span style="font-weight: 600; color: #15803D;">{name} is owed: {fmt_currency(bal)}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="padding: 8px 12px; border-radius: 6px; background: rgba(239, 68, 68, 0.08); border-left: 4px solid #EF4444; margin-bottom: 8px;">
                                <span style="font-weight: 600; color: #B91C1C;">{name} owes: {fmt_currency(abs(bal))}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
            # Minimum Settlements Card (with One-click settle)
            with st.container(border=True):
                st.markdown("##### Minimum Settlements")
                if res["settlements"]:
                    for idx, s in enumerate(res["settlements"]):
                        col_s_text, col_s_btn = st.columns([3, 2])
                        with col_s_text:
                            st.markdown(f"**{s['from']}** owes **{fmt_currency(s['amount'])}** to **{s['to']}**")
                        with col_s_btn:
                            if st.button("Settle Debt", key=f"settle_debt_{idx}_{s['from']}_{s['to']}", use_container_width=True):
                                settle_desc = f"Settlement: {s['from']} -> {s['to']}"
                                if add_expense(trip_id, settle_desc, s['amount'], s['from'], [s['to']]):
                                    st.toast(f"Settled {fmt_currency(s['amount'])} from {s['from']} to {s['to']}!")
                                    st.rerun()
                else:
                    st.success("All expenses are perfectly settled!")

    elif selected_nav == "AI Co-Pilot":
        st.markdown("## AI Co-Pilot & Mobile Sync")
        
        chat_col, log_col = st.columns([3, 2])
        
        with chat_col:
            st.markdown("### Travel Assistant Chat")
            if "itinerary_text" in st.session_state:
                st.write("Need changes? Ask me for nearby food, alternative spots, or hidden costs!")
            else:
                st.info("💡 **General Mode Active:** Ask any travel or destination question! To chat about a specific trip, plan one in the 'Plan New Trip' page first.")
                
            for msg in st.session_state["chat_history"]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            # Fetch suggested FAQs for currently active city or General
            active_city = st.session_state.get("city", "General")
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT question, answer FROM city_faqs WHERE LOWER(city_name)=LOWER(?)", (active_city,))
            faqs = cursor.fetchall()
            if not faqs:
                cursor.execute("SELECT question, answer FROM city_faqs WHERE city_name='General'")
                faqs = cursor.fetchall()
            conn.close()
            
            if faqs:
                # Track which questions from the current city have already been asked
                asked_questions = set()
                for msg in st.session_state.get("chat_history", []):
                    if msg["role"] == "user":
                        asked_questions.add(msg["content"].strip().lower().rstrip("?").strip())
                
                # Filter to only keep unasked questions
                available_faqs = []
                for q_text, a_text in faqs:
                    q_clean = q_text.strip().lower().rstrip("?").strip()
                    if q_clean not in asked_questions:
                        available_faqs.append((q_text, a_text))
                
                # Only show up to 3 questions at a time
                available_faqs = available_faqs[:3]
                
                if available_faqs:
                    st.write("")
                    st.markdown(f"**💡 Suggested Questions for {active_city.title() if active_city != 'General' else 'General Travel'}:**")
                    # Render suggested questions as buttons
                    import hashlib
                    for faq_item in available_faqs:
                        q_text, a_text = faq_item
                        q_hash = hashlib.md5(q_text.encode('utf-8')).hexdigest()[:8]
                        if st.button(f"🔍 {q_text}", key=f"faq_btn_{q_hash}_{active_city}", use_container_width=True):
                            st.session_state["chat_history"].append({"role": "user", "content": q_text})
                            st.session_state["chat_history"].append({"role": "assistant", "content": a_text})
                            st.rerun()
                    
            if user_msg := st.chat_input("Type your travel question here..."):
                st.session_state["chat_history"].append({"role": "user", "content": user_msg})
                with st.chat_message("user"):
                    st.markdown(user_msg)
                
                # Check if user message matches any cached FAQ question
                matched_answer = None
                clean_msg = user_msg.strip().lower().rstrip("?").strip()
                for q_text, a_text in faqs:
                    clean_q = q_text.strip().lower().rstrip("?").strip()
                    if clean_msg == clean_q:
                        matched_answer = a_text
                        break
                        
                with st.chat_message("assistant"):
                    if matched_answer:
                        st.markdown(matched_answer)
                        bot_response = matched_answer
                    else:
                        with st.spinner("Thinking..."):
                            from src.chains.chat_assistant import get_chat_response
                            context = st.session_state.get("itinerary_text", "")
                            bot_response = get_chat_response(get_llm_instance(), context, user_msg)
                            st.markdown(bot_response)
                            
                st.session_state["chat_history"].append({"role": "assistant", "content": bot_response})
                st.rerun()
                
        with log_col:
            st.markdown("### Mobile Co-Pilot Console")
            
            # Status Metrics
            st.markdown(
                """
                <div style="padding: 10px; border-radius: 8px; background: rgba(76, 175, 80, 0.05); border: 1px solid #4CAF50; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <span>SMS Dispatcher:</span>
                        <strong style="color: #4CAF50;">● Connected (Sandbox)</strong>
                    </div>
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 5px;">
                        <span>Email Gateway:</span>
                        <strong style="color: #4CAF50;">● Connected (SMTP Mock)</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Log console container
            st.write("📜 **Transmission Logs**")
            logs = st.session_state.get("copilot_logs", [])
            
            if logs:
                log_html = "<div style='max-height: 400px; overflow-y: auto; padding: 10px; border-radius: 6px; background: rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 255, 255, 0.05);'>"
                for entry in logs:
                    log_html += f"""
                    <div style="margin-bottom: 8px; font-size: 0.82rem; border-bottom: 1px solid rgba(255, 255, 255, 0.03); padding-bottom: 4px;">
                        <span style="opacity: 0.5;">[{entry['time']}]</span>
                        <strong style="color: #1E90FF;">{entry['type']}</strong>: 
                        <span>{entry['details']}</span>
                    </div>
                    """
                log_html += "</div>"
                st.markdown(log_html, unsafe_allow_html=True)
            else:
                st.info("No active transmissions. OTP requests, SOS actions, or PDF shares will log details here.")
                
            st.write("") 
            if st.button("Clear Logs", key="btn_clear_copilot_logs", use_container_width=True):
                st.session_state["copilot_logs"] = []
                st.toast("Logs cleared!")
                st.rerun()
            
    elif selected_nav == "Settings":
        st.markdown(f"## {tr('settings_title')}")
        st.markdown(tr('settings_desc'))
        
        # Load user info
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT fullname, email, mobile_number, preferred_style, avatar, bio, currency, temp_unit, dist_unit, security_alerts, weather_warnings, eco_karma_milestones, llm_model FROM users WHERE id=?", (st.session_state["user_id"],))
        user_info = cursor.fetchone()
        conn.close()
        
        if user_info:
            fullname, email, mobile, style, avatar, bio, currency, temp_unit, dist_unit, security_alerts, weather_warnings, eco_karma_milestones, llm_model = user_info
            
            # --- CARD 1: Edit Profile Details ---
            with st.container(border=True):
                st.write(f"### {tr('edit_profile')}")
            
                col_av, col_fields = st.columns([1, 4])
                with col_av:
                    avatars = ["🎒", "✈️", "🌴", "📸", "🗺️", "🕶️", "🚗", "⛵", "🏔️", "🏰"]
                    avatar_val = avatar if avatar in avatars else "🎒"
                    new_avatar = st.selectbox(tr("avatar"), avatars, index=avatars.index(avatar_val), help=tr("avatar_help"))
                    st.markdown(f"<div style='font-size: 4.5rem; text-align: center; margin-top: -10px;'>{new_avatar}</div>", unsafe_allow_html=True)
            
                with col_fields:
                    col1, col2 = st.columns(2)
                    with col1:
                        new_fullname = st.text_input(tr('full_name'), value=fullname or "")
                        new_email = st.text_input(tr('email_address'), value=email or "")
                    with col2:
                        new_mobile = st.text_input(tr('mobile_number'), value=mobile or "")
                        mood_options = ["Relax", "Adventure", "Spiritual", "Party"]
                        style_index = mood_options.index(style) if style in mood_options else 0
                        new_style = st.selectbox(tr('preferred_vibe'), mood_options, index=style_index)
            
                new_bio = st.text_area(tr("bio"), value=bio or "", placeholder=tr("bio_placeholder"), height=90)
                
                if st.button(tr('save_settings'), use_container_width=True):
                    # Update DB
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET fullname=?, email=?, mobile_number=?, preferred_style=?, avatar=?, bio=? WHERE id=?",
                        (new_fullname, new_email, new_mobile, new_style, new_avatar, new_bio, st.session_state["user_id"])
                    )
                    conn.commit()
                    conn.close()
                    st.session_state["avatar"] = new_avatar
                    st.session_state["user_bio"] = new_bio
                    st.success("Profile settings updated successfully!")
                    st.rerun()
            
            # --- CARD 2: App Preferences (Language) ---
            with st.container(border=True):
                st.write("### App Preferences")
            
                saved_lang = st.session_state.get("language", "English")
                lang_options = ["English", "Hindi", "Spanish", "French", "German", "Italian", "Japanese", "Russian"]
                lang_idx = lang_options.index(saved_lang) if saved_lang in lang_options else 0
                selected_lang = st.selectbox(tr('app_lang'), lang_options, index=lang_idx)
                if selected_lang != st.session_state["language"]:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET language=? WHERE id=?", (selected_lang, st.session_state["user_id"]))
                    conn.commit()
                    conn.close()
                    st.session_state["language"] = selected_lang
                    st.rerun()
            
            # --- CARD 3: Regional & Measurement Settings ---
            with st.container(border=True):
                st.write(f"### {tr('regional_settings')}")
            
                reg1, reg2, reg3 = st.columns(3)
                with reg1:
                    saved_curr = st.session_state.get("currency", "INR")
                    curr_options = ["INR", "USD", "EUR", "GBP", "JPY"]
                    curr_idx = curr_options.index(saved_curr) if saved_curr in curr_options else 0
                    selected_currency = st.selectbox("Preferred Currency", curr_options, index=curr_idx)
                    if selected_currency != st.session_state.get("currency"):
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET currency=? WHERE id=?", (selected_currency, st.session_state["user_id"]))
                        conn.commit()
                        conn.close()
                        st.session_state["currency"] = selected_currency
                        st.rerun()
                with reg2:
                    saved_temp = st.session_state.get("temp_unit", "Celsius")
                    temp_options = ["Celsius", "Fahrenheit"]
                    temp_idx = temp_options.index(saved_temp) if saved_temp in temp_options else 0
                    selected_temp = st.selectbox(tr("temp_unit"), temp_options, index=temp_idx)
                    if selected_temp != st.session_state.get("temp_unit"):
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET temp_unit=? WHERE id=?", (selected_temp, st.session_state["user_id"]))
                        conn.commit()
                        conn.close()
                        st.session_state["temp_unit"] = selected_temp
                        st.rerun()
                with reg3:
                    saved_dist = st.session_state.get("distance_unit", "Kilometers")
                    dist_options = ["Kilometers", "Miles"]
                    dist_idx = dist_options.index(saved_dist) if saved_dist in dist_options else 0
                    selected_dist = st.selectbox(tr("dist_unit"), dist_options, index=dist_idx)
                    if selected_dist != st.session_state.get("distance_unit"):
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET dist_unit=? WHERE id=?", (selected_dist, st.session_state["user_id"]))
                        conn.commit()
                        conn.close()
                        st.session_state["distance_unit"] = selected_dist
                        st.rerun()
            
            # --- CARD 4: Notification Preferences ---
            with st.container(border=True):
                st.write(f"### {tr('notification_settings')}")
            
                not1, not2, not3 = st.columns(3)
                with not1:
                    security_val = st.session_state.get("security_alerts", True)
                    new_security = st.toggle(tr("security_alerts"), value=security_val)
                    if new_security != security_val:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET security_alerts=? WHERE id=?", (1 if new_security else 0, st.session_state["user_id"]))
                        conn.commit()
                        conn.close()
                        st.session_state["security_alerts"] = new_security
                        st.rerun()
                with not2:
                    weather_val = st.session_state.get("weather_warnings", True)
                    new_weather = st.toggle(tr("weather_warnings"), value=weather_val)
                    if new_weather != weather_val:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET weather_warnings=? WHERE id=?", (1 if new_weather else 0, st.session_state["user_id"]))
                        conn.commit()
                        conn.close()
                        st.session_state["weather_warnings"] = new_weather
                        st.rerun()
                with not3:
                    eco_val = st.session_state.get("eco_karma_milestones", True)
                    new_eco = st.toggle(tr("eco_karma_milestones"), value=eco_val)
                    if new_eco != eco_val:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET eco_karma_milestones=? WHERE id=?", (1 if new_eco else 0, st.session_state["user_id"]))
                        conn.commit()
                        conn.close()
                        st.session_state["eco_karma_milestones"] = new_eco
                        st.rerun()
            
            # --- CARD 4.5: Mobile Co-Pilot & SOS Settings ---
            with st.container(border=True):
                st.write("### Mobile Co-Pilot & SOS Settings")
            
                em_contact = st.session_state.get("emergency_contact", "")
                sms_en = st.session_state.get("copilot_sms_enabled", True)
                email_en = st.session_state.get("copilot_email_enabled", True)
            
                col_em1, col_em2 = st.columns([2, 2])
                with col_em1:
                    new_em = st.text_input("Emergency Contact Number", value=em_contact, placeholder="+91 99999 99999")
                with col_em2:
                    st.write("") 
                    st.write("") 
                    col_t1, col_t2 = st.columns(2)
                    with col_t1:
                        new_sms = st.toggle("Enable SMS Alerts", value=sms_en)
                    with col_t2:
                        new_email_alerts = st.toggle("Enable Email Alerts", value=email_en)
                    
                if st.button("Save Co-Pilot Settings", key="btn_save_copilot_settings", use_container_width=True):
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET emergency_contact=?, copilot_sms_enabled=?, copilot_email_enabled=? WHERE id=?",
                        (new_em, 1 if new_sms else 0, 1 if new_email_alerts else 0, st.session_state["user_id"])
                    )
                    conn.commit()
                    conn.close()
                    st.session_state["emergency_contact"] = new_em
                    st.session_state["copilot_sms_enabled"] = new_sms
                    st.session_state["copilot_email_enabled"] = new_email_alerts
                
                    # Log the change
                    import datetime
                    log_msg = f"Settings updated: Emergency Contact = {new_em}, SMS = {'Enabled' if new_sms else 'Disabled'}, Email = {'Enabled' if new_email_alerts else 'Disabled'}."
                    st.session_state["copilot_logs"].insert(0, {
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "type": "System",
                        "details": log_msg
                    })
                    st.success("Mobile Co-Pilot settings updated successfully!")
                    st.rerun()
            
            # --- CARD 5: Advanced & API Configuration ---
            with st.container(border=True):
                st.write(f"### {tr('advanced_api_settings')}")
            
                api_col1, api_col2 = st.columns(2)
                with api_col1:
                    saved_key = st.session_state.get("groq_api_key", "")
                    new_key = st.text_input("GROQ API Key", type="password", value=saved_key, help="Enter your Groq API Key to query the LLM. Syncs with the sidebar configuration.")
                    if new_key != saved_key:
                        st.session_state["groq_api_key"] = new_key
                        from src.chains.ai_suggester import init_llm
                        init_llm(new_key, st.session_state.get("llm_model", "llama-3.3-70b-versatile"))
                        st.toast("API Key updated successfully!")
                with api_col2:
                    saved_model = st.session_state.get("llm_model", "llama-3.3-70b-versatile")
                    model_options = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"]
                    model_idx = model_options.index(saved_model) if saved_model in model_options else 0
                    selected_model = st.selectbox(tr("llm_model"), model_options, index=model_idx)
                    if selected_model != saved_model:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET llm_model=? WHERE id=?", (selected_model, st.session_state["user_id"]))
                        conn.commit()
                        conn.close()
                        st.session_state["llm_model"] = selected_model
                        from src.chains.ai_suggester import init_llm
                        init_llm(st.session_state.get("groq_api_key", ""), selected_model)
                        st.success("AI Model preference saved!")
                        st.rerun()
            
            # --- CARD 6: Change PIN Lock ---
            with st.container(border=True):
                from src.auth.auth_manager import is_pin_configured, verify_password, make_password_hash
                
                # Fetch current stored password/pin hash
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT password_hash FROM users WHERE id=?", (st.session_state["user_id"],))
                stored_hash = cursor.fetchone()[0]
                conn.close()
                
                has_pin = is_pin_configured(stored_hash)
                
                if not has_pin:
                    st.write("### 🔒 Set Your 4-Digit Security PIN Lock")
                    st.warning("You are currently using a legacy password profile. Please set a 4-digit numeric PIN to secure your local profile.")
                    p_col1, p_col2 = st.columns(2)
                    with p_col1:
                        new_pin = st.text_input("Set New 4-Digit PIN", type="password", key="settings_new_pin", max_chars=4, placeholder="••••")
                    with p_col2:
                        confirm_pin = st.text_input("Confirm New 4-Digit PIN", type="password", key="settings_confirm_pin", max_chars=4, placeholder="••••")
                        
                    if st.button("Set Security PIN Lock", use_container_width=True):
                        if new_pin and confirm_pin:
                            if not (new_pin.isdigit() and len(new_pin) == 4):
                                st.error("PIN must be exactly 4 numeric digits.")
                            elif new_pin != confirm_pin:
                                st.error("PINs do not match.")
                            else:
                                new_hash = make_password_hash(new_pin)
                                conn = get_connection()
                                cursor = conn.cursor()
                                cursor.execute("UPDATE users SET password_hash=? WHERE id=?", (new_hash, st.session_state["user_id"]))
                                conn.commit()
                                conn.close()
                                st.session_state["vault_key"] = new_pin
                                st.success("PIN Lock set successfully!")
                                st.rerun()
                        else:
                            st.warning("Please fill out both PIN fields.")
                else:
                    st.write("### 🔒 Change 4-Digit Security PIN Lock")
                    p_col1, p_col2 = st.columns(2)
                    with p_col1:
                        curr_pin = st.text_input("Current 4-Digit PIN", type="password", key="settings_curr_pin", max_chars=4, placeholder="••••")
                    with p_col2:
                        new_pin = st.text_input("New 4-Digit PIN", type="password", key="settings_new_pin", max_chars=4, placeholder="••••")
                    
                    if st.button("Update Security PIN Lock", use_container_width=True):
                        if curr_pin and new_pin:
                            if not (curr_pin.isdigit() and len(curr_pin) == 4 and new_pin.isdigit() and len(new_pin) == 4):
                                st.error("PIN must be exactly 4 numeric digits.")
                            else:
                                if verify_password(curr_pin, stored_hash):
                                    new_hash = make_password_hash(new_pin)
                                    conn = get_connection()
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE users SET password_hash=? WHERE id=?", (new_hash, st.session_state["user_id"]))
                                    conn.commit()
                                    conn.close()
                                    st.session_state["vault_key"] = new_pin # Update vault key too
                                    st.success("PIN Lock updated successfully!")
                                    st.rerun()
                                else:
                                    st.error("Incorrect current PIN.")
                        else:
                            st.warning("Please fill out both PIN fields.")
            
            # --- CARD 7: Data Privacy & Account Reset ---
            with st.container(border=True):
                st.write(f"### {tr('data_privacy')}")
            
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.write("📥 **Export Travel Data**")
                    st.write("Download all your travel logs, profile preferences, and trip histories in a standard JSON format.")
                
                    # Dynamic JSON export payload
                    import json
                    from src.database.trips_manager import get_user_trips
                
                    user_trips = get_user_trips(st.session_state["user_id"])
                    export_payload = {
                        "profile": {
                            "username": st.session_state["username"],
                            "fullname": fullname,
                            "email": email,
                            "mobile": mobile,
                            "preferred_vibe": style,
                            "bio": bio,
                            "avatar": avatar
                        },
                        "trips_count": len(user_trips),
                        "saved_trips": [
                            {
                                "trip_id": t["trip_id"],
                                "destination": t["destination_city"],
                                "duration_days": t["trip_duration"],
                                "budget": t["total_budget"],
                                "type": t["trip_type"],
                                "people": t["num_people"]
                            } for t in user_trips
                        ],
                        "app_settings": {
                            "language": st.session_state["language"],
                            "theme_mode": st.session_state["theme_mode"],
                            "currency": currency,
                            "temp_unit": temp_unit,
                            "dist_unit": dist_unit
                        }
                    }
                    json_str = json.dumps(export_payload, indent=4)
                
                    st.download_button(
                        label=tr('export_data'),
                        data=json_str,
                        file_name=f"{st.session_state['username']}_travel_data.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with m_col2:
                    st.write("🧹 **Offline Cache Operations**")
                    st.write("Clear weather responses and LLM suggestions. Forces fresh live updates.")
                
                    if st.button(tr('clear_cache'), use_container_width=True):
                        from src.weather.weather_api import get_city_weather
                        from src.chains.ai_suggester import get_spot_description
                    
                        get_city_weather.clear()
                        suggest_spots_for_city.clear()
                        get_spot_description.clear()
                    
                        st.success("All offline weather and AI suggestion caches cleared successfully!")
            
                st.markdown("<hr style='border-color: rgba(255,0,0,0.2);'/>", unsafe_allow_html=True)
                st.write(f"### {tr('factory_reset')}")
                st.write(tr('reset_warning'))
                confirm_reset = st.checkbox("I understand that this action is permanent and cannot be undone.")
                if st.button(tr('reset_btn'), type="primary", use_container_width=True, disabled=not confirm_reset):
                    # Delete user data from database
                    conn = get_connection()
                    cursor = conn.cursor()
                    # 1. Delete user trips and downstream tables
                    cursor.execute("SELECT id FROM trips WHERE user_id=?", (st.session_state["user_id"],))
                    trips_rows = cursor.fetchall()
                    for trip_row in trips_rows:
                        cursor.execute("DELETE FROM expenses WHERE trip_id=?", (trip_row[0],))
                        cursor.execute("DELETE FROM itineraries WHERE trip_id=?", (trip_row[0],))
                    cursor.execute("DELETE FROM trips WHERE user_id=?", (st.session_state["user_id"],))
                    # 2. Delete document locker
                    cursor.execute("DELETE FROM document_locker WHERE user_id=?", (st.session_state["user_id"],))
                    # 3. Delete user row itself
                    cursor.execute("DELETE FROM users WHERE id=?", (st.session_state["user_id"],))
                    conn.commit()
                    conn.close()
                
                    # Logout session
                    st.session_state["logged_in"] = False
                    st.session_state["username"] = None
                    st.session_state["user_id"] = None
                    st.session_state["vault_key"] = None
                    st.session_state["active_menu_index"] = 0
                    if "user_settings_loaded" in st.session_state:
                        del st.session_state["user_settings_loaded"]
                    st.success("Account successfully wiped and deleted.")
                    st.rerun()
                

    elif selected_nav == "About & Privacy":
        st.markdown("## About & Privacy Policies")
        
        tab_about, tab_privacy = st.tabs(["About TrekFlow", "Privacy & Security"])
        
        with tab_about:
            active_model = st.session_state.get("llm_model", "llama-3.3-70b-versatile")
            st.markdown(
                f"""
                <div class="glass-card">
                    <h3 style="color:#1E90FF;">TrekFlow Pro Max</h3>
                    <p><b>Version:</b> 2.1.0-Pro-Max-Shield</p>
                    <p>TrekFlow Pro Max is a state-of-the-art AI-powered travel assistant that acts as your private co-pilot and security shield. It coordinates planning, routing, sustainability metrics, group budget split, and document vault lock storage all in one local secure app.</p>
                    <hr style="border-color: rgba(255,255,255,0.1);"/>
                    <h4>Key Capabilities:</h4>
                    <ul>
                        <li><b>AI Route Planner:</b> Custom itinerary mapping and live weather checks.</li>
                        <li><b>Gamified Carbon Footprint tracker:</b> Earn Karma points by making green transit choices.</li>
                        <li><b>AES-256 Travel Document Locker:</b> Encrypted vault for passport details and boarding tickets.</li>
                        <li><b>Greedy Debt Settlement:</b> Expenses splits group coordinator.</li>
                        <li><b>Live Currency Exchange:</b> Conversions based on destination country rates.</li>
                    </ul>
                    <hr style="border-color: rgba(255,255,255,0.1);"/>
                    <p style="font-size:0.85rem; opacity:0.7;">Built with ❤️ using Streamlit, LangChain, SQLite, and Python. Powered by {active_model} LLM.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with tab_privacy:
            st.markdown(
                """
                <div class="glass-card">
                    <h3 style="color:#e53935;">Privacy & Security Standards</h3>
                    <p>We treat your travel privacy and credentials with military-grade standards. Here is how your data is handled:</p>
                    <ul>
                        <li><b>Salted Password Hashing:</b> We protect your account credentials using unique random salts and SHA-256 hashing. Clear-text passwords are never stored.</li>
                        <li><b>Local AES-256 Document Lock:</b> Your travel shield vault uses a local military-grade AES-256 CBC cipher. Your master password derives a 256-bit PBKDF2 encryption key. If you forget your password, even we cannot decrypt your vault documents.</li>
                        <li><b>Zero Data Sales:</b> All data, trip histories, and document locker entries remain stored strictly inside your local <code>planner.db</code> SQLite database file. No data is shared with external companies.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    # ---------------- Export PDF Widget ----------------
    if "itinerary_text" in st.session_state and selected_nav in ["Home Dashboard", "Itinerary & Guides", "Analytics & Eco-Karma"]:
        st.markdown("---")
        st.subheader("Export Plan")
        filename = f"{st.session_state['city']}_trip.pdf"
        
        import socket
        import urllib.parse
        
        def get_local_ip():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('8.8.8.8', 1))
                ip = s.getsockname()[0]
                s.close()
                return ip
            except Exception:
                return "127.0.0.1"
                
        local_ip = get_local_ip()
        city_enc = urllib.parse.quote(st.session_state["city"])
        start_enc = urllib.parse.quote(st.session_state.get("starting_point", ""))
        port = st.config.get_option("server.port") or 8501
        qr_url = f"http://{local_ip}:{port}/?city={city_enc}&start={start_enc}&action=chat"
        
        from pdf_generate import generate_pdf
        generate_pdf(
            st.session_state["final_pdf_text"], 
            filename, 
            qr_url=qr_url,
            weather_data=st.session_state.get("weather_data"),
            trip_type=st.session_state.get("trip_type", "Solo"),
            num_people=st.session_state.get("num_people", 1),
            total_budget=st.session_state.get("total_budget", 15000),
            start_date=st.session_state.get("start_date"),
            end_date=st.session_state.get("end_date")
        )
        col_dl, col_sh = st.columns([1, 1])
        with col_dl:
            with open(filename, "rb") as f:
                st.download_button(label="Download PDF Itinerary", data=f, file_name=filename, mime="application/pdf", use_container_width=True)
        with col_sh:
            with st.popover("Share via Email", use_container_width=True):
                target_email = st.text_input("Enter Email(s) (comma separated):", placeholder="partner@example.com")
                if st.button("Send PDF Itinerary", use_container_width=True):
                    if target_email:
                        import datetime
                        log_msg = f"Sent PDF Itinerary '{filename}' to {target_email} successfully."
                        st.session_state["copilot_logs"].insert(0, {
                            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "Email",
                            "details": log_msg
                        })
                        st.success(f"Itinerary shared with {target_email}!")
                    else:
                        st.warning("Please enter at least one email.")

if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Dynamic API key initialization
    if "groq_api_key" not in st.session_state:
        st.session_state["groq_api_key"] = ""
    elif st.session_state["groq_api_key"]:
        from src.chains.ai_suggester import init_llm
        init_llm(st.session_state["groq_api_key"])

    if not st.session_state["logged_in"]:
        show_auth_page()
    else:
        show_main_app()

        