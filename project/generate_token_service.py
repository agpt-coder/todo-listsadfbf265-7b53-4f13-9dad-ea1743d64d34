from datetime import datetime, timedelta

import jwt
import prisma
import prisma.models
from passlib.context import CryptContext
from pydantic import BaseModel


class TokenResponseModel(BaseModel):
    """
    Will output the JWT token along with user information and token expiry details if authentication is successful.
    """

    token: str
    token_type: str
    expires_in: int
    user_id: int


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that the plain text password matches the hashed password.

    Args:
        plain_password (str): The plain text password to check.
        hashed_password (str): The hashed password to compare.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def generate_token(username: str, password: str) -> TokenResponseModel:
    """
    Generates a new JWT token for authenticated users. It accepts a username and password, verifies these credentials using the UserManagementModule, and returns a JWT token if the credentials are valid. The token contains user information and expiration details.

    Args:
        username (str): The username of the user trying to authenticate. This will be used to look up the user in the database.
        password (str): The password of the user trying to authenticate. This will be used in conjunction with the username to verify the user's identity.

    Returns:
        TokenResponseModel: Will output the JWT token along with user information and token expiry details if authentication is successful.

    Example:
        generate_token("john_doe", "password123")
        > TokenResponseModel(token="eyJhbGciOiJIUzI1NiI", token_type="Bearer", expires_in=3600, user_id=1)
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if not user or not verify_password(password, user.password):
        raise ValueError("Incorrect username or password")
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": str(user.id),
        "exp": expire,
        "username": username,
        "role": user.role,
    }
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return TokenResponseModel(
        token=token,
        token_type="Bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_id=user.id,
    )
