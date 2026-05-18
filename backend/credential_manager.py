import sqlite3
import os
from cryptography.fernet import Fernet

def get_cipher():
    """Reads or creates a machine-local secret key for password encryption."""
    key_path = os.path.join(os.path.dirname(__file__), "secret.key")
    
    # Automatically generate a secret key file if it doesn't exist yet
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
            
    with open(key_path, "rb") as key_file:
        key = key_file.read()
    return Fernet(key)

def save_credential(portal_name, login_url, username, plaintext_password):
    """Encrypts and securely saves or updates portal credentials in SQLite."""
    cipher = get_cipher()
    encrypted_pw = cipher.encrypt(plaintext_password.encode('utf-8'))
    
    db_path = os.path.join(os.path.dirname(__file__), "jarvis.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portal_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portal_name VARCHAR(100) UNIQUE,
                login_url VARCHAR(1000),
                username VARCHAR(255),
                encrypted_password BLOB
            )
        """)
        
        cursor.execute("""
            INSERT INTO portal_credentials (portal_name, login_url, username, encrypted_password)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(portal_name) DO UPDATE SET
                login_url=excluded.login_url,
                username=excluded.username,
                encrypted_password=excluded.encrypted_password
        """, (portal_name.lower().strip(), login_url, username, encrypted_pw))
        conn.commit()
        return f"Successfully saved credentials for {portal_name}."
    except Exception as e:
        return f"Error saving credentials: {e}"
    finally:
        conn.close()

def get_credential(portal_name):
    """Retrieves and decrypts credentials for a requested portal."""
    db_path = os.path.join(os.path.dirname(__file__), "jarvis.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT login_url, username, encrypted_password FROM portal_credentials WHERE portal_name = ?", (portal_name.lower().strip(),))
        row = cursor.fetchone()
        if not row:
            return None
            
        login_url, username, encrypted_pw = row
        cipher = get_cipher()
        decrypted_pw = cipher.decrypt(encrypted_pw).decode('utf-8')
        
        return {
            "login_url": login_url,
            "username": username,
            "password": decrypted_pw
        }
    except Exception:
        return None
    finally:
        conn.close()