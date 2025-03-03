import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,             # 256-bit key
        salt=salt,
        iterations=100000
    )
    return kdf.derive(password.encode())

def encrypt_data(data: bytes, password: str) -> bytes:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce for AES-GCM
    ciphertext = aesgcm.encrypt(nonce, data, None)
    # Return salt + nonce + ciphertext
    return salt + nonce + ciphertext

def decrypt_data(token: bytes, password: str) -> bytes:
    salt = token[:16]
    nonce = token[16:28]
    ciphertext = token[28:]
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    try:
        return aesgcm.decrypt(nonce, ciphertext, None)
    except Exception as e:
        raise ValueError("Incorrect password or corrupted data") from e
