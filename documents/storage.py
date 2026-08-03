import os
import base64
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from django.core.files.base import ContentFile

class AES256Storage(FileSystemStorage):
    """
    Military-grade AES-256 GCM encrypted storage.
    Encrypts files transparently before writing to disk and decrypts them upon retrieval.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 32 bytes = 256 bits for AES-256
        key = getattr(settings, 'AES_ENCRYPTION_KEY', None)
        if not key:
            raise ValueError("AES_ENCRYPTION_KEY must be a 32-byte base64 encoded string in settings.py")
        self.aesgcm = AESGCM(base64.b64decode(key))

    def _save(self, name, content):
        # Read the raw file data
        data = content.read()
        
        # Generate a random 12-byte nonce (standard for GCM)
        nonce = os.urandom(12)
        
        # Encrypt the data
        encrypted_data = nonce + self.aesgcm.encrypt(nonce, data, None)
        
        # Replace the content with the encrypted payload
        encrypted_content = ContentFile(encrypted_data)
        
        return super()._save(name, encrypted_content)

    def open(self, name, mode='rb'):
        # Open the file via standard FileSystemStorage
        file_obj = super().open(name, mode)
        
        if 'w' in mode:
            return file_obj
            
        encrypted_data = file_obj.read()
        if not encrypted_data:
            return file_obj
            
        # The first 12 bytes are the nonce, the rest is the ciphertext
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        
        try:
            decrypted_data = self.aesgcm.decrypt(nonce, ciphertext, None)
        except Exception:
            # If decryption fails (e.g. legacy unencrypted file), return original
            file_obj.seek(0)
            return file_obj
            
        return ContentFile(decrypted_data)
