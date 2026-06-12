# src/ui/auth_ui.py
import streamlit as st
from src.auth.auth_manager import get_default_user, verify_password, make_password_hash, is_pin_configured
from src.database.db import get_connection

def _safe_rerun():
    """Support rerun across Streamlit versions."""
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

def show_auth_page():
    # Inject premium Glassmorphism CSS styling
    st.markdown(
        """
        <style>
        /* Gradient background for the login page */
        .stApp {
            background: linear-gradient(135deg, #090615 0%, #110c24 50%, #03020a 100%) !important;
        }

        /* Glassmorphism card styling targeting the st.container(border=True) element */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 20px !important;
            padding: 40px 30px !important;
            box-shadow: 0 8px 32px 0 rgba(138, 43, 226, 0.25) !important;
            max-width: 440px;
            margin: 40px auto !important;
        }

        /* Style input fields inside the glass card */
        div[data-baseweb="input"] {
            background-color: rgba(255, 255, 255, 0.06) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 8px !important;
        }
        
        div[data-baseweb="input"] input {
            color: white !important;
            text-align: center !important;
            letter-spacing: 8px !important;
            font-size: 1.5rem !important;
            font-weight: bold !important;
        }

        /* Glow inputs on focus */
        div[data-baseweb="input"]:focus-within {
            border-color: #8A2BE2 !important;
            box-shadow: 0 0 10px rgba(138, 43, 226, 0.5) !important;
        }

        /* Title styling */
        .auth-title {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 5px;
            background: linear-gradient(135deg, #1E90FF, #8A2BE2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        .auth-subtitle {
            text-align: center;
            color: rgba(255, 255, 255, 0.7) !important;
            margin-bottom: 25px;
            font-weight: 400;
            font-size: 1rem;
        }

        /* Center auth button and style it */
        div.stButton > button {
            background: linear-gradient(135deg, #1E90FF, #8A2BE2) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-weight: bold !important;
            width: 100% !important;
            box-shadow: 0 4px 15px rgba(138, 43, 226, 0.3) !important;
            transition: all 0.3s ease !important;
            margin-top: 15px;
        }

        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(138, 43, 226, 0.5) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    import base64
    logo_base64 = ""
    try:
        with open("trekflow_logo.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        pass
        
    if logo_base64:
        st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'><img src='data:image/png;base64,{logo_base64}' style='width: 90px; height: 90px; border-radius: 20px; box-shadow: 0 8px 24px rgba(138, 43, 226, 0.35);'/></div>", unsafe_allow_html=True)

    st.markdown('<div class="auth-title">TrekFlow Pro Max</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subtitle">AI-Powered Travel Co-Pilot & Security Shield</div>', unsafe_allow_html=True)
    
    # Retrieve/initialize default user profile
    default_user = get_default_user()
    db_pin_hash = default_user["password_hash"]
    
    col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
    with col2:
        with st.container(border=True):
            if db_pin_hash == 'unset' or not is_pin_configured(db_pin_hash):
                st.write("### 🔒 Set Your Security PIN")
                st.info("Set a 4-Digit Security PIN to protect your travel itineraries, documents, and split expenses.")
                
                new_pin = st.text_input("Enter 4-Digit PIN", type="password", key="setup_pin_1", max_chars=4, placeholder="••••")
                confirm_pin = st.text_input("Confirm 4-Digit PIN", type="password", key="setup_pin_2", max_chars=4, placeholder="••••")
                
                if st.button("Set Security PIN", key="btn_set_pin", use_container_width=True):
                    if new_pin and confirm_pin:
                        if not (new_pin.isdigit() and len(new_pin) == 4):
                            st.error("PIN must be exactly 4 numeric digits.")
                        elif new_pin != confirm_pin:
                            st.error("PINs do not match.")
                        else:
                            new_hash = make_password_hash(new_pin)
                            conn = get_connection()
                            cursor = conn.cursor()
                            cursor.execute("UPDATE users SET password_hash=? WHERE id=?", (new_hash, default_user["id"]))
                            conn.commit()
                            conn.close()
                            
                            st.session_state["user_id"] = default_user["id"]
                            st.session_state["username"] = default_user["username"]
                            st.session_state["logged_in"] = True
                            st.session_state["vault_key"] = new_pin
                            st.success("PIN set successfully! Welcome to TrekFlow.")
                            _safe_rerun()
                    else:
                        st.warning("Please fill out both fields.")
            else:
                st.write("### 🔓 Unlock Application")
                st.write("Please enter your 4-digit PIN to access your travel profile.")
                
                entered_pin = st.text_input("Enter 4-Digit PIN", type="password", key="unlock_pin_input", max_chars=4, placeholder="••••")
                
                if st.button("Unlock App", key="btn_unlock_app", use_container_width=True):
                    if entered_pin:
                        if not (entered_pin.isdigit() and len(entered_pin) == 4):
                            st.error("PIN must be exactly 4 numeric digits.")
                        else:
                            if verify_password(entered_pin, db_pin_hash):
                                st.session_state["user_id"] = default_user["id"]
                                st.session_state["username"] = default_user["username"]
                                st.session_state["logged_in"] = True
                                st.session_state["vault_key"] = entered_pin
                                st.success("Access Granted!")
                                _safe_rerun()
                            else:
                                st.error("Incorrect PIN. Please try again.")
                    else:
                        st.warning("Please enter your PIN.")
