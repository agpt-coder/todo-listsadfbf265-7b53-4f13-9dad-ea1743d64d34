import datetime
from typing import Any, Dict

import jwt
from pydantic import BaseModel


class TokenResponse(BaseModel):
    """
    Response model includes the new JWT token provided upon successful verification of the refresh token.
    """

    access_token: str
    token_type: str
    expires_in: int


JWT_SECRET = "your_secret_key_here"

JWT_ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def verify_refresh_token(token: str) -> Dict[str, Any]:
    """
    Verifies the given refresh token using JWT.

    Args:
        token (str): The JWT refresh token to verify.

    Returns:
        Dict[str, Any]: The payload contained in the token if valid.

    Example:
        valid_payload = await verify_refresh_token("some_refresh_token")
        > {"user_id": 1, "exp": 1619027098}
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Expired refresh token")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid refresh token")


def create_access_token(data: Dict[str, Any], expires_delta: datetime.timedelta) -> str:
    """
    Creates a new JWT token with the specified data and expiration time.

    Args:
        data (Dict[str, Any]): The data to encode within the token.
        expires_delta (datetime.timedelta): The amount of time before the token expires.

    Returns:
        str: The newly created JWT token.

    Example:
        data = {"user_id": 1}
        token = create_access_token(data, datetime.timedelta(minutes=30))
        > "eyJhbGciOiJIUzI1NiIs..."
    """
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def refresh_token(refresh_token: str) -> TokenResponse:
    """
    Refreshes an existing JWT token. It accepts a valid refresh token, verifies its authenticity, and returns a new JWT token with updated expiration. This ensures continuous access without requiring the user to re-authenticate.

    Args:
        refresh_token (str): The refresh token that needs to be verified and used for generating a new JWT token.

    Returns:
        TokenResponse: Response model includes the new JWT token provided upon successful verification of the refresh token.

    Example:
        refreshed_token_response = await refresh_token("some_valid_refresh_token")
        > TokenResponse(access_token="new_access_token", token_type="Bearer", expires_in=1800)
    """
    payload = await verify_refresh_token(refresh_token)
    user_id = payload.get("user_id")
    if not user_id:
        raise ValueError("Invalid token payload")
    expires_delta = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_token = create_access_token({"user_id": user_id}, expires_delta)
    return TokenResponse(
        access_token=new_token,
        token_type="Bearer",
        expires_in=int(expires_delta.total_seconds()),
    )
