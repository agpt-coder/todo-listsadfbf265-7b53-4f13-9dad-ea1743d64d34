from datetime import datetime

import jwt
import prisma
import prisma.models
from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    """
    This response model contains the profile details of the authenticated user, including username, email, and other profile-related data retrieved from the User model.
    """

    id: int
    username: str
    email: str
    role: str
    createdAt: datetime
    updatedAt: datetime


async def getUserProfile(Authorization: str) -> UserProfileResponse:
    """
    Retrieves the profile details of the authenticated user. This includes personal information like username, email, and other profile-related data. Requires a valid token.

    Args:
    Authorization (str): Bearer token for authenticating the request.

    Returns:
    UserProfileResponse: This response model contains the profile details of the authenticated user, including username, email, and other profile-related data retrieved from the User model.

    Example:
        response = await getUserProfile('Bearer <token>')
        > UserProfileResponse(id=1, username="john_doe", email="john@example.com", role="User", createdAt=datetime.datetime(2022, 1, 23, 14, 29, 44), updatedAt=datetime.datetime(2023, 2, 5, 19, 23, 44))
    """
    token = Authorization.split(" ")[1]
    SECRET_KEY = "YOUR_SECRET_KEY"
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload.get("user_id")
    if not user_id:
        raise ValueError("Invalid token or token does not contain user information")
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if not user:
        raise ValueError("User not found")
    return UserProfileResponse(
        id=user.id,
        username=user.email.split("@")[0],
        email=user.email,
        role=user.role,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt,
    )
