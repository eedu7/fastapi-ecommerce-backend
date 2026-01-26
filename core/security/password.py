import bcrypt


class PasswordManager:
    @staticmethod
    def hash(password: str) -> str:
        """Hash a plaintext password and return as UTF-8 string."""
        encoded = password.encode("utf-8")
        hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())
        return hashed.decode("utf-8")

    @staticmethod
    def verify(password: str, hashed_password: str) -> bool:
        """Verify a plaintext password against the hashed password."""
        encoded_password = password.encode("utf-8")
        encoded_hashed_password = hashed_password.encode("utf-8")
        return bcrypt.checkpw(encoded_password, encoded_hashed_password)
