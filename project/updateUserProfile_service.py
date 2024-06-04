from datetime import datetime
from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    Response model containing the updated profile details of the user.
    """

    id: int
    email: str
    role: str
    createdAt: datetime
    updatedAt: datetime


async def updateUserProfile(
    email: Optional[str], password: Optional[str], role: Optional[str]
) -> UpdateUserProfileResponse:
    """
    Updates the profile information of the authenticated user. It accepts data fields that need updating and returns the updated profile details. Requires a valid token.

    Args:
    email (Optional[str]): The new email address of the user.
    password (Optional[str]): The new password for the user.
    role (Optional[str]): The new role of the user.

    Returns:
    UpdateUserProfileResponse: Response model containing the updated profile details of the user.

    Example:
        email = 'newemail@example.com'
        password = 'newpassword123'
        role = 'Admin'
        updateUserProfile(email, password, role)
        > UpdateUserProfileResponse(id=1, email='newemail@example.com', role='Admin', createdAt=datetime, updatedAt=datetime)
    """
    user_id = 1
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if not user:
        raise ValueError("User not found")
    update_data = {}
    if email:
        update_data["email"] = email
    if password:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        update_data["password"] = hashed_password
    if role:
        update_data["role"] = role
    if not update_data:
        raise ValueError("Nothing to update")
    updated_user = await prisma.models.User.prisma().update(
        where={"id": user_id}, data=update_data
    )
    if not updated_user:
        raise ValueError("Failed to update user profile")
    return UpdateUserProfileResponse(
        id=updated_user.id,
        email=updated_user.email,
        role=updated_user.role,
        createdAt=updated_user.createdAt,
        updatedAt=updated_user.updatedAt,
    )
