from datetime import datetime

import jwt
import prisma
import prisma.models
from pydantic import BaseModel


class InvalidateTokenResponse(BaseModel):
    """
    Response model after a JWT token is invalidated successfully. This includes a status message confirming the invalidation.
    """

    status: str


def decode_token(token: str) -> int:
    """
    Decodes a JWT token to extract the user ID.

    Args:
        token (str): The JWT token that needs to be decoded.

    Returns:
        int: The extracted user ID from the decoded token.

    Example:
        token = "eyJhbGciOiJIUzI1NiIsIn..."
        decode_token(token)
        > 123
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise ValueError("Token does not contain user_id")
        return user_id
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Token decoding error: {e}")


SECRET_KEY = "your-secret-key"

ALGORITHM = "HS256"


async def invalidate_token(token: str) -> InvalidateTokenResponse:
    """
    Invalidates an existing JWT token, effectively logging the user out. It marks the token as unusable in the token store. This endpoint ensures that the user can log out securely, and their token cannot be reused.

    Args:
    token (str): The JWT token that needs to be invalidated.

    Returns:
    InvalidateTokenResponse: Response model after a JWT token is invalidated successfully. This includes a status message confirming the invalidation.

    Example:
        token = "eyJhbGciOiJIUzI1NiIsIn..."
        invalidate_token(token)
        > InvalidateTokenResponse(status="Token has been successfully invalidated.")
    """
    user_id = decode_token(token)
    await prisma.models.AuditLog.prisma().create(
        data={
            "action": "invalidate_token",
            "userId": user_id,
            "timestamp": datetime.utcnow(),
        }
    )
    return InvalidateTokenResponse(status="Token has been successfully invalidated.")
