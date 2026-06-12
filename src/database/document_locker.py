# src/database/document_locker.py
from src.database.db import get_connection
from src.auth.encryption import encrypt_data, decrypt_data

def add_document(user_id: int, title: str, plain_content: str, vault_key: str) -> bool:
    """
    Encrypts and adds a document to the document locker in the database.
    """
    encrypted_content = encrypt_data(vault_key, plain_content)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO document_locker (user_id, title, encrypted_content) VALUES (?, ?, ?)",
            (user_id, title, encrypted_content)
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def get_documents(user_id: int, vault_key: str) -> list:
    """
    Fetches all documents for a user and attempts to decrypt them.
    Returns a list of dicts: [{'id': int, 'title': str, 'content': str, 'decrypted': bool}]
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, title, encrypted_content, created_at FROM document_locker WHERE user_id=? ORDER BY created_at DESC",
            (user_id,)
        )
        rows = cursor.fetchall()
        
        docs = []
        for r in rows:
            doc_id, title, encrypted_content, created_at = r
            decrypted_content = decrypt_data(vault_key, encrypted_content)
            
            if decrypted_content is not None:
                docs.append({
                    "id": doc_id,
                    "title": title,
                    "content": decrypted_content,
                    "decrypted": True,
                    "created_at": created_at
                })
            else:
                docs.append({
                    "id": doc_id,
                    "title": title,
                    "content": "[DECRYPTION FAILED - INVALID KEY]",
                    "decrypted": False,
                    "created_at": created_at
                })
        return docs
    finally:
        conn.close()

def delete_document(user_id: int, doc_id: int) -> bool:
    """
    Deletes a document from the locker.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM document_locker WHERE user_id=? AND id=?", (user_id, doc_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()
