import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings


class AES256:
    def __init__(self):
        self.key = settings.AES256_KEY
        self.salt_bytes = bytes([64] * 20)
        self.iv = bytes([64] * 16)

    def get_cipher(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA1(), length=32, salt=self.salt_bytes, iterations=70000
        )
        secret_key = kdf.derive(self.key.encode())
        cipher = Cipher(
            algorithm=algorithms.AES(secret_key),
            mode=modes.CBC(self.iv),
            backend=default_backend(),
        )
        return cipher

    def encrypt_ase(self, base):
        encryptor = self.get_cipher().encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(base.encode()) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        buffer = self.salt_bytes + self.iv + encrypted_data
        return base64.b64encode(buffer).decode()

    def decrypt_ase(self, base):
        decryptor = self.get_cipher().decryptor()
        buffer = base64.b64decode(base)[len(self.salt_bytes) + len(self.iv) :]
        padder = padding.PKCS7(128).unpadder()
        decryptor_data = decryptor.update(buffer) + decryptor.finalize()
        unpadded_data = padder.update(decryptor_data) + padder.finalize()
        return unpadded_data.decode()
