import hmac
import hashlib
import base64

from typing import Optional

COOKIE_SECRET_KEY = "1b7d5142d2d34edc51d306c8e4a91d70fca60355a6b7a514283545e0271868ff"  # openssl rand -hex 32
PASSWORD_SECRET_KEY = "a3fb79cb59c0eb0260d78edf3a7d8c0d33c5d4019129589372a73f21beae0e6f"  # openssl rand -hex 32


def sign_data(data: str) -> str:
    return (
        hmac.new(
            COOKIE_SECRET_KEY.encode(), msg=data.encode(), digestmod=hashlib.sha256
        )
        .hexdigest()
        .upper()
    )


def get_username_from_signed_data(signed_username: str) -> Optional[str]:
    try:
        username_base64, sign = signed_username.split(".")
        username = base64.b64decode(username_base64.encode()).decode()
        valid_sign = sign_data(username)

        if hmac.compare_digest(sign, valid_sign):
            return username

    except ValueError:
        return None


def hash_password(password: str) -> str:
    return hashlib.sha256((password + PASSWORD_SECRET_KEY).encode()).hexdigest()
