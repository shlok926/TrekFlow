# src/auth/encryption.py
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derives a 256-bit key from a password and a salt using PBKDF2.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, # 256 bits
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_data(password: str, plaintext: str) -> str:
    """
    Encrypts a string using AES-256 CBC mode.
    Returns a base64 encoded string containing: salt (16 bytes) + iv (16 bytes) + ciphertext.
    """
    if not plaintext:
        return ""
    
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # PKCS7 Padding manually
    pad_len = 16 - (len(plaintext) % 16)
    padded_data = plaintext + chr(pad_len) * pad_len
    
    ciphertext = encryptor.update(padded_data.encode('utf-8')) + encryptor.finalize()
    
    # Combine salt, IV and ciphertext
    combined = salt + iv + ciphertext
    return base64.b64encode(combined).decode('utf-8')

def decrypt_data(password: str, encrypted_b64: str) -> str:
    """
    Decrypts a base64 encoded string containing: salt + iv + ciphertext.
    Returns the original plaintext, or None if decryption fails.
    """
    if not encrypted_b64:
        return ""
    
    try:
        combined = base64.b64decode(encrypted_b64.encode('utf-8'))
        if len(combined) < 32: # Salt (16) + IV (16) minimum
            return None
        
        salt = combined[:16]
        iv = combined[16:32]
        ciphertext = combined[32:]
        
        key = derive_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        padded_str = padded_data.decode('utf-8')
        
        # Remove manual PKCS7 padding
        pad_len = ord(padded_str[-1])
        if pad_len < 1 or pad_len > 16:
            return None
        
        # Verify padding character correctness
        for char in padded_str[-pad_len:]:
            if ord(char) != pad_len:
                return None
                
        return padded_str[:-pad_len]
    except Exception:
        return None
