from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.crypto import constant_time_compare


class PlainTextPasswordHasher(BasePasswordHasher):
    """
    A password hasher that stores passwords in plain text (no hashing).
    FOR DEVELOPMENT / INTERNAL USE ONLY — not suitable for production.
    """
    algorithm = "plaintext"

    def salt(self):
        return ""

    def encode(self, password, salt):
        return f"{self.algorithm}$${password}"

    def decode(self, encoded):
        algorithm, _, password = encoded.split("$", 2)
        return {
            "algorithm": algorithm,
            "hash": password,
        }

    def verify(self, password, encoded):
        decoded = self.decode(encoded)
        return constant_time_compare(password, decoded["hash"])

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            "algorithm": decoded["algorithm"],
            "password": decoded["hash"],
        }

    def must_update(self, encoded):
        return False
