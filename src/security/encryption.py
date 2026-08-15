"""
Encryption Engine - XOR encryption with key
"""
import hashlib


class EncryptionEngine:
    """Simple XOR encryption for data protection"""

    def __init__(self, key: str = "neurosonic_secret_2024"):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, data: str) -> str:
        """Encrypt data using XOR"""
        result = bytearray()
        data_bytes = data.encode("utf-8")
        for i, byte in enumerate(data_bytes):
            result.append(byte ^ self.key[i % len(self.key)])
        return result.hex()

    def decrypt(self, data_hex: str) -> str:
        """Decrypt data"""
        try:
            data = bytes.fromhex(data_hex)
            result = bytearray()
            for i, byte in enumerate(data):
                result.append(byte ^ self.key[i % len(self.key)])
            return result.decode("utf-8")
        except Exception as e:
            return f"[Decryption error: {e}]"
