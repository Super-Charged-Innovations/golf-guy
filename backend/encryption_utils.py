"""
GDPR-Compliant Data Encryption Utilities
Handles encryption of sensitive user data in compliance with EU/Swedish data protection laws
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import base64
import os
import hashlib

# Generate or load encryption key (in production, use secure key management service)
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', Fernet.generate_key().decode())

def get_fernet():
    """Get Fernet cipher instance"""
    return Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    """Encrypt sensitive data"""
    if not data:
        return data
    try:
        cipher = get_fernet()
        encrypted = cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return data

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt sensitive data"""
    if not encrypted_data:
        return encrypted_data
    try:
        cipher = get_fernet()
        decoded = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = cipher.decrypt(decoded)
        return decrypted.decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return encrypted_data

def hash_data(data: str) -> str:
    """Create one-way hash for data that doesn't need to be retrieved"""
    return hashlib.sha256(data.encode()).hexdigest()

def anonymize_email(email: str) -> str:
    """Anonymize email for deletion (GDPR right to be forgotten)"""
    username, domain = email.split('@')
    return f"deleted_{hash_data(email)[:8]}@{domain}"

def encrypt_user_data(user_data: dict) -> dict:
    """Encrypt sensitive fields in user data"""
    sensitive_fields = ['phone_number', 'address', 'passport_number']
    encrypted_data = user_data.copy()
    
    for field in sensitive_fields:
        if field in encrypted_data and encrypted_data[field]:
            encrypted_data[field] = encrypt_data(str(encrypted_data[field]))
    
    return encrypted_data

def decrypt_user_data(encrypted_data: dict) -> dict:
    """Decrypt sensitive fields in user data"""
    sensitive_fields = ['phone_number', 'address', 'passport_number']
    decrypted_data = encrypted_data.copy()
    
    for field in sensitive_fields:
        if field in decrypted_data and decrypted_data[field]:
            decrypted_data[field] = decrypt_data(str(decrypted_data[field]))
    
    return decrypted_data
