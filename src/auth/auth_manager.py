# src/auth/auth_manager.py
import hashlib
import secrets
from src.database.db import get_connection

def generate_salt() -> str:
    """Generates a random 16-byte hex salt."""
    return secrets.token_hex(16)

def hash_password_with_salt(password: str, salt: str) -> str:
    """Hashes a password concatenated with salt using SHA-256."""
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def make_password_hash(password: str) -> str:
    """Creates a salted hash string in the format salt$hash."""
    salt = generate_salt()
    pwd_hash = hash_password_with_salt(password, salt)
    return f"{salt}${pwd_hash}"

def verify_password(password: str, stored_hash: str) -> bool:
    """Verifies a password against a stored salted hash or legacy SHA-256 hash."""
    if "$" not in stored_hash:
        # Legacy backward compatibility check
        legacy_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return legacy_hash == stored_hash
    
    salt, pwd_hash = stored_hash.split("$", 1)
    return hash_password_with_salt(password, salt) == pwd_hash

def register_user(username: str, password: str, fullname: str = "", email: str = "", preferred_style: str = "Relax", mobile_number: str = "", auth_provider: str = "local") -> bool:
    """Registers a new user with extended profile options using salted hashing. Returns True if successful."""
    password_hash = make_password_hash(password)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, fullname, email, preferred_style, mobile_number, auth_provider) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, password_hash, fullname, email, preferred_style, mobile_number, auth_provider)
        )
        conn.commit()
        return True
    except Exception:
        # Likely a unique constraint failure on username
        return False
    finally:
        conn.close()

def login_user(username_or_mobile: str, password: str) -> dict:
    """Verifies user credentials using salted hashing. Returns user dict with profile info or None."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, username, password_hash, fullname, email, preferred_style, mobile_number, auth_provider FROM users WHERE username=? OR mobile_number=?", 
            (username_or_mobile, username_or_mobile)
        )
        user = cursor.fetchone()
        if user:
            user_id, uname, stored_hash, fullname, email, pref_style, mobile, provider = user
            if verify_password(password, stored_hash):
                return {
                    "id": user_id, 
                    "username": uname,
                    "fullname": fullname or "",
                    "email": email or "",
                    "preferred_style": pref_style or "Relax",
                    "mobile_number": mobile or "",
                    "auth_provider": provider or "local"
                }
        return None
    finally:
        conn.close()

def get_default_user() -> dict:
    """Gets the default local user from the database. Creates one if none exists."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, username, password_hash, fullname, email, preferred_style, mobile_number FROM users ORDER BY id ASC LIMIT 1")
        user = cursor.fetchone()
        if not user:
            # Create a default traveler user
            # Note: password_hash starts as "unset" to indicate no PIN is set yet.
            cursor.execute(
                "INSERT INTO users (username, password_hash, fullname, email, preferred_style, mobile_number) VALUES (?, ?, ?, ?, ?, ?)",
                ("traveler", "unset", "Traveler", "traveler@trekflow.com", "Relax", "+91 98765 43210")
            )
            conn.commit()
            cursor.execute("SELECT id, username, password_hash, fullname, email, preferred_style, mobile_number FROM users WHERE id=?", (cursor.lastrowid,))
            user = cursor.fetchone()
        
        user_id, uname, pwd_hash, fullname, email, pref_style, mobile = user
        return {
            "id": user_id,
            "username": uname,
            "password_hash": pwd_hash,
            "fullname": fullname or "Traveler",
            "email": email or "traveler@trekflow.com",
            "preferred_style": pref_style or "Relax",
            "mobile_number": mobile or "+91 98765 43210"
        }
    finally:
        conn.close()

def is_pin_configured(stored_hash: str) -> bool:
    """Checks if the stored hash corresponds to a 4-digit numeric PIN."""
    if stored_hash == "unset":
        return False
    # Brute-force 10,000 combinations of 4-digit PINs (0000-9999) to verify
    for i in range(10000):
        candidate = f"{i:04d}"
        if verify_password(candidate, stored_hash):
            return True
    return False
