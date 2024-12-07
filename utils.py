import base64
import hashlib
import os


def generate_jwt_secret_key(random_byte_sequence_length: int = 64) -> str:
    # `length` parameter determines the length of the random byte sequence, larger number - more "randomness"
    random_bytes = os.urandom(random_byte_sequence_length)
    sha256_hash = hashlib.sha256(random_bytes).digest()
    base64_encoded_key = base64.urlsafe_b64encode(sha256_hash).rstrip(b"=")
    scrambled_key = base64.urlsafe_b64encode(hashlib.sha256(sha256_hash[::-1]).digest()).rstrip(b"=")
    combined_key = base64_encoded_key + scrambled_key
    return combined_key.decode("utf-8")


def convert_bytes_to_mb(file_size):
    """
    1 MB = 1000^2 bytes
    1 MiB = 1024^2 bytes
    https://stackoverflow.com/questions/2365100/converting-bytes-to-megabytes
    """
    return float(file_size / (1000**2))


ALLOWED_METHODS = {
    "/": ["GET"],
    "/upload/": ["POST"],
    "/image-preview/": ["GET"],
    "/images/": ["GET"],
    "/register/": ["POST"],
    "/login/": ["POST"],
    "/logout/": ["POST"],
    "/docs": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
}
